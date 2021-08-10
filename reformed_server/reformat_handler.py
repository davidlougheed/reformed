import asyncio
import os
import pathlib
import tempfile
import zipfile

from itertools import chain
from tornado.web import RequestHandler
from typing import Any, Coroutine, List, Optional, Union

from .pandoc_spec import INPUT_FORMATS, OUTPUT_FORMATS

__all__ = ["ReformatHandler"]

CHUNK_SIZE = 16 * 1024
DOCUMENT_KEY = "document"

BUNDLE_PATH = "./bundle.zip"
IN_FILE_PATH = "./pandoc-input"
OUT_FILE_PATH = "./pandoc-output"


def _get_arg(body: dict, key: str) -> Optional[Union[str, List[str]]]:
    v = body.get(key, [])
    if not v:
        return None
    elif len(v) == 1:
        v = v[0].strip()
        return v or None
    else:
        return v


def run_pandoc(to_format, from_format, body) -> Coroutine[Any, Any, asyncio.subprocess.Process]:
    def bool_flag(f: str) -> tuple:
        return (f"--{f}",) if _get_arg(body, f) else ()

    def choices_flag(f: str, *options) -> tuple:
        v = _get_arg(body, f)
        return (f"--{f}={v}",) if v in options else ()

    def int_flag(f: str, min_: int, max_: int) -> tuple:
        sv = _get_arg(body, f)
        try:
            pv = min(max(int(sv), min_), max_)
            return f"--{f}={pv}",  # Leave the trailing comma
        except (TypeError, ValueError):  # Blank, None, or other non-int
            return ()

    return asyncio.create_subprocess_exec(
        "pandoc",

        # General options
        #  - System-set flags
        "--pdf-engine=xelatex",  # Use xelatex to allow for Unicode characters in input
        "--extract-media=.",
        #  - User-set flags
        *chain.from_iterable(map(bool_flag, (
            "ascii",
            "no-highlight",
            "html-q-tags",
            "incremental",
            "listings",
            "preserve-tabs",
            "reference-links",
            "section-divs",
            "standalone",
            "strip-comments",
            "toc",
        ))),
        *int_flag("columns", 1, 300),
        *int_flag("dpi", 36, 600),
        *int_flag("toc-depth", 1, 6),
        *choices_flag("eol", "crlf", "lf", "native"),
        *choices_flag("markdown-headings", "atx", "setext"),
        *choices_flag("reference-location", "block", "section", "document"),
        *choices_flag("top-level-division", "default", "section", "chapter", "part"),
        *choices_flag("track-changes", "accept", "reject", "all"),
        *choices_flag("wrap", "auto", "none", "preserve"),

        # Input-related options
        IN_FILE_PATH,
        "-f", from_format,
        "-t", to_format,
        "-o", OUT_FILE_PATH,

        stderr=asyncio.subprocess.PIPE)


def prepare_zip_bundle(out_name: str):
    media_path = pathlib.Path("media")
    media_contents = os.listdir(media_path) if os.path.isdir(media_path) else []

    with zipfile.ZipFile(BUNDLE_PATH, mode="w") as zf:
        zf.write(OUT_FILE_PATH, out_name)
        for mp in media_contents:
            zf.write(media_path / mp, f"media/{mp}")


# Tornado's type hinting stuff is messed up
# noinspection PyAbstractClass
class ReformatHandler(RequestHandler):
    def write_error(self, status_code: int, **kwargs: dict) -> None:
        message = kwargs.get("message", "")
        self.write({"code": status_code, **({"error": message} if message else {})})

    async def post(self, from_format: str, to_format: str):
        # Handle input errors first

        if from_format not in INPUT_FORMATS:
            self.send_error(400, message=f"invalid input format: {from_format}")
            return

        if to_format not in OUTPUT_FORMATS:
            self.send_error(400, message=f"invalid output format: {to_format}")
            return

        # TODO: py3.9: use walrus
        num_files = len(self.request.files.get(DOCUMENT_KEY, ()))
        if num_files != 1:
            self.send_error(400, message=f"exactly 1 document must be passed (got {num_files})")
            return

        body = self.request.body_arguments or {}

        # Parameters look good to go, so create a temporary directory to do
        # some work in - time to convert the document!

        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)  # Need this to be the working directory or it'll break media links in the output

            in_file = self.request.files[DOCUMENT_KEY][0]

            # Write the POSTed body to the file system, using a non-user-passed
            # file name to prevent anything malicious or annoying.

            with open(IN_FILE_PATH, "wb") as fh:
                fh.write(in_file["body"])

            # Run Pandoc on the input
            res = await run_pandoc(to_format, from_format, body)
            _, stderr = await res.communicate()

            # - If Pandoc hit an error, return the error text (if present) to the requester
            if res.returncode != 0:
                self.send_error(500, message=f"pandoc exited with a non-0 status code ({res.returncode})" +
                                             (f": {stderr.decode()}" if stderr else ""))
                return

            # If everything went smoothly, return a file response in the desired format
            # unless any media were extracted, in which case return a zip bundle with the
            # file (using our name, not theirs) and the media folder.

            def send_in_chunks(fp):
                self.set_header("Content-Length", str(os.path.getsize(fp)))

                with open(fp, "rb") as cfh:
                    # Read the file in chunks to prevent exploding our memory
                    while True:  # TODO: py3.9: walrus operator
                        data = cfh.read(CHUNK_SIZE)
                        if not data:
                            break
                        self.write(data)

            # Output mime type and file extension
            out_mime_type, out_file_ext, _ = OUTPUT_FORMATS[to_format]

            new_name = f"{os.path.splitext(in_file['filename'])[0]}.{out_file_ext}"
            send_as_bundle = _get_arg(body, "bundle")

            if send_as_bundle:
                # Prepare a .zip archive with the document output + media files (if present)
                prepare_zip_bundle(new_name)

            # These headers force the file to not get rendered in-browser,
            # since some Pandoc output formats are renderable either as plain
            # text or actually will be viewable (e.g. html)
            # Manually setting the Content-Length header lets users see how big
            # the file they're downloading is.
            # After this, send the bytes of the document.
            name_to_send = "bundle.zip" if send_as_bundle else new_name
            self.set_header("Content-Disposition", f"attachment; filename=\"{name_to_send}\"")
            self.set_header("Content-Type", "application/zip" if send_as_bundle else out_mime_type)
            send_in_chunks(BUNDLE_PATH if send_as_bundle else OUT_FILE_PATH)
