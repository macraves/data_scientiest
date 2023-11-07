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
def get_flight_by_id(flight_id):
    """Calls FlightData related method to get flight by ID query result then
    converts the result to DataFrame, this way the iteration will get quicker
    for this method, convertiong df object to dictionary and then to JSON object"""
    rows = FLIGHT_DATA.get_flight_by_id(flight_id)
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
        try:
            FLIGHT_DATA.insert_flight_into_flights(flight)
            return jsonify({"message": "Flight added successfully"}, 201)
        except CrudError:
            return jsonify({"error": "Failed to add the flight"}, 500)
    return jsonify({"error": "Invalid data format. Use JSON."}, 400)


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


if __name__ == "__main__":
    app.run(debug=True)

# column_dict = {
#     "ID": [653, 4543],
#     "airport": ["JFK", "JFK"],
#     "AIRLINE": ["American Airlines Inc.", "JetBlue Airways"],
#     "DELAY": [21, 21],
# }
