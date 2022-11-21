import config
import pandas as pd
import sqlalchemy
import urllib

from datetime import date, timedelta
from clients.graphQL import TrainAPIGraphQl


query = """
{
    train(
        trainNumber:27, 
        departureDate:"XXX"
    ) {
        trainNumber
        departureDate
        cancelled
        commuterLineid
        runningCurrently
        timetableType
        timetableAcceptanceDate
        deleted
        timeTableRows {
            type
            cancelled
            scheduledTime
            actualTime
            differenceInMinutes
            unknownDelay
            commercialTrack
        station {
            shortCode
        }
    }
  }
}
"""

# initilize a date range 
# TODO: figure out a way to fetch all data at once via graphql api
start_date = date(2020, 1, 1) 
end_date = date.today()
delta = end_date - start_date

graphql_client = TrainAPIGraphQl()

normalized_data = []
for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    graphql_query = query.replace("XXX", day.strftime("%Y-%m-%d"))
    data = graphql_client.query_data(query=graphql_query)["data"]["train"]
    for row in data:
        timetable_data = row["timeTableRows"]
        for time_row in timetable_data:
            time_row["station"] = time_row["station"]["shortCode"]
            time_row["trainNumber"] = row["trainNumber"]
            time_row["departureDate"] = row["departureDate"]
            time_row["train_cancelled"] = row["cancelled"]
            time_row["commuterLineid"] = row["commuterLineid"]
            time_row["runningCurrently"] = row["runningCurrently"]
            time_row["timetableType"] = row["timetableType"]
            time_row["timetableAcceptanceDate"] = row["timetableAcceptanceDate"]
            time_row["deleted"] = row["deleted"]
            normalized_data.append(time_row)
        print(f"Now retrieving data from date: {day}")

df = pd.DataFrame(normalized_data)

# create sqlalchemy database engine, needed with pandas to_sql command
def sqlalchemy_db_connection(database, server, username, password):
    driver = "{ODBC Driver 17 for SQL Server}"
    param_raw = "DRIVER=" + driver + ";SERVER=" + server + ";DATABASE=" + \
            database + ";UID=" + username + ";PWD=" + password
    params = urllib.parse.quote_plus(param_raw)
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)
    return engine


engine = sqlalchemy_db_connection(
    config.db_name, 
    config.db_server, 
    config.db_username, 
    config.db_password
    )

table_name = "train_data"
df.to_sql(table_name, engine, schema=config.schema, if_exists="replace")
