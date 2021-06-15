# config.py
# Zach Dingels - 2.2021
# ------------------------------------------------------------------------------
# Syncs the local version of kinematika with the databases
# ------------------------------------------------------------------------------
import argparse
import datetime
import logging
import sqlite3

import pandas as pd

import attribution as at
# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
logger = logging.getLogger("attribution")


def _table_exists(name):
    with at.DB.LOCAL() as con:
        res = con.execute("SELECT count(*) FROM sqlite_master WHERE name=?", [name])
        return bool(res.fetchone()[0])

# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------
def sync(date):
    date_str = date.strftime("%Y-%m-%d")
    next_date_str = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    logger.info("Syncing %s", date_str)


    # Pull IDs from both datasets
    with at.DB.MERCURY() as con:
        Q = f"""
        SELECT id FROM kldspos.kinematika
        WHERE timestamp >= '{date_str}'
        AND   timestamp  < '{next_date_str}'
        """
        remote_ids = set(str(ID) for ID, in con.execute(Q).fetchall())

    local_ids = set()
    if _table_exists("kinematika"):
        with at.DB.LOCAL() as con:
                Q = f"""
                SELECT id FROM kinematika
                WHERE timestamp >= '{date_str}'
                AND   timestamp  < '{next_date_str}'
                """
                local_ids = set(str(ID) for ID, in con.execute(Q).fetchall())

    # Finding missing IDS from local
    missing_ids = remote_ids - local_ids
    if missing_ids:
        logger.info("Found %s missing rows. Pulling...", len(missing_ids))
        missing_ids_str = ",".join(missing_ids)

        # Pull data for missing IDs from remote
        Q = f"""
        SELECT id, timestamp, fund, model, hs, asset, ct_bb, broker, cur, exchange, istoday, exec_price, position, mult, px_enter, px_mark, fx_last, pnl, PX_LAST FROM kldspos.kinematika
        WHERE id in ({missing_ids_str});
        """
        df = pd.read_sql(Q, at.DB.MERCURY())
        
        # Add data for missing IDS to local
        df.to_sql("kinematika", at.DB.LOCAL(), if_exists="append", chunksize=1000, method="multi")
    logger.info("Done!")

    
    
    
