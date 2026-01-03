# MkDocs MoreRelativePaths

A MkDocs plugin that intelligently rewrites file paths in markdown to handle common directory organization patterns, particularly for Material for MkDocs.

## The Problem

When organizing documentation with assets in subfolders that mirror page names, MkDocs path resolution can be inconsistent:

```
docs/
├── tutorial/
│   ├── index.md          # References: ![](image.png)
│   └── tutorial/         # Assets subfolder
│       └── image.png
└── guide.md              # References: ![](diagram.png)
    └── guide/            # Assets subfolder
        └── diagram.png
```

This plugin automatically detects these patterns and rewrites paths so they resolve correctly.

## Installation

```yaml
# mkdocs.yml
plugins:
  - morerelativepaths
```

No configuration options required.

## How It Works

### Processing Flow

```
Markdown Source
       │
       ▼
┌────────────────────────────────┐
│  on_page_markdown()            │
│  ┌──────────────────────────┐  │
│  │ Determine page type      │  │
│  │ • index.md → use parent  │  │
│  │   directory name         │  │
│  │ • page.md → use page     │  │
│  │   stem as subfolder      │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │ Find matching subfolder  │  │
│  │ (case-insensitive)       │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │ Rewrite paths if:        │  │
│  │ • Resource exists in     │  │
│  │   subfolder              │  │
│  │ • Page is index.md       │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
       │
       ▼
  Modified Markdown
```

### Path Resolution Logic

**For `index.md` files:**
- Checks for a sibling subfolder matching the parent directory name
- Rewrites paths to include the subfolder prefix
- Example: `docs/tutorial/index.md` with `![](image.png)` → `![](tutorial/image.png)`

**For regular pages (e.g., `page.md`):**
- Checks for a sibling subfolder matching the page stem
- Does NOT rewrite paths (MkDocs outputs `page.md` as `page/index.html`, so relative paths already work)

### Supported Patterns

The plugin rewrites both markdown and HTML syntax:

**Markdown images:**
```markdown
![alt text](image.png)
![alt text](image.png){attributes}
!![alt text](image.png)
```

**HTML attributes:**
```html
<img src="image.png">
<video src="video.mp4">
<a href="document.pdf">
```

---

## Examples

### Directory Structure

```
docs/
├── projects/
│   ├── index.md
│   └── projects/           # Subfolder matches parent dir
│       ├── screenshot.png
│       └── demo.mp4
└── setup.md
    └── setup/              # Subfolder matches page stem
        └── diagram.png
```

### Before Plugin (index.md)

```markdown
# Projects

![Screenshot](screenshot.png)
```

Path fails because `screenshot.png` is actually in `projects/projects/`.

### After Plugin (index.md)

```markdown
# Projects

![Screenshot](projects/screenshot.png)
```

Path is rewritten to find the file in the subfolder.

### Non-Index Pages

For `setup.md`, paths are NOT rewritten because MkDocs outputs it as `setup/index.html`, making relative paths work automatically.

---

## Skipped Paths

The plugin does not modify:

- External URLs (`http://`, `https://`, `//`)
- Absolute paths (`/images/...`)
- Paths already containing the subfolder name
- Resources that don't exist in the expected subfolder

---

## Use Case

This plugin is designed to run early in the plugin chain, normalizing paths before other plugins (like displaymotron) process the markdown. It enables a clean file organization where each page's assets live in a matching subfolder.

---

## License

MIT
