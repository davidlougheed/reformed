import asyncio
import os
import pathlib
import tempfile

from tornado.web import RequestHandler
from typing import List, Optional, Union

from .pandoc_spec import INPUT_FORMATS, OUTPUT_FORMATS

__all__ = ["ReformatHandler"]

CHUNK_SIZE = 16 * 1024
DOCUMENT_KEY = "document"


def _get_arg(body: dict, key: str) -> Optional[Union[str, List[str]]]:
    v = body.get(key, [])
    if not v:
        return None
    elif len(v) == 1:
        v = v[0].strip()
        return v or None
    else:
        return v


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
            self.send_error(400, message=f"invalid input format: {to_format}")
            return

        # TODO: py3.9: use walrus
        num_files = len(self.request.files.get(DOCUMENT_KEY, ()))
        if num_files != 1:
            self.send_error(400, message=f"exactly 1 document must be passed (got {num_files})")
            return

        body = self.request.body_arguments or {}

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

        # Parameters look good to go, so create a temporary directory to do
        # some work in - time to convert the document!

        with tempfile.TemporaryDirectory() as td:
            input_file = self.request.files[DOCUMENT_KEY][0]

            temp_in_file = pathlib.Path(td) / "pandoc-input"
            temp_out_file = pathlib.Path(td) / "pandoc-output"

            # Write the POSTed body to the file system, using a non-user-passed
            # file name to prevent anything malicious or annoying.

            with open(temp_in_file, "wb") as fh:
                fh.write(input_file["body"])

            # Run Pandoc on the input

            res = await asyncio.create_subprocess_exec(
                "pandoc",

                # General options
                "--pdf-engine=xelatex",  # Use xelatex to allow for Unicode characters in input
                *bool_flag("ascii"),
                *bool_flag("no-highlight"),
                *int_flag("columns", 1, 300),
                *int_flag("dpi", 36, 600),
                *choices_flag("eol", "crlf", "lf", "native"),
                *bool_flag("html-q-tags"),
                *bool_flag("incremental"),
                *bool_flag("listings"),
                *choices_flag("markdown-headings", "atx", "setext"),
                *bool_flag("preserve-tabs"),
                *bool_flag("reference-links"),
                *choices_flag("reference-location", "block", "section", "document"),
                *bool_flag("section-divs"),
                *bool_flag("standalone"),
                *bool_flag("strip-comments"),
                *bool_flag("toc"),
                *int_flag("toc-depth", 1, 6),
                *choices_flag("top-level-division", "default", "section", "chapter", "part"),
                *choices_flag("track-changes", "accept", "reject", "all"),
                *choices_flag("wrap", "auto", "none", "preserve"),

                # Input-related options
                str(temp_in_file),
                "-f", from_format,
                "-t", to_format,
                "-o", str(temp_out_file),

                stderr=asyncio.subprocess.PIPE)

            _, stderr = await res.communicate()

            # If Pandoc hit an error, return the error text (if present) to the requester
            if res.returncode != 0:
                self.send_error(500, message=f"pandoc exited with a non-0 status code ({res.returncode})" +
                                             (f": {stderr.decode()}" if stderr else ""))
                return

            # If everything went smoothly, return a file response in the desired format

            mime_type, file_ext, _ = OUTPUT_FORMATS[to_format]
            new_name = f"{os.path.splitext(input_file['filename'])[0]}.{file_ext}"

            # These headers force the file to not get rendered in-browser,
            # since some Pandoc output formats are renderable either as plain
            # text or actually will be viewable (e.g. html)
            # Manually setting the Content-Length header lets users see how big
            # the file they're downloading is.
            self.set_header("Content-Disposition", f"attachment; filename=\"{new_name}\"")
            self.set_header("Content-Length", str(os.path.getsize(temp_out_file)))
            self.set_header("Content-Type", mime_type)

            with open(temp_out_file, "rb") as fh:
                # Read the file in chunks to prevent exploding our memory
                while True:
                    data = fh.read(CHUNK_SIZE)
                    if not data:
                        break
                    self.write(data)
