import asyncio
import os
import pathlib
import tempfile

from tornado.web import RequestHandler

from .pandoc_spec import INPUT_FORMATS, OUTPUT_FORMATS

__all__ = ["ReformatHandler"]

CHUNK_SIZE = 16 * 1024
DOCUMENT_KEY = "document"


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

        # Parameters look good to go, so create a temporary directory to do
        # some work in - time to convert the document!

        with tempfile.TemporaryDirectory() as td:
            input_file = self.request.files[DOCUMENT_KEY][0]

            # Write the POSTed body to the file system, using a non-user-passed
            # file name to prevent anything malicious or annoying.
            temp_in_file = pathlib.Path(td) / "pandoc-input"
            with open(temp_in_file, "wb") as fh:
                fh.write(input_file["body"])

            # Run Pandoc on the input
            temp_out_file = pathlib.Path(td) / "pandoc-output"
            res = await asyncio.create_subprocess_exec(
                "pandoc",
                "--pdf-engine=xelatex",  # Use xelatex to allow for Unicode characters in input
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
