import os
import sys

# Ensure repository root (Info) is on sys.path so tests can import the package
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

# Import test helpers early so they can register fake hardware modules
# (e.g. `machine`, `rp2`, `utime`) before other package modules are imported
try:
	# normal package import path used when tests are discovered as
	# `pico_go_programme.Tests.test_...`
	from pico_go_programme.Tests import test_helpers  # noqa: F401
except Exception:
	# fallback when tests are run in a different import context
	from . import test_helpers  # noqa: F401
