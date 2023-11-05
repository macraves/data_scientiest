"""SQL queries for the flight data"""
import os

current_path = os.getcwd()
basename = os.path.basename(current_path)
if basename == "SE_107.0":
    DATABASE_URI = "sqlite:///CodioSkySql/data/flights.sqlite3"
else:
    DATABASE_URI = "sqlite:///data/flights.sqlite3"

QUERY_FLIGHT_BY_ID = """
    SELECT flights.*, 
    airlines.airline, 
    flights.ID as FLIGHT_ID, 
    flights.DEPARTURE_DELAY as DELAY 
    FROM flights 
    JOIN airlines ON flights.airline = airlines.id 
    WHERE flights.ID = :id"""

QUERY_FLIGHT_BY_DATES = (
    "SELECT "
    "f.YEAR, f.MONTH, f.DAY, "
    "f.FLIGHT_NUMBER as [flight number], "
    "a.AIRLINE, "
    "f.TAIL_NUMBER as [tail number], "
    "f.ORIGIN_AIRPORT as origin, "
    "f.DESTINATION_AIRPORT as destination, "
    "f.SCHEDULED_DEPARTURE as departure, "
    "f.SCHEDULED_ARRIVAL as arrival "
    "FROM "
    "flights as f JOIN airlines as a "
    "ON f.AIRLINE = a.ID "
    "WHERE f.YEAR = :year AND f.MONTH = :month AND f.DAY = :day "
)
DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT
	al.ID, f.ORIGIN_AIRPORT as origin,
	al.AIRLINE,
	f.ARRIVAL_DELAY + f.DEPARTURE_DELAY as delay
FROM flights as f
JOIN airlines as al
ON f.AIRLINE = al.ID
WHERE al.AIRLINE = :airline AND delay > 1
ORDER BY delay;"""

DELAYED_FLIGHTS_BY_ORIGIN = """
SELECT 
	f.ID,
	f.ORIGIN_AIRPORT as airport,
	al.AIRLINE,
	f.DEPARTURE_DELAY as DELAY
FROM flights as f
JOIN airlines as al
ON f.AIRLINE = al.ID
WHERE airport = :origin AND (DELAY > 1 AND (DELAY IS NOT NULL AND DELAY != ''))
ORDER BY DELAY;"""

DELAYED_AIRLINE_FLIGHTS_BY_DATE = """
    SELECT
        f.ID,
        a.AIRLINE,
        f.DEPARTURE_DELAY as departure,
        f.ARRIVAL_DELAY as arrival
        f.DEPARTURE_DELAY + f.ARRIVAL_DELAY as delay
    FROM flights as f
    JOIN airlines as a
    ON f.AIRLINE = a.ID
    WHERE delay > 1
    AND (f.YEAR = :year AND f.MONTH = :month AND f.DAY = :day)
    Order by delay DESC;"""

PRINT_RESULTS = """
    SELECT
	f.ID as FLIGHT_ID, 
	f.ORIGIN_AIRPORT,
	f.DESTINATION_AIRPORT,
	al.AIRLINE,
	f.ARRIVAL_DELAY + f.DEPARTURE_DELAY as DELAY
FROM flights as f
JOIN airlines as al
ON f.AIRLINE = al.ID
WHERE DELAY > 1 -- IF MORE THAN ONE MINUTE DELAYED
ORDER BY DELAY;"""

TOTAL_DELAYED_FLIGHTS_OF_ALL_AIRLINES_BY_ALL_ORIGINS = """
SELECT
	--fl.ID,
	fl.ORIGIN_AIRPORT as ORIGIN,
	al.AIRLINE,
	fl.DEPARTURE_DELAY + fl. ARRIVAL_DELAY  as DELAY
FROM flights as fl
JOIN airports as ar
ON fl.ORIGIN_AIRPORT = ar.IATA_CODE
JOIN airlines as al
ON fl.AIRLINE = al.ID
WHERE DELAY > 1 -- IF MORE THAN ONE MINUTE DELAYED
GROUP BY al.AIRLINE, ORIGIN
ORDER by ORIGIN;"""


AIRLINES_TOTAL_DELAYS_AND_FLIGHTS = """
SELECT 
    al.AIRLINE,
    SUM(CASE 
        WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY 
        ELSE 0 
    END + 
    CASE 
        WHEN f.ARRIVAL_DELAY > 0 THEN f.ARRIVAL_DELAY 
        ELSE 0 
    END) as total_delay_minutes,
    COUNT(*) as total_flights
FROM flights as f
JOIN airlines as al
ON f.AIRLINE = al.ID
GROUP BY al.AIRLINE
HAVING total_delay_minutes > 2
"""

PERCENTAGE_OF_DELAYED_FLIGHT_PER_HOUR_OF_THE_DAY = """
SELECT
	f.SCHEDULED_DEPARTURE as hours,
	count(*) as total_flights,
	cast(sum(case when f.DEPARTURE_DELAY > 0 then f.DEPARTURE_DELAY else 0 end)as INTEGER) as total_delay
FROM flights as f
GROUP BY hours
ORDER BY hours;"""

ORIGIN_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_AND_ARRIVAL_DELAYS = """
SELECT
	f.ORIGIN_AIRPORT as origin, 
	f.DESTINATION_AIRPORT as destination,
	COUNT(*) as total_flights,
	SUM(CASE WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY ELSE 0 END) as departure_delays,
	SUM(CASE WHEN f.ARRIVAL_DELAY >0 THEN f.ARRIVAL_DELAY ELSE 0 END) as arrival_delays
FROM flights as f
GROUP BY origin,destination;"""
