# config.py
# Zach Dingels - 2.2021
# ------------------------------------------------------------------------------
# Constants and globals for the project
# ------------------------------------------------------------------------------
from base64 import b64decode
import logging.config
import pathlib
import yaml
from sqlalchemy import create_engine
import sqlite3

# ------------------------------------------------------------------------------
# PATHS
# ------------------------------------------------------------------------------
class PATHS:
    SRC  = pathlib.Path(__file__).parent.absolute()
    ROOT = SRC.parent.parent
    DATA = ROOT / "data"
    DB   = DATA / "local.db"


# ------------------------------------------------------------------------------
# DB
# ------------------------------------------------------------------------------
class DB:
    # Ping the server before using the connection to make sure it's connected. 
    MERCURY = lambda: create_engine(
        b64decode(b"bXlzcWwrbXlzcWxjb25uZWN0b3I6Ly9tZXJjdXJ5OkV5WExQXmslJU4kKkZeOGJjVVdRQDM1LjE4Ni4xNjIuMTYy").decode("utf8"),
        pool_pre_ping=True
    ).connect()
    LOCAL  = lambda: sqlite3.connect(PATHS.DB)
    

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
# Custom profiling level
PROFILE_LEVELV_NUM = 15
logging.addLevelName(PROFILE_LEVELV_NUM, "PROFILE")
def profile(self, message, *args, **kws):
    if self.isEnabledFor(PROFILE_LEVELV_NUM):
        self._log(PROFILE_LEVELV_NUM, message, args, **kws)
logging.Logger.profile = profile
                    
with open(PATHS.ROOT / 'logging.yaml', 'rt') as file:
    log_config = yaml.safe_load(file.read())
    logging.config.dictConfig(log_config)
    del log_config



