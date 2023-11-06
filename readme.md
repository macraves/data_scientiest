# Scenario of SQLite3 and Working as Data Scientist

Application for reading and running appropriate SQL query to get relative data set from the database. Project files are for managing databases with instance and running its methods to get figures and draw their plot.

### data.py

Connection to database its methods.
to avoid `SQL Injection`, `Parameterized Queries` are used.

### main_plot.py

For better presentation matplotlib and folium library are used.

### how to run

Application kicks start from main.py. It is a generic file that reads functions of flight_data.py and creates a list of functions where the user can enter its command to run appropriate functions.
