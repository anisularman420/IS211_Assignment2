import urllib.request
import csv
import argparse
import logging
import datetime

def downloadData(url):
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")
        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        exit(1)

def processData(data):
    person_data = {}
    lines = data.split('\n')
    for line in lines:
        if line:
            try:
                id, name, birthday = line.split(',')
                person_data[int(id)] = (name, birthday)
            except ValueError:
                logging.error(f"Invalid data format: {line}")
    return person_data

def displayPerson(id_number, person_data):
    if id_number <= 0:
        print("ID must be a positive number.")
    elif id_number in person_data:
        name, birthday = person_data[id_number]
        print(f"Name: {name}, Birthday: {birthday}")
    else:
        print("Person not found.")

def main():
    parser = argparse.ArgumentParser(description="Assignment 2 - Python Standard Library")
    parser.add_argument('url', type=str, help="URL of the CSV data")
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR, format="Error processing line: %(message)s")

    csv_url = args.url
    csv_data = downloadData(csv_url)

    if csv_data:
        person_data = processData(csv_data)

        while True:
            try:
                id_number = int(input("Enter an ID number (0 or negative to exit): "))
                if id_number <= 0:
                    break
                displayPerson(id_number, person_data)
            except ValueError:
                print("Invalid input. Please enter a valid ID number.")

if __name__ == "__main__":
    main()
