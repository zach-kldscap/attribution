# config.py
# Zach Dingels - 2.2021
# ------------------------------------------------------------------------------
# Command line tool to sync the kinematika DB
# ------------------------------------------------------------------------------
import argparse
import datetime
import logging

import pandas as pd

import attribution as at

logger = logging.getLogger("attribution")


def table_exists(name):
    with at.DB.LOCAL() as con:
        res = con.execute("SELECT count(*) FROM sqlite_master WHERE name=?", [name])
        return bool(res.fetchone()[0])


def cmdline_args():
    # Make parser object
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start',
        '-s',
        type=lambda s: datetime.datetime.strptime(s, '%Y%m%d').date(),
        default = None
    )
    parser.add_argument(
        '--end',
        '-e',
        type=lambda s: datetime.datetime.strptime(s, '%Y%m%d').date(),
        default = datetime.datetime.now().date()
    )

    return parser.parse_args()

def main(start, end):
    """Syncs the local database for every day from start to end"""
    if start is None:
        if table_exists("kinematika"):
            # If no time is set use the last date of data we have in the DB
            last_sync = pd.read_sql(
                """SELECT DATE(MAX(timestamp)) as dt FROM kinematika""",
                at.DB.LOCAL()
            ).dt.iloc[0]
            last_sync = datetime.datetime.strptime(last_sync, "%Y-%m-%d").date()
            start = start or last_sync
        else:
            start = datetime.date(2017,8,29)

    # Sync from start to end. Do this in chunks because the database is large.
    logger.info(
        "Syncing `kinematika` from %s to %s",
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d")
    )
    cur = start
    while cur <= end:
        at.kinematika.sync(cur)
        cur += datetime.timedelta(days=1)
    

if __name__ == "__main__":
    args = cmdline_args()
    main(args.start, args.end)
