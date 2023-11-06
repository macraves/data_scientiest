"""SQL queries for the flight data"""
import os

current_path = os.getcwd()
basename = os.path.basename(current_path)
if basename == "SE_107.0":
    DATABASE_URI = "sqlite:///CodioSkySql/data/flights.sqlite3"
else:
    DATABASE_URI = "sqlite:///data/flights.sqlite3"

DELAY = 20

QUERY_FLIGHT_BY_ID = """
SELECT 
	ar.AIRLINE as airline,
	f.*  
FROM flights as f
JOIN airlines as ar
ON f.airline = ar.id 
WHERE f.ID = :id;"""

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
DELAYED_FLIGHTS_BY_AIRLINE = f"""
SELECT
	al.ID, f.ORIGIN_AIRPORT as origin,
	al.AIRLINE,
	f.DEPARTURE_DELAY as delay
FROM flights as f
JOIN airlines as al
ON f.AIRLINE = al.ID
WHERE al.AIRLINE = :airline AND delay > {DELAY}
ORDER BY delay;"""

DELAYED_FLIGHTS_BY_ORIGIN = f"""
SELECT 
	f.ID,
	f.ORIGIN_AIRPORT as airport,
	al.AIRLINE,
	f.DEPARTURE_DELAY as DELAY
FROM flights as f
JOIN airlines as al
ON f.AIRLINE = al.ID
WHERE airport = :origin AND (DELAY > {DELAY} AND (DELAY IS NOT NULL AND DELAY != ''))
ORDER BY DELAY;"""

DELAYED_AIRLINE_FLIGHTS_BY_DATE = f"""
    SELECT
        f.ID,
        a.AIRLINE,
        f.DEPARTURE_DELAY as departure,
        f.ARRIVAL_DELAY as arrival
        f.DEPARTURE_DELAY as delay
    FROM flights as f
    JOIN airlines as a
    ON f.AIRLINE = a.ID
    WHERE delay > {DELAY}
    AND (f.YEAR = :year AND f.MONTH = :month AND f.DAY = :day)
    Order by delay DESC;"""


TOTAL_DELAYED_FLIGHTS_OF_ALL_AIRLINES_BY_ALL_ORIGINS = f"""
SELECT
	--fl.ID,
	fl.ORIGIN_AIRPORT as ORIGIN,
	al.AIRLINE,
	fl.DEPARTURE_DELAY as DELAY
FROM flights as fl
JOIN airports as ar
ON fl.ORIGIN_AIRPORT = ar.IATA_CODE
JOIN airlines as al
ON fl.AIRLINE = al.ID
WHERE DELAY > {DELAY}
GROUP BY al.AIRLINE, ORIGIN
ORDER by ORIGIN;"""


AIRLINES_TOTAL_DELAYS_AND_FLIGHTS = f"""
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
HAVING total_delay_minutes > {DELAY}
"""

PERCENTAGE_OF_DELAYED_FLIGHT_PER_HOUR_OF_THE_DAY = f"""
SELECT
	f.SCHEDULED_DEPARTURE as hours,
	count(*) as total_flights,
	cast(sum(case when f.DEPARTURE_DELAY > 0 then f.DEPARTURE_DELAY else 0 end)as INTEGER) as total_delay
FROM flights as f
GROUP BY hours
HAVING total_delay > {DELAY}
ORDER BY hours;"""

ORIGIN_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_AND_ARRIVAL_DELAYS = f"""
SELECT
	f.ORIGIN_AIRPORT as origin, 
	f.DESTINATION_AIRPORT as destination,
	COUNT(*) as total_flights,
	SUM(CASE WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY ELSE 0 END) as departure_delays,
	SUM(CASE WHEN f.ARRIVAL_DELAY >0 THEN f.ARRIVAL_DELAY ELSE 0 END) as arrival_delays
FROM flights as f
GROUP BY origin,destination
HAVING departure_delays > {DELAY} OR arrival_delays > {DELAY};"""

LOCATION_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_DELAYS = f"""
SELECT
	f.ORIGIN_AIRPORT as origin,
	ar.LATITUDE as origin_lat,
	ar.LONGITUDE as origin_long,
	count(*) as total_flights,
	sum(case WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY ELSE 0 END) as total_delays,
	f.DESTINATION_AIRPORT as destination,
	air.LATITUDE as destination_lat,
	air.LONGITUDE as destination_long
FROM
	flights as f
JOIN airports as ar
ON f.ORIGIN_AIRPORT = ar.IATA_CODE
JOIN airports as air
ON f.DESTINATION_AIRPORT = air.IATA_CODE
WHERE f.ORIGIN_AIRPORT = :origin
GROUP BY origin, destination
HAVING total_delays > {DELAY}
ORDER BY origin, destination --total_delays;"""


LOCATION_DESTINATION_TOTAL_FLIGHTS = f"""
SELECT
    f.ORIGIN_AIRPORT as origin,
    ar.LATITUDE,
    ar.LONGITUDE,
    f.DESTINATION_AIRPORT as destination,
    (SELECT LATITUDE FROM airports WHERE IATA_CODE = f.DESTINATION_AIRPORT) as destination_lat,
    (SELECT LONGITUDE FROM airports WHERE IATA_CODE = f.DESTINATION_AIRPORT) as destination_long,
    count(*) as total_flights,
    sum(case WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY ELSE 0 END) as total_delays
FROM
    flights as f
JOIN airports as ar
ON f.ORIGIN_AIRPORT = ar.IATA_CODE
GROUP BY origin, destination, destination_lat, destination_long
HAVING total_delays > {DELAY}
ORDER BY origin, destination;"""
