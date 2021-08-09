from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.routing import PathMatches, Rule, RuleRouter
from tornado.web import Application

from .format_list_handler import FormatListHandler
from .reformat_handler import ReformatHandler

from .config import MAX_BUFFER_SIZE, PORT, WORKERS

API_V1 = "/api/v1"


def make_api_v1_app() -> Application:
    return Application(list(map(lambda r: (API_V1 + r[0], r[1]), (
        (r"/formats", FormatListHandler),
        (r"/from/(\w+)/to/(\w+)", ReformatHandler),
    ))))


def main():
    router = RuleRouter([
        Rule(PathMatches(rf"{API_V1}.*"), make_api_v1_app()),
    ])

    server = HTTPServer(router, max_buffer_size=MAX_BUFFER_SIZE)
    server.bind(PORT)
    print(f"reformed listening on {PORT}; workers={WORKERS}")
    server.start(WORKERS)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
