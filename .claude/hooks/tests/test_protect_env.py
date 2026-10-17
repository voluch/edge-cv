import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parents[1] / "protect_env.py"


def run(tool: str, **tool_input) -> int:
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input})
    return subprocess.run(
        [sys.executable, str(HOOK)], input=payload, text=True, capture_output=True
    ).returncode


@pytest.mark.parametrize(
    "tool,path,code",
    [
        ("Edit", "/x/.env", 2),
        ("Write", "/x/sub/.env.local", 2),
        ("MultiEdit", ".env", 2),
        ("Write", "/x/.env_template", 0),
        ("Edit", "/x/.env.example", 0),
        ("Edit", "/x/environment.py", 0),
    ],
)
def test_file_tools(tool, path, code):
    assert run(tool, file_path=path) == code


@pytest.mark.parametrize(
    "cmd,code",
    [
        ("rm .env", 2),
        ("rm -f ./.env", 2),
        ("echo X=1 >> ./.env", 2),
        ("echo X=1 >.env", 2),
        ("sed -i s/a/b/ .env", 2),
        ("mv .env /tmp/x", 2),
        ("cp .env_template .env", 2),
        ("cp .env.example .env.bak", 2),
        ("git rm .env", 2),
        ("git clean -fdx", 2),
        ("tee .env", 2),
        ("ls && rm .env", 2),
        ("bash -c 'rm .env'", 2),
        ("FOO=1 rm .env", 2),
        # allowed
        ("rm .env_template", 0),
        ("ls -la", 0),
        ("grep -c KEY .env", 0),
        ("cat .env_template", 0),
        ("cp .env_template /tmp/t", 0),
        ('git commit -m "protect .env files <x>"', 0),
        ('git commit -m "mention .env" 2>&1', 0),
        ("echo 'rm .env' > notes.txt", 0),
        ("git clean -fd", 0),
    ],
)
def test_bash(cmd, code):
    assert run("Bash", command=cmd) == code
