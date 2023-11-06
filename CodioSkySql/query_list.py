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

LOCATION_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_DELAYS = """
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
HAVING total_delays > 60 -- filters more than 10 minutes delays
ORDER BY origin, destination --total_delays;"""


LOCATION_DESTINATION_TOTAL_FLIGHTS = """
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
HAVING total_delays > 10
ORDER BY origin, destination;"""

"""ATL	33.64044	-84.42694	775	7410.0	AUS	30.19453	-97.66987"""
