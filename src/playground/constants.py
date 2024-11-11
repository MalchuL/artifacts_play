import os.path
from rootutils import rootutils

SKILL_MAX_LEVEL = 40
CHARACTER_MAX_LEVEL = 40
MAX_FIGHTS_LENGTH = 50
TURN_COOLDOWN = 2

MAX_UTILITIES_EQUIPPED = 100

ROOT_FOLDER = rootutils.find_root(search_from=__file__, indicator=".project-root")
CACHE_FOLDER = os.path.join(ROOT_FOLDER, ".artifacts_cache")
