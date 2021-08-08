from tornado.web import RequestHandler

from .pandoc_spec import INPUT_FORMATS, OUTPUT_FORMATS

__all__ = ["FormatListHandler"]


# Tornado's type hinting stuff is messed up
# noinspection PyAbstractClass
class FormatListHandler(RequestHandler):
    @staticmethod
    def _formmatted_formats(formats: dict):
        return {k: {"mime": v[0], "ext": v[1], "detail": v[2]} for k, v in formats.items()}

    async def get(self):
        """
        Returns a JSON response with an object containing the input and output
        formats available for reformatting via the API.
        """
        return self.finish({
            "input": self._formmatted_formats(INPUT_FORMATS),
            "output": self._formmatted_formats(OUTPUT_FORMATS),
        })
