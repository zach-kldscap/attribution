DROP TABLE IF EXISTS kinematika_eod;

CREATE TABLE kinematika_eod AS
SELECT date(timestamp) as dt, fund, model, hs, asset, ct_bb, broker, cur, exchange, istoday, exec_price, position, mult, px_enter, px_mark, fx_last, pnl, PX_LAST FROM kinematika
WHERE timestamp in (
      SELECT MAX(timestamp) FROM kinematika
      GROUP BY DATE(timestamp)
);

CREATE INDEX idx_dt
ON kinematika_eod(dt);
