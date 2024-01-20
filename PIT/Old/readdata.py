import os
import time
import csv

index = 1

while os.path.exists(f"{index}.data.csv"):
    index += 1
file_name = f"{index-1}.data.csv"


def display_most_up_to_date_info(csv_file):
    # Read the CSV file
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    # Transpose the data
    transposed_data = list(map(list, zip(*data)))

    # Remove empty columns
    cleaned_data = [col for col in transposed_data if any(col)]

    # Get the last non-null values in each row
    result = [col[-1] if col else '' for col in cleaned_data]

    # Print the result
    # print(','.join(map(str, result)))

    # formatted
    cw = [max(len(str(value)) for value in col) for col in cleaned_data]
    for row in zip(*cleaned_data):
        f_row = [f"{value: <{width}}" for value, width in zip(row, cw)]
        print(','.join(f_row))


while True:

    # Replace 'your_file.csv' with the actual path to your CSV file
    display_most_up_to_date_info(file_name)

    time.sleep(0.1)
