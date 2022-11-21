import logging

import azure.functions as func
import config
from ..clients.database import DatabaseClient
from data import predictions


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(f"Error in parsing json.", status_code=500)
    
    try:
        train_number = req_body["train_number"]
        arrival_date = req_body["arrival_date"]
        arrival_time = req_body["arrival_time"]
    except KeyError:
        return func.HttpResponse(f"Add required keys: train_number, arrival_date, arrival_time.", status_code=400)

    with DatabaseClient(
        config.db_server,
        config.db_name,
        config.db_username,
        config.db_password
    ) as db_client:
        prediction = predictions.calculate_avg(db_client, train_number=train_number)

    ret_string = f"The average delay has historically been {prediction} minutes. Intercity 27 is scheduled to depart at 14:24 and arrive at 15:58. Therefore, if you want to arrive {arrival_date} at {arrival_time}, you will have to take another train."
    return func.HttpResponse(
             ret_string,
             status_code=200
        )
