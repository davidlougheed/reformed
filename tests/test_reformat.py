import pathlib
# Tornado is annoying and doesn't encode form data for us, so we use requests just in testing
import requests

from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from reformed_server.server import API_V1, make_api_v1_app

DOCX_FILE = pathlib.Path(__file__).parent.resolve() / "documents/test1.docx"


class ReformatTests(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        return make_api_v1_app()

    def test_invalid_input_format_1(self):
        r = self.fetch(f"{API_V1}/from/bad/to/pdf", method="POST", body=b"")
        self.assertEqual(r.code, 400)
        self.assertIn(b"invalid input", r.body)

    def test_invalid_input_format_2(self):
        r = self.fetch(f"{API_V1}/from/pdf/to/docx", method="POST", body=b"")
        self.assertEqual(r.code, 400)
        self.assertIn(b"invalid input", r.body)

    def test_invalid_output_format(self):
        r = self.fetch(f"{API_V1}/from/docx/to/bad", method="POST", body=b"")
        self.assertEqual(r.code, 400)
        self.assertIn(b"invalid output", r.body)

    @gen_test
    def test_no_file_provided(self):
        # The request isn't actually fired, we just hijack it to get the body
        b = requests.Request("POST", "http://example.org/", data={"bundle": "true"}, files={}).prepare()
        r = yield self.http_client.fetch(
            self.get_url(f"{API_V1}/from/docx/to/html"),
            method="POST",
            body=b.body,
            headers=b.headers,
            raise_error=False)
        self.assertEqual(r.code, 400)
        self.assertIn(b"(got 0)", r.body)

    @gen_test(timeout=15)
    def test_docx_to_pdf(self):
        with open(DOCX_FILE, "rb") as df:
            # The request isn't actually fired, we just hijack it to get the body
            b = requests.Request("POST", "http://example.org/", files=(
                ("document", ("document", df)),
            )).prepare()

            r = yield self.http_client.fetch(
                self.get_url(f"{API_V1}/from/docx/to/pdf"),
                method="POST",
                body=b.body,
                headers=b.headers)
            self.assertEqual(r.code, 200)
            self.assertEqual(r.headers["Content-Type"], "application/pdf")

    @gen_test
    def test_docx_to_html(self):
        with open(DOCX_FILE, "rb") as df:
            # The request isn't actually fired, we just hijack it to get the body
            b = requests.Request("POST", "http://example.org/", data={"bundle": "true"}, files=(
                ("document", ("document", df)),
            )).prepare()

            r = yield self.http_client.fetch(
                self.get_url(f"{API_V1}/from/docx/to/html"),
                method="POST",
                body=b.body,
                headers=b.headers)
            self.assertEqual(r.code, 200)
            self.assertEqual(r.headers["Content-Type"], "application/zip")
            # TODO: inspect zip
