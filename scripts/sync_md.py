#!/usr/bin/env python3
import argparse
import os
import re
import sys

# Add current dir to path to import run_md_blocks
sys.path.append(os.path.dirname(__file__))
import run_md_blocks  # noqa: E402


def sync_markdown(md_path: str):
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    meta = run_md_blocks.parse_top_comment(content)

    # Pattern to find a code block and a following result marker
    # Group 1: code block including backticks
    # Group 2: code inside backticks
    # Group 3: text between code block and end-result tag
    pattern = re.compile(
        r"(```(?:python|py)\n(.*?)\n```)\s*<!--\s*result\s*-->(.*?)<!--\s*end-result\s*-->",
        re.S | re.I,
    )

    all_blocks = run_md_blocks.extract_py_blocks(content)

    def replace_func(match):
        code_block_full = match.group(1)
        code_content = match.group(2).strip()

        try:
            block_idx = all_blocks.index(code_content)
            cumulative_blocks = all_blocks[: block_idx + 1]
        except ValueError:
            return match.group(0)

        print(f"Running block {block_idx + 1} from {md_path}...")
        temp_path = run_md_blocks.build_temp_script(md_path, meta, cumulative_blocks)
        try:
            code, out = run_md_blocks.run_with_uv(temp_path)
            display_out = out.strip()

            if not display_out.startswith("|"):
                display_out = f"```text\n{display_out}\n```"

            return f"{code_block_full}\n<!-- result -->\n{display_out}\n<!-- end-result -->"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    new_content = pattern.sub(replace_func, content)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Synced {md_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("mdfile", help="Markdown file to sync")
    args = p.parse_args()

    if not os.path.exists(args.mdfile):
        print(f"File not found: {args.mdfile}")
        sys.exit(1)

    sync_markdown(args.mdfile)


if __name__ == "__main__":
    main()
