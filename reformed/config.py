import os

__all__ = [
    "MAX_BUFFER_SIZE",
    "PORT",
    "WORKERS"
]

# Maximum buffer size for requests, in bytes - mostly useful for controlling file uploads
# Defaults to 25 MiB
MAX_BUFFER_SIZE = int(os.getenv("REFORMED_MAX_BUFFER_SIZE", 25 * (1024 ** 2)))

# Port to accept requests on
PORT = int(os.getenv("REFORMED_PORT", 8000))

# Number of worker processes to start
WORKERS = int(os.getenv("REFORMED_WORKERS", 2))
