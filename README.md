# AI Interview Handbook (static site generator)

Generates a static, searchable **2026 AI Interview Handbook** website from a folder of Markdown chapters.

- `build.py` converts the chapters to HTML (Python `markdown` with table-of-contents support), builds a search
  index and writes the site to `dist/`.
- `app.js` is the client: sidebar navigation, mobile menu and a full-text search overlay.
- `styles.css` is the styling.

## Use

```bash
pip install markdown
python build.py        # writes ./dist
```

**Source content is not in this repo.** `build.py` reads from a hard-coded path
(`/home/ubuntu/grok/ai-interview-prep-2026`). The chapters are in the public archive repo
[`ai-apps-dump`](https://github.com/manojastro/ai-apps-dump) under `research topic/ai-interview-prep-2026`;
change `SRC` in `build.py` to point at them.

## Status

Small utility (about 1,100 lines), no tests.
