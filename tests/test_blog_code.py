import glob
import os
import sys

import pytest

# Add scripts directory to path to import run_md_blocks
scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.append(scripts_dir)

import run_md_blocks  # noqa: E402


def get_all_test_cases():
    """Collects all individual code blocks across all blog posts."""
    test_cases = []
    base_dir = os.path.join(os.path.dirname(__file__), "..", "content", "blog")
    md_files = glob.glob(os.path.join(base_dir, "**", "*.md"), recursive=True)

    for md_path in sorted(md_files):
        with open(md_path, encoding="utf-8") as f:
            text = f.read()

        meta = run_md_blocks.parse_top_comment(text)
        blocks = run_md_blocks.extract_py_blocks(text)

        post_name = os.path.basename(os.path.dirname(md_path))

        for i, _block in enumerate(blocks):
            # Run blocks cumulatively to maintain state (imports, variables)
            cumulative_blocks = blocks[: i + 1]
            test_id = f"{post_name}-block-{i + 1}"
            test_cases.append(
                pytest.param(md_path, cumulative_blocks, meta, id=test_id)
            )

    return test_cases


@pytest.mark.parametrize("md_path, blocks, meta", get_all_test_cases())
def test_markdown_code_block(md_path, blocks, meta):
    temp_path = run_md_blocks.build_temp_script(md_path, meta, blocks)
    try:
        code, out = run_with_uv_test_helper(temp_path)
        assert code == 0, f"Failure in {md_path} at block {len(blocks)}:\n{out}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def run_with_uv_test_helper(temp_path: str):
    """Reuse logic from run_md_blocks but wrapped for tests."""
    import subprocess

    cmd = ["uv", "run", "--no-project", temp_path]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    return proc.returncode, proc.stdout
