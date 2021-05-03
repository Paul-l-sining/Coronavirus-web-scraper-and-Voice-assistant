from data_scraping import Data
from voice_assistant import voice_assistant

import re


def main():
    print("Program Started")
    END_PHRASE = 'stop'
    data = Data()

    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_death,
        re.compile("[\w\s]+ total death"): data.get_total_death,
        re.compile("[\w\s]+ total [\w\s]+ recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ total recovered"): data.get_total_recovered
    }

    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)["total_cases"],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)["total_deaths"],
        re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: data.get_country_data(country)["total_recovered"]
    }

    UPDATE_COMMAND = "update"

    va = voice_assistant()

    while True:
        print("Listening...")
        text = va.get_audio()
        print(text)
        result = None

        for patten, func in COUNTRY_PATTERNS.items():
            if patten.match(text):
                words = set(text.split(" "))
                for country in data.get_list_of_countries():
                    if country in words:
                        result = func(country)
                        break

        for patten, func in TOTAL_PATTERNS.items():
            if patten.match(text):
                result = func()
                break

        if text == UPDATE_COMMAND:
            result = "Data is being updated. This may take a moment!"
            data.update_data()

        if result:
            print(result)
            va.speak(result)

        if text.find(END_PHRASE) != -1:  # Stop loop
            print("Exit")
            break


if __name__ == '__main__':
    main()
