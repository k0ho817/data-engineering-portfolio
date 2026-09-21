"""Check static references, tab wiring and displayed SQL provenance."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

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


page = Page()
page.feed((ROOT / "index.html").read_text())
assert len(page.ids) == len(set(page.ids)), "Duplicate HTML IDs"
for ref in page.refs:
    url = urlsplit(ref)
    if url.scheme or url.netloc:
        continue
    if url.path:
        assert (ROOT / unquote(url.path)).is_file(), ref
    elif url.fragment:
        assert url.fragment in page.ids, ref
assert len(page.tabs) == 3
assert sum(t["aria-selected"] == "true" for t in page.tabs) == 1
for tab in page.tabs:
    assert tab["aria-controls"] in page.ids
schema = (ROOT / "pipeline/schema.sql").read_text()
assert len(page.codes) == 2
for sql in page.codes:
    assert sql.strip() in schema, "Displayed SQL differs from source"
print("PASS: local links, anchors, tab IDs and SQL source excerpts")
