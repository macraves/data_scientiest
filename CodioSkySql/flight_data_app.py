"""API Endpoints for flight data"""
import json
from datetime import datetime
from data import FlightData, CrudError
import query_list as ql
import pandas as pd
from flask import jsonify, Flask, request

app = Flask(__name__)
FLIGHT_DATA = FlightData(ql.DATABASE_URI)


@app.route("/api/flight/<int:flight_id>", methods=["GET"])
def find_flight_by_id(flight_id):
    """Calls FlightData related method to get flight by ID query result then
    converts the result to DataFrame, this way the iteration will get quicker
    for this method, convertiong df object to dictionary and then to JSON object"""
    rows = FLIGHT_DATA.find_flight_by_id(flight_id)
    if not rows:
        return "No flight found."
    df = pd.DataFrame(rows)
    # Convert to dictionary
    dict_fact = df.to_dict(orient="records")
    # Convert to JSON object
    json_file = json.dumps(dict_fact, indent=4)
    return jsonify(json.loads(json_file))


@app.route("/api/flights", methods=["POST"])
def add_flight():
    """JSON dictionary is sent to this endpoint and then it is added to the database"""
    flight = request.get_json()
    if all(key in flight for key in ("id", "airline", "delay")):
        does_exist = FLIGHT_DATA.find_flight_by_id(flight["id"])
        if does_exist:
            return jsonify({"error": "Flight already exists"}), 400
        try:
            FLIGHT_DATA.insert_flight_into_flights(flight)
            return jsonify({"message": "Flight added successfully"}, 201)
        except CrudError:
            return jsonify({"error": "Failed to add the flight"}, 500)
    return jsonify({"error": "Invalid data format. Use JSON."}, 400)


@app.route("/api/flights/<int:flight_id>", methods=["PUT"])
def update_flight(flight_id):
    """Sends endpoint and then it is updated in the database
    Current implementation does not allow to change the flight ID
    Need to add a check for that and find a method to check CRUD operation result"""
    # Not working
    flight = request.get_json()
    does_exist = FLIGHT_DATA.find_flight_by_id(flight_id)
    if not does_exist:
        return jsonify({"error": "Flight does not exist"}), 404
    if (
        not any(key in flight for key in ("id", "airline", "delay"))
        or not isinstance(flight["id"], int)
        or not isinstance(flight["delay"], int)
        or not isinstance(flight["airline"], int)
    ):
        return jsonify({"error": "Invalid data format. Use JSON."}, 400)
    if flight["id"] != flight_id:
        return jsonify({"error": "Flight ID cannot be changed"}), 400
    # flight["airline"] = flight["airline"].title().strip()
    try:
        FLIGHT_DATA.update_flight(flight)
        return jsonify({"message": "Flight updated successfully"}, 200)
    except CrudError:
        return jsonify({"error": "Failed to update the flight"}, 500)


@app.route("/api/flights/<int:flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    """Deletes flight by ID"""
    does_exist = FLIGHT_DATA.find_flight_by_id(flight_id)
    if not does_exist:
        return jsonify({"error": "Flight does not exist"}), 404
    try:
        FLIGHT_DATA.delete_flight(flight_id)
        return jsonify({"message": "Flight deleted successfully"}, 200)
    except CrudError:
        return jsonify({"error": "Failed to delete the flight"}, 500)


@app.route("/api/flights", methods=["GET"])
def get_flights_by_date():
    """Gets users year, month and day input and calls FlightData related method"""
    try:
        year = request.args.get("year")
        month = request.args.get("month")
        day = request.args.get("day")
        date_str = f"{year}/{month}/{day}"
        # Convert date string to a Python date object
        # If format is wrong, ValueError exception will be raised
        date = datetime.strptime(date_str, "%Y/%m/%d").date()
        flights = FLIGHT_DATA.get_flights_by_date(date)
        if flights:
            flights_frame = pd.DataFrame(flights)
            flights_dict = flights_frame.to_dict(orient="records")
            json_file = json.dumps(flights_dict, indent=4)
            return jsonify(json.loads(json_file))
        return jsonify({"error": "No flights found for the given date"}, 404)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY/MM/DD' format."}, 400)


@app.route("/api/airline/delays/date", methods=["GET"])
def delayed_airline_flights_by_date():
    """Gets users year, month and day input and calls FlightData related method"""
    try:
        year = request.args.get("year")
        month = request.args.get("month")
        day = request.args.get("day")
        date_str = f"{year}/{month}/{day}"
        # Convert date string to a Python date object
        # If format is wrong, ValueError exception will be raised
        date = datetime.strptime(date_str, "%Y/%m/%d").date()
        flights = FLIGHT_DATA.delayed_airline_flights_by_date(date)
        if flights:
            flights_frame = pd.DataFrame(flights)
            flights_dict = flights_frame.to_dict(orient="records")
            json_file = json.dumps(flights_dict, indent=4)
            return jsonify(json.loads(json_file))
        return jsonify({"error": "No flights found for the given date"}, 404)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use 'YYYY/MM/DD' format."}, 400)


if __name__ == "__main__":
    app.run(debug=True)
