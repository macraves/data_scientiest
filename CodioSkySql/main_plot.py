"""Plotting functions for flights data"""

from matplotlib.colors import Normalize
from matplotlib import cm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import query_list as ql
import folium
from branca.colormap import LinearColormap


def percentage_of_delayed_flights_per_route_on_map(data_manager):
    """Plots percentage of delayed flights per route on map"""
    while True:
        origin = input("Enter origin airport: ")
        origin = origin.upper().strip()
        if not len(origin) == 3:
            print("Please enter a valid airport code")
            continue
        break
    m = folium.Map(location=[30.19453, -97.66987], zoom_start=4)
    params = {"origin": origin}
    query = ql.LOCATION_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_DELAYS
    results = data_manager.execute_bonus_query(query, params)
    df = pd.DataFrame(results)
    df["delays_percentage"] = round(
        ((df["total_delays"] // 60) / df["total_flights"]) * 100, 2
    )
    df["origin"] = df["origin"].astype(str)
    df["destination"] = df["destination"].astype(str)
    df["delays_percentage"] = df["delays_percentage"].astype(float)

    # Create a color map based on delays_percentage
    color_map = LinearColormap(
        ["yellow", "blue", "darkred"],
        vmin=df["delays_percentage"].min(),
        vmax=df["delays_percentage"].max(),
    )
    origin = df["origin"].iloc[0]
    origin_lat = df["origin_lat"].iloc[0]
    origin_long = df["origin_long"].iloc[0]
    folium.Marker(
        location=[origin_lat, origin_long],
        tooltip=origin,
        icon=folium.Icon(color="red", icon="plane", prefix="fa"),
    ).add_to(m)

    coordinates = []
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["destination_lat"], row["destination_long"]],
            tooltip=row["destination"],
            popup=f"Percentage of delayed flights: {row['delays_percentage']}%",
            icon=folium.Icon(color="green", icon="plane", prefix="fa"),
        ).add_to(m)
        coordinates.append(
            [
                (float(row["origin_lat"]), float(row["origin_long"])),
                (float(row["destination_lat"]), float(row["destination_long"])),
            ]
        )

    for i, coord in enumerate(coordinates):
        delay_percentage = df.loc[i, "delays_percentage"]
        color = color_map(delay_percentage)

        folium.PolyLine(
            locations=coord,
            color=color,
            weight=8,
            opacity=1,
            smooth_factor=0,
        ).add_to(m)

    color_map.add_to(m)
    m.save(f"{origin} overview.html")
    return f"Map saved as {origin} overview.html"


