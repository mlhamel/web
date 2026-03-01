.PHONY: help serve build check clean setup post uv-sync run-md

# Default target: show help
help:
	@echo "Available targets:"
	@echo "  serve    - Start local development server with live reload"
	@echo "  build    - Build the static site into the 'public' directory"
	@echo "  check    - Check the site for broken links"
	@echo "  clean    - Remove the 'public' directory"
	@echo "  setup    - Install Zola (Debian/Ubuntu)"
	@echo "  post     - Create a new blog post (usage: make post SLUG=my-post-slug)"
	@echo "  test     - Run all blog code block tests with pytest"

# Start local development server
serve:
	zola serve

# Build the static site
build:
	zola build

# Check for broken links
check:
	zola check

# Remove generated files
clean:
	rm -rf public

# Install Zola using the provided script
setup:
	chmod +x scripts/install-zola.sh
	./scripts/install-zola.sh

# Synchronize Python dependencies via uv (creates .venv)
uv-sync:
	uv sync --no-install-project

# Run python code blocks from a markdown file (argument: MD=<path>)
run-md:
	@if [ -z "$(MD)" ]; then echo "Usage: make run-md MD=path/to/file.md"; exit 1; fi
	uv run --no-project scripts/run_md_blocks.py $(MD)

# Create a new blog post
post:
	@if [ -z "$(SLUG)" ]; then echo "Usage: make post SLUG=my-post-slug"; exit 1; fi
	@mkdir -p content/blog/$(SLUG)
	@printf "+++\ntitle = \"$(SLUG)\"\ndate = $(shell date +%Y-%m-%d)\ndescription = \"\"\n[taxonomies]\ntags = []\n+++\n" > content/blog/$(SLUG)/index.md
	@echo "Created content/blog/$(SLUG)/index.md"

# Run all code block tests
test:
	uv run --no-project pytest tests/
