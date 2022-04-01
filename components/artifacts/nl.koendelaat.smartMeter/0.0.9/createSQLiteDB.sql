PRAGMA journal_mode=WAL;

CREATE Table TempData (
    LastUpdate datetime NOT NULL
);

CREATE Table Consumption (
	TimeStamp datetime NOT NULL,
	ETotal int(8) NOT NULL,
	PRIMARY KEY (TimeStamp)
);

CREATE VIEW vwConsumptionPower AS
select datetime(h.TimeStamp, 'unixepoch', 'localtime') TS, h.TimeStamp, (h.ETotal-hprev.ETotal)*3600 / (h.TimeStamp-hprev.TimeStamp) as PowerUsed
from (select h.*,
             (select h2.TimeStamp
              from Consumption h2
              where h2.TimeStamp < h.TimeStamp
              order by h2.TimeStamp desc
              limit 1
             ) as prev_Consumption
      from Consumption h
     ) h join
     Consumption hprev
     on hprev.TimeStamp = h.prev_Consumption;

CREATE VIEW vwConsumption AS
SELECT datetime(TimeStamp, 'unixepoch', 'localtime') TimeStamp,
	datetime(CASE WHEN (TimeStamp % 300) < 150
	THEN TimeStamp - (TimeStamp % 300)
	ELSE TimeStamp - (TimeStamp % 300) + 300
	END, 'unixepoch', 'localtime') AS Nearest5min,
	PowerUsed
	FROM vwConsumptionPower;

CREATE VIEW vwAvgConsumption AS
	SELECT Timestamp,
		Nearest5min,
		avg(PowerUsed) As PowerUsed
	FROM vwConsumption
	GROUP BY Nearest5Min;