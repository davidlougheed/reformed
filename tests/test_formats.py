import json

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from reformed_server.server import API_V1, make_api_v1_app


from reformed_server.pandoc_spec import INPUT_FORMATS, OUTPUT_FORMATS


class FormatListTests(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        return make_api_v1_app()

    def test_formats(self):
        r = self.fetch(f"{API_V1}/formats")
        self.assertEqual(r.code, 200)
        d = json.loads(r.body)

        self.assertIn("input", d)
        self.assertIn("output", d)

        self.assertEqual(len(d["input"]), len(INPUT_FORMATS))
        self.assertEqual(len(d["output"]), len(OUTPUT_FORMATS))
