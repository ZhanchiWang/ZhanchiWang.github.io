"""Build the single-page site and BibTeX files using only the Python standard library."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def bibtex(p):
    fields = {'title': p['title'], 'author': ' and '.join(p['authors']), 'year': p['date'][:4]}
    fields['booktitle' if p['type'] == 'inproceedings' else 'journal' if p['type'] == 'article' else 'howpublished'] = p['venue']
    for key in ('volume', 'number', 'pages', 'publisher', 'doi', 'url'):
        if p.get(key):
            fields[key] = p[key].replace('-', '--') if key == 'pages' else p[key]
    def tex(value):
        return value.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')
    return '@' + p['type'] + '{' + p['id'] + ',\n' + ',\n'.join('  ' + k + ' = {' + (v if k == 'url' else tex(v)) + '}' for k, v in fields.items()) + '\n}\n'


def build():
    papers = json.loads((ROOT / '_data/publications.json').read_text(encoding='utf-8'))
    papers.sort(key=lambda p: tuple(int(x) for x in (p['date'] + '-0-0').split('-')[:3]), reverse=True)
    assert len({p['id'] for p in papers}) == len(papers), 'Duplicate publication IDs'
    bibdir = ROOT / 'references'
    bibdir.mkdir(exist_ok=True)
    rows, citations = [], []
    year = None
    for p in papers:
        assert re.fullmatch(r'[a-zA-Z0-9_-]+', p['id'])
        assert p['url'].startswith('https://')
        if year != p['date'][:4]:
            if year is not None:
                rows.append('</ul>')
            year = p['date'][:4]
            rows.append(f'<h3 class="year">{year}</h3><ul class="papers">')
        equal = p.get('equal_contributors', [])
        corresponding = p.get('corresponding_authors', [])
        assert set(equal + corresponding).issubset(p['authors']), 'Unknown annotated author'
        author_labels = []
        for a in p['authors']:
            label = '<strong>' + escape(a) + '</strong>' if a in ('Zhanchi Wang', 'Zhanci Wang', 'Z Wang') else escape(a)
            if a in equal:
                label += '<sup title="Equal contribution">*</sup>'
            if a in corresponding:
                label += '<sup title="Corresponding author">&dagger;</sup>'
            author_labels.append(label)
        authors = ', '.join(author_labels)
        bib = bibtex(p)
        citations.append(bib)
        (bibdir / (p['id'] + '.bib')).write_text(bib, encoding='utf-8')
        venue = escape(p['venue'])
        if p.get('volume'):
            venue += ', ' + escape(p['volume'])
            if p.get('number'):
                venue += '(' + escape(p['number']) + ')'
        if p.get('pages'):
            venue += ', ' + escape(p['pages'])
        rows.append(f'''<li class="paper">
<a class="paper-title" href="{escape(p['url'], quote=True)}">{escape(p['title'])}</a>
<div class="authors">{authors}.</div>
<div class="venue"><em>{venue}</em>, {year}.</div>
<div class="paper-links"><a href="{escape(p['url'], quote=True)}">[Paper]</a>
<details><summary>[Bib]</summary><div class="citation"><pre>{escape(bib)}</pre><a href="references/{p['id']}.bib" download>Download BibTeX</a></div></details></div>
</li>''')
    if year is not None:
        rows.append('</ul>')
    (bibdir / 'publications.bib').write_text('\n'.join(citations), encoding='utf-8')
    template = (ROOT / 'scripts/homepage.html').read_text(encoding='utf-8')
    (ROOT / 'index.html').write_text(template.replace('<!-- PUBLICATIONS -->', '\n'.join(rows)), encoding='utf-8')
    print(f'Built index.html and {len(papers)} BibTeX entries.')


if __name__ == '__main__':
    build()
