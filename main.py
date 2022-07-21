import datetime
import os
import sys
import csv
import json

import requests

# ENV CONFIG FOR API KEY
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# GLOBAL VARIABLES
INPUT_LINE_COUNT = 0
API_ERROR_COUNT = 0
CONTACT_ID = 0
RequestStruct = {
    "filters": {
        "property": "phoneNumbers"
    }
}


class JSONHelper(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, PersonRequestStruct):
            return o.__dict__
        return super().default(o)


class PersonRequestStruct:
    def __init__(self, company, first_name, last_name):
        global CONTACT_ID
        self.contactId = str(CONTACT_ID)
        self.companies = [{
            "name": company,
            "isCurrent": True,
        }]
        self.firstName = first_name
        self.lastName = last_name
        CONTACT_ID += 1


class PersonResStruct():
    def __init__(self, contact_id, company, first_name, last_name, phone_number1, phone_number2):
        self.contact_id = contact_id
        self.company = company
        self.firstName = first_name
        self.lastName = last_name
        self.phone_number1 = phone_number1
        self.phone_number2 = phone_number2

    def print_person(self):
        print("\033[1;32m" + self.firstName + " " + self.lastName + "\033[0m" + " works in " +
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
            persons.append(PersonRequestStruct(row[0], row[1], row[2]))

    return persons


def write_to_csv(persons: [PersonResStruct]):
    for person in persons:
        with open("output.csv", "a+") as f:
            f.write(
                person.contact_id + "," + person.company + "," + person.firstName + "," + person.lastName + "," +
                person.phone_number1 + "," + person.phone_number2 + "\n")


# To make routine work easier, we can use the Lusha API (not verified yet due to lack of the API key)
# API Document : https://www.lusha.com/docs/#person-api
def call_bulk_api(RequestStruct: dict):
    url = "https://api.lusha.com/bulk/person"
    headers = {'api_key': API_KEY, 'Content-type': 'application/json'}
    payload = json.dumps(RequestStruct, cls=JSONHelper)
    r = requests.post(url, headers=headers, data=payload)
    answer = r.json()
    return url, answer


def api_response_handler(answer, persons):
    global API_ERROR_COUNT
    answer_contact = answer["contacts"]
    persons_response = []

    print("Got {0} answers from server.".format(len(answer_contact)))

    for a in answer_contact.keys():
        contact = answer_contact[a]
        person = PersonResStruct(a, persons[int(a)].companies[0]["name"], persons[int(a)].firstName, persons[int(a)].lastName,
                                 "", "")
        if "firstName" not in answer_contact[a]:
            print("\033[1;31mError: \033[0m {0} - {1} : {2}"
                  .format(str(persons[int(a)].contactId),
                          str(persons[int(a)].firstName) + ' ' + str(persons[int(a)].lastName),
                          str(answer_contact[a])))
            API_ERROR_COUNT += 1
        elif len(contact["phones"]) == 0:
            print("\033[1;31mError: \033[0m {0} - {1} : The STUPID API returned a person WITH NO PHONE"
                  .format(str(persons[int(a)].contactId),
                          str(persons[int(a)].firstName) + ' ' + str(persons[int(a)].lastName)))
            API_ERROR_COUNT += 1
        else:
            phone_2 = contact["phones"][1] if len(contact["phones"]) == 2 else ""
            person.phone_number1 = contact["phones"][0]
            person.phone_number2 = phone_2
            person.print_person()

        persons_response.append(person)

    return persons_response


def save_request(request_url, request_answer):
    with open("records.txt", "a+") as f:
        f.write(str(datetime.datetime.now()) + "\n")
        f.write(request_url + "\n" + str(request_answer) + "\n\n")


def main():
    if os.path.exists("output.csv"):
        os.remove("output.csv")

    persons = read_from_csv(sys.argv[1])
    print("Successfully read {0} persons from {1}".format(INPUT_LINE_COUNT, sys.argv[1]))

    RequestStruct["contacts"] = persons

    url, answer = call_bulk_api(RequestStruct)
    save_request(url, answer)
    persons_respons = api_response_handler(answer, persons)

    write_to_csv(persons_respons)

    print("\033[1;32mFinished. Results can be found in output.csv\033[0m")
    print("\033[1;33mCouldn't find {0} of {1} persons in the list.\033[0m".format(API_ERROR_COUNT, INPUT_LINE_COUNT))


if __name__ == '__main__':
    main()
