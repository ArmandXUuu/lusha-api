import os
import requests
import json

# ENV CONFIG FOR API KEY
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


def read_from_csv(file_name):
    # read from csv file, get the first name, last name, company
    with open(file_name, "r") as f:
        lines = f.readlines()
        persons = []
        for line in lines:
            person = line.split(",")
            persons.append(person)
    ...


def write_to_csv(file_name, data):
    ...


# To make routine work easier, we can use the Lusha API (not verified yet due to lack of the API key)
# API Document : https://www.lusha.com/docs/#person-api
def call_api(first_name, last_name, company):
    url = "https://api.lusha.com/person?firstName={0}&lastName={1}&company={2}&property=phoneNumbers".format(first_name, last_name, company)
    headers = {"api_key": API_KEY}
    r = requests.get(url, headers=headers)
    answer = r.json()
    return answer


def test():
    # read from csv file, get the first name, last name, company, domain
    persons = read_from_csv(file_name)

    for person in persons:
        call_api(...)
        # add the phone number to csv file
        write_to_csv(file_name, person, phone_number)

    return


def main():
    print("Hello world")
    print(API_KEY)
    answer = call_api("Fanny", "Dufourt", "PAYOT")
    print(answer)


if __name__ == '__main__':
    main()