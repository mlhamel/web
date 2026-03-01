import os
import glob
import pytest
import sys
import importlib.util

# Add scripts directory to path to import run_md_blocks
scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.append(scripts_dir)

import run_md_blocks

def get_blog_files():
    # find all index.md in blog subdirs
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'blog')
    files = glob.glob(os.path.join(base_dir, '**', '*.md'), recursive=True)
    return sorted(files)

@pytest.mark.parametrize("md_path", get_blog_files())
def test_markdown_code_blocks(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    meta = run_md_blocks.parse_top_comment(text)
    blocks = run_md_blocks.extract_py_blocks(text)
    
    if not blocks:
        pytest.skip(f"No python blocks in {os.path.basename(os.path.dirname(md_path))}")
        
    temp_path = run_md_blocks.build_temp_script(md_path, meta, blocks)
    try:
        code, out = run_with_uv_test_helper(temp_path)
        assert code == 0, f"Error running blocks in {md_path}: {out}"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def run_with_uv_test_helper(temp_path: str):
    """Reuse logic from run_md_blocks but wrapped for tests."""
    import subprocess
    cmd = ["uv", "run", "--no-project", temp_path]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout
