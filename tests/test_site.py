import json
import re
import tempfile
import unittest
from pathlib import Path

from agk.site import broken_links, inject_data

ROWS = [{"id": "XW-001", "theme": "Inventory", "summary": "Keep one </script> safe"}]


class SiteTests(unittest.TestCase):
    def test_injects_json_between_markers(self):
        html = "<body><!--XW-DATA--><!--/XW-DATA--></body>"
        out = inject_data(html, "XW", ROWS)
        data = re.search(r'id="xw-data">(.*?)</script>', out, re.S).group(1)
        self.assertEqual(json.loads(data.replace("<\\/", "</"))[0]["id"], "XW-001")

    def test_injection_is_repeatable(self):
        html = "<!--XW-DATA--><!--/XW-DATA-->"
        once = inject_data(html, "XW", ROWS)
        self.assertEqual(inject_data(once, "XW", ROWS), once)

    def test_names_do_not_collide(self):
        html = "<!--XW-DATA--><!--/XW-DATA--><!--LC-DATA--><!--/LC-DATA-->"
        out = inject_data(inject_data(html, "XW", ROWS), "LC", [{"stage": "plan"}])
        self.assertIn('id="xw-data"', out)
        self.assertIn('id="lc-data"', out)

    def test_escapes_script_close(self):
        out = inject_data("<!--XW-DATA--><!--/XW-DATA-->", "XW", ROWS)
        self.assertEqual(out.count("</script>"), 1)

    def test_missing_markers_raise(self):
        with self.assertRaises(ValueError):
            inject_data("<body></body>", "XW", ROWS)

    def test_broken_relative_link_reported(self):
        d = Path(tempfile.mkdtemp())
        (d / "index.html").write_text('<a href="tools.html">t</a><a href="https://x.com">x</a><a href="#top">t</a>')
        self.assertEqual(broken_links(d), ["index.html: tools.html"])
