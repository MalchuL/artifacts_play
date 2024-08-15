import logging
import os

logging.basicConfig(level=logging.INFO)

# Set for dynaconf
os.environ["ENV_FOR_DYNACONF"] = "testing"
