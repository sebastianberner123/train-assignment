import sys
from os import path
sys.path.append(path.dirname(path.dirname(__file__)))


def calculate_avg(db_client, train_number):
    query = f"""
        SELECT AVG(differenceInMinutes) 
        FROM sebastian_test.train_data
        WHERE
            trainNumber = {train_number} AND
            station = 'TPE' AND 
            [type] = 'ARRIVAL'
    """


    cursor = db_client.connection.cursor()
    avg_time = cursor.execute(query).fetchone()[0]
    return avg_time


def calculate_total_time(db_client, train_number):
    query = f"""
        SELECT AVG(differenceInMinutes) 
        FROM sebastian_test.train_data
        WHERE
            trainNumber = {train_number} AND
            station = 'TPE' AND 
            [type] = 'ARRIVAL'
    """


    cursor = db_client.connection.cursor()
    avg_time = cursor.execute(query).fetchone()[0]
    return avg_time

