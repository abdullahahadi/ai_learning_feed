import logging


def configure_logging() -> None:
    """Enable informational progress messages for command-line entry points."""
    logging.basicConfig(level=logging.INFO)
