"""Methods for accessing flight data from the database."""

from contextlib import closing
from sqlalchemy import create_engine, text, exc
import query_list as ql


class CrudError(Exception):
    """Crud methods of sql if it is failed result varible can not retrun rows"""

    def __init__(self, message):
        self.message = message


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is created,
    the class forms connection to the sqlite database file, which remains active
    until the object is destroyed.
    """

    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        with closing(self._engine.connect()) as connection:
            try:
                query = text(query)
                results = connection.execute(query, params)
                return results.fetchall()
            except exc.SQLAlchemyError as query_error:
                print("Error executing query: ", query_error)
                return []

    def _crud_queries(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary.
        If an exception was raised, print the error.
        """
        with closing(self._engine.connect()) as connection:
            try:
                query = text(query)
                connection.execute(query, params)
                connection.commit()
            except exc.SQLAlchemyError as crud_error:
                raise CrudError(f"Error executing query: {crud_error}") from crud_error

    def find_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """

        params = {"id": flight_id}
        return self._execute_query(ql.FIND_FLIGHT_BY_ID, params)

    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """

        params = {"id": flight_id}
        return self._execute_query(ql.QUERY_FLIGHT_BY_ID, params)

    def get_flights_by_date(self, date):
        """
        Searches for flights by date.
        If the flight was found, returns a list with a single record.
        """
        year = date.year
        month = date.month
        day = date.day
        params = {"year": year, "month": month, "day": day}
        return self._execute_query(ql.QUERY_FLIGHT_BY_DATES, params)

    def delayed_airline_flights_by_date(self, date):
        """Specifically gets airlines by date"""
        year = date.year
        month = date.month
        day = date.day
        params = {"year": year, "month": month, "day": day}
        return self._execute_query(ql.DELAYED_AIRLINE_FLIGHTS_BY_DATE, params)

    def get_delayed_flights_by_airline(self, airline):
        """
        Searches for delayed flights by airline.
        If the flight was found, returns a list with a single record.
        """
        params = {"airline": airline}
        return self._execute_query(ql.DELAYED_FLIGHTS_BY_AIRLINE, params)

    def get_delayed_flights_by_origin(self, origin):
        """
        Searches for delayed flights by origin.
        If the flight was found, returns a list with a single record.
        """
        params = {"origin": origin}
        return self._execute_query(ql.DELAYED_FLIGHTS_BY_ORIGIN, params)

    def get_total_delayed_flights_of_airline_by_all_origins(self):
        """Method to gets tabloid of total delayed flights of airline by all origins"""
        return self._execute_query(
            ql.TOTAL_DELAYED_FLIGHTS_OF_ALL_AIRLINES_BY_ALL_ORIGINS, {}
        )

    def get_airlines_total_delays_and_flights(self):
        """Method to gets tabloid of total delayed flights of airline by all origins"""
        return self._execute_query(ql.AIRLINES_TOTAL_DELAYS_AND_FLIGHTS, {})

    def get_percentage_delayed_flights_per_hour_of_the_day(self):
        """Method to gets tabloid of total delayed flights of airline by all origins"""
        return self._execute_query(
            ql.PERCENTAGE_OF_DELAYED_FLIGHT_PER_HOUR_OF_THE_DAY, {}
        )

    def get_total_delayed_flights_by_origin_and_destination(self):
        """Method to gets tabloid of total delayed flights of airline by all
        origins and destionation"""
        return self._execute_query(
            ql.ORIGIN_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_AND_ARRIVAL_DELAYS, {}
        )

    def execute_bonus_query(self, query, params=None):
        """Method to execute bonus query"""
        if params is None:
            params = {}
            return self._execute_query(query, {})
        return self._execute_query(query, params)

    def insert_flight_into_flights(self, flight):
        """Method to insert flight into flights table"""
        params = {
            "id": flight["id"],
            "airline": flight["airline"],
            "delay": flight["delay"],
        }
        self._crud_queries(ql.INSERT_FLIGHT, params)

    def update_flight(self, flight):
        """Method to update flight into flights table"""
        params = {
            "id": flight["id"],
            "airline": flight["airline"],
            "delay": flight["delay"],
        }
        self._crud_queries(ql.UPDATE_FLIGHT, params)

    def delete_flight(self, flight_id):
        """Method to delete flight from flights table"""
        params = {"id": flight_id}
        self._crud_queries(ql.DELETE_FLIGHT, params)

    def __del__(self):
        """
        Closes the connection to the databse when the object is about to be destroyed
        """
        self._engine.dispose()
