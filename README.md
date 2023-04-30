# sqlalchemy-challenge
## Part 1: Analyze and Explore the Climate Data
Using the provided starter files, I used SQLAlchemy functions to create_engine() to the SQLite database, automap_base() function to reflect the table (saving references to the two classes) and created a SQLAlchemy session to link it to Python.

The next step was to perform an analysis on the precipitation data by finding the most recent date, and querying the date from the prior 12 months. This was then loaded into a DataFrame and sorted by date, before being turned into a bar chart. Finally, I printed summary statistics for the precipitation data.

Then, I performed analysis on the station date, by both identifying the total number of stations, and determine which ones were most active (frequently updated). After querying the prior 12 months of data for the most active station, I created a histogram to show frequency of observed temperatures.

## Part 2: Design a Climate App
