import urllib.request
import csv
import argparse
import logging
from datetime import datetime


def downloadData( url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return data
    except Exception as e:
        logging.error(f"Error downloading data from {url}: {e}")
        return None


def processData(csv_data):
    person_data = {}
    try:
        csv_reader = csv.reader(csv_data.splitlines())
        next(csv_reader)
        for row in csv_reader:
            if len(row) == 3:
                id_number, name, birthday_str = row
                try:
                    id_number = int(id_number)
                    birthday = datetime.strptime(birthday_str, '%d/%m/%Y').date()
                    person_data[id_number] = (name, birthday)
                except (ValueError, IndexError, ValueError) as e:
                    logging.error(f"Error processing line: {row}, Error: {e}")
    except Exception as e:
        logging.error(f"Error processing CSV data: {e}")

    return person_data


def displayPerson(id_number, person_data):
    if id_number in person_data:
        name, birthday = person_data[id_number]
        print(f"Person #{id_number} is {name} with a birthday of {birthday.strftime('%Y%m%d')}")
    else:
        print(f"No user found with ID #{id_number}")


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

