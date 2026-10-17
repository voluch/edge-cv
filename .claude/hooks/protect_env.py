#!/usr/bin/env python3
"""PreToolUse hook: block edits to, and removal of, .env files (.env, .env.local, ...).

.env_template, .env.example, .env.sample and .env.template are allowed.
Exit code 2 blocks the tool call and shows stderr to Claude.

Bash commands are parsed into segments and words, so a mention of .env inside a quoted
string (a commit message, an echo) is not a match. Best effort: it does not expand globs
or run-time constructed paths, so `rm -rf *` is not caught.
"""

import json
import os
import re
import shlex
import sys

ALLOWED = {".env.example", ".env.sample", ".env.template"}
ENV_RE = re.compile(r"^\.env(\..+)?$")
# commands where every protected argument is a modification or removal
WRITERS = {
    "rm", "mv", "tee", "truncate", "shred", "unlink", "chmod", "chown", "ln", "install", "dd",
}
# commands where only the last argument (the destination) is modified
DEST_ONLY = {"cp", "rsync", "scp"}
PREFIXES = {"sudo", "command", "env", "nohup", "time"}


def block(reason: str) -> None:
    print(
        f"Blocked: {reason}. .env files hold secrets and must be changed by the user, "
        "not Claude. Edit .env_template instead.",
        file=sys.stderr,
    )
    sys.exit(2)


def is_protected(path: str) -> bool:
    base = os.path.basename(path.rstrip("/"))
    return base not in ALLOWED and bool(ENV_RE.match(base))


def segments(command: str):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    seg: list[str] = []
    for tok in lexer:
        # tokens made only of ; & | ( ) are separators; redirects like > or >> are kept
        if set(tok) <= set(";&|()"):
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def check_segment(words: list[str]) -> None:
    # redirects: `> .env`, `>> .env`, `>.env`, `2>.env`
    for i, w in enumerate(words):
        m = re.match(r"^(\d*>>?|&>|>\|)(.*)$", w)
        if m:
            target = m.group(2) or (words[i + 1] if i + 1 < len(words) else "")
            if target and is_protected(target):
                block("redirect that writes to .env")

    while words and (re.match(r"^\w+=", words[0]) or words[0] in PREFIXES):
        words = words[1:]
    if not words:
        return
    cmd = os.path.basename(words[0])
    args = words[1:]
    paths = [a for a in args if not a.startswith("-")]

    if cmd in {"bash", "sh", "zsh"} and "-c" in args:
        idx = args.index("-c")
        if idx + 1 < len(args):
            check_command(args[idx + 1])
        return
    if cmd in WRITERS and any(is_protected(a) for a in paths):
        block(f"{cmd} on .env")
    if cmd in DEST_ONLY and paths and is_protected(paths[-1]):
        block(f"{cmd} onto .env")
    if cmd in {"sed", "perl"} and any(
        a == "--in-place" or re.match(r"^-[a-zA-Z]*i", a) for a in args
    ):
        if any(is_protected(a) for a in paths):
            block(f"in-place {cmd} on .env")
    if cmd == "git" and args:
        sub, rest = args[0], args[1:]
        if sub in {"rm", "mv", "checkout", "restore", "stash"} and any(
            is_protected(a) for a in rest
        ):
            block(f"git {sub} on .env")
        # `git clean -x` also deletes ignored files such as .env
        if sub == "clean" and any(re.match(r"^-[a-zA-Z]*x", a) for a in rest):
            block("git clean -x would delete ignored files such as .env")


def check_command(command: str) -> None:
    try:
        for seg in segments(command):
            check_segment(seg)
    except ValueError:
        # unparseable quoting: fall back to a conservative scan of the raw text
        if re.search(r"\b(rm|mv|tee|truncate|shred)\b[^\n;|&]*\s\.env(\.\w+)?(\s|$)", command):
            block("unparseable command that appears to modify .env")


def main() -> None:
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    tin = data.get("tool_input") or {}
    if tool in {"Edit", "Write", "MultiEdit", "NotebookEdit"}:
        path = tin.get("file_path") or tin.get("notebook_path") or ""
        if path and is_protected(path):
            block(f"{tool} on {path}")
    elif tool == "Bash":
        check_command(tin.get("command", ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
