#!/usr/bin/env python3
"""Extract and run Python code blocks from a Markdown file using `uv run`.

Usage: scripts/run_md_blocks.py path/to/file.md

The script will look for a top HTML comment containing a `dependencies` list
and will create a temporary Python file with a uv-style header so `uv run`
installs requirements automatically before running.
"""

import argparse
import ast
import os
import re
import subprocess
import sys
import tempfile


def parse_top_comment(text: str):
    m = re.search(r"<!--\s*(.*?)\s*-->", text, re.S)
    if not m:
        return {}
    body = m.group(1)
    result = {}
    # find requires-python
    m_req = re.search(r"requires-python\s*=\s*\"([^\"]+)\"", body)
    if m_req:
        result["requires-python"] = m_req.group(1)
    # find dependencies list
    m_deps = re.search(r"dependencies\s*=\s*(\[[^\]]*\])", body, re.S)
    if m_deps:
        try:
            deps = ast.literal_eval(m_deps.group(1))
            result["dependencies"] = deps
        except Exception:
            pass
    return result


def extract_py_blocks(text: str):
    blocks = re.findall(r"```(?:python|py)\n(.*?)\n```", text, re.S | re.I)
    return [b.strip() for b in blocks if b.strip()]


def build_temp_script(md_path: str, comment_meta: dict, blocks: list[str]):
    fd, temp_path = tempfile.mkstemp(prefix="run_md_", suffix=".py", dir=os.getcwd())
    with os.fdopen(fd, "w") as f:
        if comment_meta.get("dependencies"):
            f.write("# /// script\n")
            req = comment_meta.get("requires-python", ">=3.9")
            f.write(f'# requires-python = "{req}"\n')
            f.write("# dependencies = [\n")
            for d in comment_meta.get("dependencies", []):
                f.write(f'#     "{d}",\n')
            f.write("# ]\n")
            f.write("# ///\n\n")
        # helpful comment
        f.write(f"# Generated from {md_path}\n\n")
        for i, b in enumerate(blocks):
            f.write(f"# --- block {i + 1} ---\n")
            f.write(b)
            f.write("\n\n")
    return temp_path


def run_with_uv(temp_path: str):
    # Use `uv run` so dependencies declared in the header are auto-installed
    cmd = ["uv", "run", "--no-project", temp_path]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    return proc.returncode, proc.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument("mdfile", help="Markdown file to scan")
    args = p.parse_args()

    if not os.path.exists(args.mdfile):
        print("File not found:", args.mdfile, file=sys.stderr)
        sys.exit(2)

    text = open(args.mdfile, encoding="utf-8").read()
    meta = parse_top_comment(text)
    blocks = extract_py_blocks(text)
    if not blocks:
        print("No python code blocks found.")
        sys.exit(0)

    temp = build_temp_script(args.mdfile, meta, blocks)
    try:
        code, out = run_with_uv(temp)
        print(out)
        sys.exit(code)
    finally:
        try:
            os.remove(temp)
        except Exception:
            pass


if __name__ == "__main__":
    main()
