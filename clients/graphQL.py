import requests
import json
import time


class TrainAPIGraphQl:
    """
    Used to fetch data from rata.digitraffic
    """ 

    def __init__(self):
        self.headers: dict = {"Content-Type": "application/json", "Accept-Encoding": "gzip"}


    def query_data(self, query: str):

        q = {"query": f"""{query}"""}
        graphql_url = "https://rata.digitraffic.fi/api/v2/graphql/graphql"
        r = requests.post(graphql_url, headers=self.headers, json=q)
        if r.status_code == 200:
            data = json.loads(r.content)
        elif r.status_code in [401,403,404,429]:
            print(f"status code: {r.status_code}, sleeping")
            time.sleep(5) # 60 requests per minute
            r = requests.post(graphql_url, headers=self.headers, json=q)
            if r.status_code == 200:
                data = json.loads(r.content)
            else:
                print(r.content)
                raise Exception(f"Error fetching data for: {print(r.content)}")
                
        elif r.status_code != 200:
            print(r.content)
            raise Exception(f"Error fetching data for: {print(r.content)}")

        return data

