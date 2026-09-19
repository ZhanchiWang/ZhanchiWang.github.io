# Zhanchi Wang - personal homepage

A single-page academic website hosted at https://ZhanchiWang.github.io/.

## Update content

- Biography and contact links: `scripts/homepage.html`.
- Publications: `_data/publications.json`.
- Layout and mobile styling: `assets/css/homepage.css`.
- Portrait: `images/profile.png`.

After editing, run:

```powershell
python scripts/build_homepage.py
python -m http.server 8000
```

Open http://localhost:8000. Stop the server with Ctrl+C.
The generator produces `index.html`, individual `references/*.bib`, and the combined bibliography.
The page and BibTeX expansion work without JavaScript.

## Add a publication

Copy an entry in `_data/publications.json`. Set a unique `id`, title, complete authors,
date (`YYYY`, `YYYY-MM`, or `YYYY-MM-DD`), venue, type (`article`, `inproceedings`,
or `misc` for preprints), and paper URL. Optional fields: volume, number, pages,
publisher, doi. Keep `source` as a provenance link. Dates are sorted automatically;
Zhanchi Wang is automatically bolded in the displayed authors. BibTeX preserves source spelling.
Re-run the generator and commit the data, generated HTML, and bibliography together.

## Publish

```powershell
git add index.html _config.yml _data/publications.json scripts assets/css/homepage.css references README.md
git commit -m "Update academic homepage"
git push
```

GitHub Settings > Pages: deploy from `main`, `/ (root)`.
Old Academic Pages source files are retained for reference but excluded from publishing.

## Bibliography provenance

Publication metadata was retrieved from Google Scholar profile VRPyvDAAAAAJ and its
individual records on 2026-09-19. Two undated duplicate records were omitted.
The OpenSpiRobs software entry is not counted as a paper. Preprints are explicitly
identified by their arXiv venue. Dates follow Scholar (including online publication dates).
The 2026 De-occlusion record spells the author name "Zhanci Wang"; the citation
preserves that spelling and the homepage highlights it. Confirm with the publisher
before correcting bibliographic metadata. BibTeX is generated from the retrieved
metadata, not represented as publisher-exported citations.
