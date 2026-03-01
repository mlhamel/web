.PHONY: help serve build check clean setup post

# Default target: show help
help:
	@echo "Available targets:"
	@echo "  serve    - Start local development server with live reload"
	@echo "  build    - Build the static site into the 'public' directory"
	@echo "  check    - Check the site for broken links"
	@echo "  clean    - Remove the 'public' directory"
	@echo "  setup    - Install Zola (Debian/Ubuntu)"
	@echo "  post     - Create a new blog post (usage: make post SLUG=my-post-slug)"

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

# Create a new blog post
post:
	@if [ -z "$(SLUG)" ]; then echo "Usage: make post SLUG=my-post-slug"; exit 1; fi
	@mkdir -p content/blog/$(SLUG)
	@printf "+++\ntitle = \"$(SLUG)\"\ndate = $(shell date +%Y-%m-%d)\ndescription = \"\"\n[taxonomies]\ntags = []\n+++\n" > content/blog/$(SLUG)/index.md
	@echo "Created content/blog/$(SLUG)/index.md"
