# Personal Website

A personal website built with [Zola](https://www.getzola.org/), a fast static site generator written in Rust.

## Prerequisites

- Git
- Zola

## Setup

### Install Zola

**Debian/Ubuntu:**
```bash
./scripts/install-zola.sh
```

**Or manually:**
```bash
# Download latest release
curl -sL https://github.com/getzola/zola/releases/download/v0.19.2/zola-v0.19.2-x86_64-unknown-linux-gnu.tar.gz | tar xz

# Move to local bin
mkdir -p ~/.local/bin
mv zola ~/.local/bin/

# Ensure ~/.local/bin is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Build and Run Locally

```bash
# Serve with live reload
zola serve

# Build for production
zola build
```

Site will be available at http://127.0.0.1:1111

## Deploy to GitHub Pages

1. Create a repository named `mlhamel.github.io` or use a project repository
2. Push your code:
```bash
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/mlhamel/web.git
git push -u origin main
```

3. GitHub Actions will automatically build and deploy (see `.github/workflows/deploy.yml`)

Your site will be live at: `https://mlhamel.github.io/web/`

## Project Structure

```
.
├── config.toml          # Site configuration
├── content/             # Markdown content
│   ├── _index.md       # Homepage
│   ├── about.md        # About page
│   └── blog/           # Blog posts
├── templates/           # HTML templates
├── static/              # Static assets (CSS, images)
├── sass/                # SCSS stylesheets
└── .github/workflows/   # CI/CD automation
```

## Customization

- Edit `config.toml` to change site settings
- Modify templates in `templates/`
- Add content in `content/`
- Update styles in `sass/` or `static/`
