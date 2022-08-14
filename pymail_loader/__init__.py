import logging

import importlib_metadata

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# importlib_metadata is necessary here for backwards compat with mkdocs.
version = importlib_metadata.version("pymail_loader")  # type: ignore [attr-defined]


__all__ = ["version"]
