import os
from base import *

ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT")

if ENVIRONMENT == "live":
    from live import *
elif ENVIRONMENT == "staging":
    from staging import *

try:
    from local import *
except ImportError:
    pass

