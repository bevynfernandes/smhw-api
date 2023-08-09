import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "smhw-api"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from loguru import logger

logger.remove(0)
__logid = logger.add(sys.stderr, level="INFO")

from .api import *
from . import exceptions
from . import objects


def set_debug(state: bool):
    """
    The function sets the debug state and updates the logger accordingly.

    Args:
        state (bool): state is a boolean parameter that determines whether debug log is turned on or off.
    If state is True, debug log is turned on and if it is False, debug log is turned off.
    """
    global __logid
    logger.remove(__logid)
    if state:
        __logid = logger.add(sys.stderr, level="DEBUG")
    else:
        __logid = logger.add(sys.stderr, level="INFO")
    logger.debug(f"Debug set to: {state=}")
