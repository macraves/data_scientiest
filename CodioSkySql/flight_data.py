"""List of executable functions for the query module."""
from datetime import datetime
import main_plot as mp


IATA_LENGTH = 3


def show_total_delayed_flights_by_origin(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data object method "get_delayed_flights_by_origin".
    and draws list of delayed flights of airports by its FLIGHT ID.
    """
    valid = False
    while not valid:
        requested_origin = input("Enter origin airport: ").upper().strip()
        if requested_origin.isalpha() and len(requested_origin) == IATA_LENGTH:
            valid = True
        rows = data_manager.get_delayed_flights_by_origin(requested_origin)
        if not rows:
            print(f"No delayed flights found for {requested_origin}.")
    mp.plot_total_delayed_flights_by_origin(rows, requested_origin)
    return "Plot is shown"


def show_scatter_plot_of_total_delayed_flights_by_all_origin(data_manager):
    """
    Gets total delayed flights by all origin with sql query in the group of origin
    and AIRLINE total delayed flights
    """
    rows = data_manager.get_total_delayed_flights_of_airline_by_all_origins()
    mp.scater_plot_of_delayed_flights_and_origins(rows)
    return "Plot is shown"


def show_plot_percentage_of_delayed_flight_per_airline(data_manager):
    """Gets percentage of delayed flights per airline"""
    rows = data_manager.get_airlines_total_delays_and_flights()
    mp.plot_percentage_of_delayed_flight_per_airline(rows)
    return "Plot is shown"


def show_plot_percentage_of_delayed_flight_per_hour_of_the_day(data_manager):
    """Gets percentage of delayed flights per airline"""
    rows = data_manager.get_percentage_delayed_flights_per_hour_of_the_day()
    mp.plot_percentage_of_delayed_flight_per_hour_of_the_day(rows)
    return "Plot is shown"


def show_scatter_heat_map(data_manager):
    """Bonus section for scatter heat map"""
    mp.scatter_heat_map_origin_destination(data_manager)
    print("Plot is shown")


def show_heat_map_of_delayed_flights_by_airline(data_manager):
    """Bonus section for heat map of delayed flights by airline"""
    mp.heat_map_origin_destination(data_manager)
    return "Plot is shown"


def show_percentage_of_delayed_flights_per_route_on_map(data_manager):
    """Displays percentage of delayed flights per route on map"""
    return mp.percentage_of_delayed_flights_per_route_on_map(data_manager)


def print_flight_by_id(data_manager):
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print" to show them to on the screen.
    """
    while True:
        try:
            requested_flight_id = int(input("Enter flight ID: "))
            if requested_flight_id < 1:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a valid flight ID.")

    rows = data_manager.get_flight_by_id(requested_flight_id)
    if not rows:
        return "No flight found."
    # none of the fetchall methods return a list of dictionary like object !!!
    list_fact = [
        {
            "airline": row[0],
            "id": row[1],
            "year": row[2],
            "month": row[3],
            "day": row[4],
            "tail no": row[8],
            "origin": row[9],
            "destination": row[10],
            "scheduled departure": f"{row[11][:2]}:{row[11][2:]}",
            "scheduled arrival": f"{row[22][:2]}:{row[11][2:]}",
        }
        for row in rows
    ]
    flight_info = list_fact[0]
    dict_map = map(lambda x: f"{x[0]}: {x[1]}", flight_info.items())
    return "\n".join(dict_map)


def print_flights_by_date(data_manager):
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print" to show them to on the screen.
    """
    while True:
        try:
            requested_date = input("Enter date in format(YYYY/MM/DD): ")
            date = datetime.strptime(requested_date, "%Y/%m/%d")
            rows = data_manager.get_flights_by_date(date)
            if not rows:
                print(f"No flights found in requested date {requested_date}.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid date in format (YYYY/MM/DD).")

    map_rows = map(
        lambda x: f"""Date: {x[0]}/{x[1]}/{x[2]}
    Flight no: {x[3]}, Airline {x[4]} Tail: {x[5]}, Origin: {x[6]}
    Destination: {x[7]}, Departure: {x[8]}, Arrive: {x[9]}""",
        rows,
    )
    return "\n".join(map_rows)


def print_delayed_flights_by_airline(data_manager):
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method "get_delayed_flights_by_airline".
    When results are back, calls "print" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            requested_airline = input("Enter airline: ")
            requested_airline = requested_airline.title().strip()
            if len(requested_airline) > 3 or not requested_airline.isnumeric():
                valid = True
            rows = data_manager.get_delayed_flights_by_airline(requested_airline)
            if not rows:
                print(f"No delayed flights found for {requested_airline}.")
                continue
        except ValueError as val_err:
            print("Invalid input. Please enter a valid airline.\n", val_err)

    # -- 2. JFK -> LAX by Virgin America, Delay: 28 Minutes
    filtered_rows = filter(
        lambda row: (row[3] is not None and row[3] != "") and float(row[3]) > 20, rows
    )
    template = map(
        lambda x: f"""{x[0]}. {x[1]} -> LAX by {x[2]}, Delay: {x[3]} Minutes""",
        filtered_rows,
    )
    return (
        "\n".join(template)
        + "\n"
        + f"Total delayed flights: {len(rows)} that more than 20 minutes"
    )


def print_delayed_flights_by_origin(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data object method "get_delayed_flights_by_airport".
    """
    valid = False
    while not valid:
        requested_origin = input("Enter origin airport: ").upper().strip()
        if requested_origin.isalpha() and len(requested_origin) == IATA_LENGTH:
            valid = True
        rows = data_manager.get_delayed_flights_by_origin(requested_origin)
        rows = [row for row in rows if row[3] > 20 and row[3] != ""]
        if not rows:
            print(f"No delayed flights found with {requested_origin}.")
            continue
    template = map(
        lambda x: f"""Flightno: {x[0]} {x[1]} -> LAX by {x[2]}, Delay: {x[3]} minutes""",
        rows,
    )

    return "\n".join(template)
