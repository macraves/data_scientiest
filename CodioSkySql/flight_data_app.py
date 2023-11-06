"""API Endpoints for flight data"""
import json
from datetime import datetime
from data import FlightData
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


if __name__ == "__main__":
    app.run(debug=True)

column_dict = {
    "ID": [653, 4543],
    "airport": ["JFK", "JFK"],
    "AIRLINE": ["American Airlines Inc.", "JetBlue Airways"],
    "DELAY": [21, 21],
}
