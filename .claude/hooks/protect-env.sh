#!/usr/bin/env bash
# PreToolUse hook: block edits to, and removal of, .env files (.env, .env.local, ...).
# .env_template, .env.example, .env.sample and .env.template are allowed.
# Exit code 2 blocks the tool call and shows stderr to Claude.
# Best effort for Bash: it catches common write/remove commands, not every possible trick.
set -u

input=$(cat)
tool=$(jq -r '.tool_name // empty' <<<"$input")

block() {
  echo "Blocked: $1. .env files hold secrets and must be changed by the user, not Claude. Edit .env_template instead." >&2
  exit 2
}

is_protected_path() {
  local base
  base=$(basename -- "$1")
  case "$base" in
    .env.example | .env.sample | .env.template) return 1 ;;
    .env | .env.*) return 0 ;;
    *) return 1 ;;
  esac
}

case "$tool" in
  Edit | Write | MultiEdit | NotebookEdit)
    path=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' <<<"$input")
    if [ -n "$path" ] && is_protected_path "$path"; then
      block "$tool on $path"
    fi
    ;;
  Bash)
    cmd=$(jq -r '.tool_input.command // empty' <<<"$input")
    # a .env token: .env or .env.<suffix>, not .env_template / .env.example / .env.sample / .env.template
    token='(^|[[:space:]/"'"'"'=<>])\.env(\.[A-Za-z0-9_-]+)?($|[[:space:]"'"'"';|&)<>])'
    if [[ $cmd =~ $token ]]; then
      stripped=$(sed -E 's/\.env\.(example|sample|template)//g' <<<"$cmd")
      if [[ $stripped =~ $token ]]; then
        writers='(^|[[:space:];&|(])(rm|mv|cp|install|tee|truncate|shred|dd|ln|chmod|chown|unlink|rsync|scp|sed[[:space:]]+(-[a-zA-Z]*i|--in-place)|perl[[:space:]]+-[a-zA-Z]*i|git[[:space:]]+(rm|clean|checkout|restore|stash|reset|mv))([[:space:]]|$)|>'
        if [[ $stripped =~ $writers ]]; then
          block "Bash command that may modify or remove .env"
        fi
      fi
    fi
    ;;
esac
exit 0