def scatter_heat_map_origin_destination(data_manager):
    """Scatter plot of delayed flights by origin and destination
    Uses pd read_sql_query to read data from a database to calculate departure delays
    as a percentage of total departure delays and plot it on a scatter plot"""

    query = ql.ORIGIN_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_AND_ARRIVAL_DELAYS
    records = data_manager.execute_bonus_query(query)
    df = pd.DataFrame(records)
    df["delay_percentage"] = round(
        ((df["departure_delays"] / 60) / df["total_flights"]) * 100, 2
    )
    origin = df["origin"]
    destination = df["destination"]
    delay_percentage = df["delay_percentage"]

    # Customizing scatter plot
    norm = Normalize(vmin=min(delay_percentage), vmax=max(delay_percentage))
    cmap = cm.get_cmap("Reds")
    s = delay_percentage * 1

    sc = plt.scatter(
        origin,
        destination,
        c=delay_percentage,
        s=s,  # Marker size is delay_percentage * 1
        edgecolor="black",
        linewidths=1,
        cmap=cmap,
        norm=norm,
    )

    cbar = plt.colorbar(sc, format="%.1f")
    cbar.set_label("Percentage of delayed")
    plt.title("Percentage of delayed on a heatmap of routes (Origin <-> Destination)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


def heat_map_origin_destination(data_manager):
    """Plots heatmap of total departure delays by origin and destination
    Uses pd read_sql_query to read data from database to calculate departure delays
    then calculates percentage of total departure delays by origin and destination
    to represent weighted heatmap of total departure delays origin and destination"""

    query = ql.ORIGIN_DESTINATION_TOTAL_FLIGHTS_DEPARTURE_AND_ARRIVAL_DELAYS
    results = data_manager.execute_bonus_query(query)
    df = pd.DataFrame(results)
    # Adding new column to dataframe as 'delay_percentage' where minutes
    # converted to hours and divided by total flights then multiplied by 100
    df["delay_percentage"] = round(
        ((df["departure_delays"] / 60) / df["total_flights"]) * 100, 2
    )
    # Pivot table to create heatmap data
    heatmap_data = df.pivot(
        index="origin", columns="destination", values="delay_percentage"
    )

    plt.figure(figsize=(12, 8))
    plt.title("Percentage of delayed on a heatmap of routes (Origin <-> Destination)")
    sns.heatmap(
        heatmap_data, cmap="YlOrRd", linewidths=0.5, linecolor="black", cbar=True
    )

    plt.show()


def plot_total_delayed_flights_by_origin(delayed_origin_flights, origin):
    """Plot delayed flights by origin, where creates frequency of delayed flights of airlines
    and plot it by bar chart"""
    airlines = {}
    for flight in delayed_origin_flights:
        if flight[2] not in airlines:
            airlines[flight[2]] = flight[3]
        else:
            airlines[flight[2]] += flight[3]

    airline = list(airlines.keys())
    delays_in_minutes = list(airlines.values())

    plt.figure(figsize=(10, 6))
    plt.bar(airline, delays_in_minutes)
    plt.xlabel("AIRLINES")
    plt.ylabel("Delay (Minutes)")
    plt.title(f"Delayed Flights from {origin} Airport")
    plt.xticks(rotation=45)
    plt.show()


def scater_plot_of_delayed_flights_and_origins(data):
    """Origin and airline places on x and y axis and their delays
    time colored by given values as minutes"""
    origins = [row[0] for row in data]
    airlines = [row[1] for row in data]
    delays = [row[2] for row in data]
    plt.scatter(origins, airlines, c=delays, cmap="viridis")
    plt.xlabel("Origin")
    plt.ylabel("Airline")
    plt.title("Scatter Plot of Delays by Origin and Airline")
    plt.colorbar(label="Delays (minutes)")
    plt.xticks(rotation=45)
    plt.show()


def plot_percentage_of_delayed_flight_per_airline(data):
    """Extracts total number of flights and delays of airlines and
    calculates percentage of delayed flights per airline by
    total_delays / total_flights * 100"""
    airlines = [row[0] for row in data]
    total_delays_in_minutes = [row[1] for row in data]
    total_flights_of_airline = [row[2] for row in data]

    delayed_percentage = [
        round(((minutes // 60) / flights) * 100, 2)
        for minutes, flights in zip(total_delays_in_minutes, total_flights_of_airline)
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(airlines, delayed_percentage)
    plt.xlabel("AIRLINES")
    plt.ylabel("Percentage of Delayed Flights")
    plt.title("Percentage of Delayed Flights per Airline")
    plt.xticks(rotation=45)
    plt.show()


def plot_percentage_of_delayed_flight_per_hour_of_the_day(data):
    """Plots percentage of delayed flights per hour of the day"""
    hours_freq = {}
    # Extracts hours from time and calculates total flights and delays per hour
    for row in data:
        clock = row[0][:2]
        if clock not in hours_freq:
            hours_freq[clock] = {"total flights": row[1], "total delay": row[2]}
        else:
            hours_freq[clock]["total flights"] += row[1]
            hours_freq[clock]["total delay"] += row[2]
    # Calculates percentage of delayed flights per hour and keep them in list of tuples
    hours_percentage = [
        (k, round(((v["total delay"] / 60) / v["total flights"]) * 100, 2))
        for k, v in hours_freq.items()
    ]
    # Sorts list of tuples by hour
    hours_percentage = sorted(hours_percentage, key=lambda x: x[0])
    hours = [x[0] for x in hours_percentage]
    percentage = [x[1] for x in hours_percentage]
    plt.bar(hours, percentage)
    plt.xlabel("Hours of Day")
    plt.ylabel("Percentage of Delayed Flights (%)")
    plt.title("Percentage of Delayed Flights by Hour Day")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
