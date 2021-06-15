# ------------------------------------------------------------------------------
# app.py
# Zach Dingels 6.2021
# ------------------------------------------------------------------------------
# A REST API for attribution
# ------------------------------------------------------------------------------
import datetime
from flask import Flask, Response, request
import io
import pandas as pd
import urllib

import attribution as at

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------
app = Flask(__name__)

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------------------
@app.route("/kinematika/eod")
def kinematika_eod():
    # Parse args
    start = request.args.get('start', '20210101')
    end   = request.args.get('end',   '20210601')

    start = datetime.datetime.strptime(start, "%Y%m%d")
    end   = datetime.datetime.strptime(end,   "%Y%m%d")
    
    # Collect data
    df = pd.read_sql(
        """
        SELECT * FROM kinematika_eod
        WHERE dt >= ?
        AND   dt <= ?
        """,
        at.DB.LOCAL(),
        params = [start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")]
    )
    
    # Convert to string
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    
    # Return 
    return Response(
        buf.getvalue(),
        mimetype="text/csv"
    )

@app.route("/test/<x>")
def test(x):
    # Collect data
    df = pd.read_sql(
        f"select * from kinematika order by timestamp desc limit {x}",
        at.DB.LOCAL()
    )
    df = df.drop(columns=['index'])
    
    # Convert to string
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    
    # Return 
    return Response(
        buf.getvalue(),
        mimetype="text/csv"
    )




        
