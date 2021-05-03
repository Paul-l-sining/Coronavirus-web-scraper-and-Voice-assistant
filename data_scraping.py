import requests
import json
import threading
import time


API_KEY = "t4QaG-fBKT1P"
PROJECT_TOKEN = "t0McMKTWGhfd"
RUN_TOKEN = "tqQUN7EZDnCU"


# Scrape data from the web "https://www.worldometers.info/coronavirus/" using parse.
class Data:
    def __init__(self, api_key=API_KEY, project_token=PROJECT_TOKEN):
        self.project_token = project_token
        self.api_key = api_key
        self.data = self.getData()

    def getData(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params={"api_key": self.api_key})
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        # Retrieve total cases from the web
        for content in self.data['total']:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']
        return "0"

    def get_total_death(self):
        # Retrieve total death from the web
        for content in self.data['total']:
            if content['name'] == 'Deaths:':
                return content['value']
        return "0"

    def get_total_recovered(self):
        # Retrieve total recovered from the web
        for content in self.data['total']:
            if content['name'] == 'Recovered:':
                return content['value']
        return "0"

    def get_country_data(self, country):
        # Retrieve a single country's information.
        for content in self.data["countries"]:
            if content['name'].lower() == country.lower():
                return content
        return "0"

    def get_list_of_countries(self):
        # Get a list of countries
        countries = []
        for country in self.data['countries']:
            countries.append(country['name'].lower())

        return countries

    def update_data(self):
        # Update data
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                 params={"api_key": self.api_key})

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.getData()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated!")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


if __name__ == '__main__':
    data = Data()
    print(f'Total cases: {data.get_total_cases()}')
    print(f'Total deaths: {data.get_total_death()}')
    print(f'Total recovered: {data.get_total_recovered()}')
    print(f'Total cases in China: {data.get_country_data("china")}')
    print(data.get_list_of_countries())
