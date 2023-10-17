# Backend Logging

Logging is done with the Python standard library `logging` module.  The
`logger.py` file defines a configuration for the root logger that should be
used, so instead of doing `logger = logging.getLogger(__name__)`, just use the
`logging.root` logger.
