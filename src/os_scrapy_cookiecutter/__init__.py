import os
import pkgutil

__version__ = pkgutil.get_data(__package__, "VERSION").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split("."))

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
del os
del pkgutil
