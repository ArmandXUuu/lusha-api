import datetime
import os
import sys
import csv

import requests

# ENV CONFIG FOR API KEY
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# GLOBAL VARIABLES
INPUT_LINE_COUNT = 0
API_ERROR_COUNT = 0


class Person:
    def __init__(self, company, first_name, last_name):
        self.company = company
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number1 = ""
        self.phone_number2 = ""

    def print_person(self):
        print("\033[1;32m" + self.first_name + " " + self.last_name + "\033[0m" + " works in " +
              "\033[1;32m" + self.company + "\033[0m" + " phone number(s): " +
              "\033[1;32m" + self.phone_number1 + "\033[0m" + " and " + "\033[1;32m" + self.phone_number2 + "\033[0m")


def read_from_csv(file_name):
    # read from csv file, get the first name, last name, company
    global INPUT_LINE_COUNT
    persons = []

    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            INPUT_LINE_COUNT += 1
            persons.append(Person(row[0], row[1], row[2]))

    return persons


def write_to_csv(persons):
    for person in persons:
        with open("output.csv", "a+") as f:
            f.write(
                person.company + "," + person.first_name + "," + person.last_name + "," + person.phone_number1 + "," + person.phone_number2 + "\n")


# To make routine work easier, we can use the Lusha API (not verified yet due to lack of the API key)
# API Document : https://www.lusha.com/docs/#person-api
def call_api(person: Person):
    url = "https://api.lusha.com/person?firstName={0}&lastName={1}&company={2}&property=phoneNumbers" \
        .format(person.first_name, person.last_name, person.company)
    headers = {"api_key": API_KEY}
    r = requests.get(url, headers=headers)
    answer = r.json()
    return url, answer


def api_response_handler(answer, person):
    global API_ERROR_COUNT
    if "errors" in answer:
        API_ERROR_COUNT += 1
        print("\033[1;31mError: \033[0m" + answer["errors"]["message"])
    else:
        person.phone_number1 = answer["data"]["phoneNumbers"][0]["internationalNumber"]
        if len(answer["data"]["phoneNumbers"]) > 1:
            person.phone_number2 = answer["data"]["phoneNumbers"][1]["internationalNumber"]
        person.print_person()


def save_request(request_url, request_answer):
    with open("records.txt", "a+") as f:
        f.write(str(datetime.datetime.now()) + "\n")
        f.write(request_url + "\n" + str(request_answer) + "\n\n")


def main():
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    persons = read_from_csv(sys.argv[1])
    print("Successfully read {0} persons from {1}".format(INPUT_LINE_COUNT, sys.argv[1]))

    for person in persons:
        url, answer = call_api(person)
        save_request(url, answer)
        api_response_handler(answer, person)

    write_to_csv(persons)

    print("\033[1;32mFinished. Results can be found in output.csv\033[0m")
    print("\033[1;33mCouldn't find {0} of {1} persons in the list.\033[0m".format(API_ERROR_COUNT, INPUT_LINE_COUNT))


if __name__ == '__main__':
    main()
