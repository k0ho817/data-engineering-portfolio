"""Check local references, IDs, tabs and displayed SQL provenance."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.tabs = []
        self.codes = []
        self.in_code = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.refs.append(attrs[key])
        if attrs.get("role") == "tab":
            self.tabs.append(attrs)
        if tag == "code":
            self.in_code = True
            self.codes.append("")

    def handle_endtag(self, tag):
        if tag == "code":
            self.in_code = False

    def handle_data(self, data):
        if self.in_code:
            self.codes[-1] += data


pages = {}
for path in sorted(ROOT.rglob("*.html")):
    page = Page()
    page.feed(path.read_text())
    pages[path.resolve()] = page
    assert len(page.ids) == len(set(page.ids)), f"Duplicate IDs: {path}"

for path, page in pages.items():
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path or path.name)).resolve()
        assert target.is_file(), f"Missing {ref} in {path.relative_to(ROOT)}"
        if url.fragment and target.suffix == ".html":
            assert url.fragment in pages[target].ids, f"Missing #{url.fragment} in {target}"

sql_page = pages[(ROOT / "projects/sql.html").resolve()]
assert len(sql_page.tabs) == 3
assert sum(tab["aria-selected"] == "true" for tab in sql_page.tabs) == 1
for tab in sql_page.tabs:
    assert tab["aria-controls"] in sql_page.ids

schema = (ROOT / "pipeline/schema.sql").read_text()
for sql in sql_page.codes:
    if "CREATE " in sql:
        assert sql.strip() in schema, "Displayed SQL differs from pipeline/schema.sql"

print(f"PASS: {len(pages)} pages, local links, anchors, tabs and SQL excerpts")
