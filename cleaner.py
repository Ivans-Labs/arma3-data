import csv
import json
from collections import defaultdict

class Item:
    def __init__(self, name, classname):
        self.name = name
        self.classname = classname

    def __lt__(self, other):
        return self.name < other.name

def read_csv(file_path):
    groups = defaultdict(list)
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                for i in range(0, len(row), 2):
                    name = row[i].strip()
                    if name and i + 1 < len(row):
                        classname = row[i + 1].strip()
                        if classname:
                            group_key = headers[i]
                            groups[group_key].append(Item(name, classname))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return groups

def sort_groups(groups):
    sorted_groups = {}
    for key, items in groups.items():
        sorted_groups[key.strip()] = sorted(items, key=lambda item: item.name)
    return sorted_groups

def convert_to_json(groups):
    json_data = {}
    for key, items in groups.items():
        json_data[key] = [{'name': item.name, 'classname': item.classname} for item in items]
    return json.dumps(json_data, indent=4)

def write_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            jsonfile.write(data)
    except Exception as e:
        print(f"An error occurred while writing to JSON: {e}")

def write_csv(file_path, groups):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the headers
            headers = [key for key in groups.keys() for _ in (0, 1)]
            writer.writerow(headers)
            # Write the sorted data
            rows = zip(*[[(item.name, item.classname) for item in items] for items in groups.values()])
            for row in rows:
                flattened_row = [element for pair in row for element in pair]
                writer.writerow(flattened_row)
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

def main():
    input_file = 'data.csv'
    output_json_file = 'data.json'
    output_csv_file = 'sorted_data.csv'

    groups = read_csv(input_file)
    sorted_groups = sort_groups(groups)
    json_output = convert_to_json(sorted_groups)
    write_json(output_json_file, json_output)
    write_csv(output_csv_file, sorted_groups)

    print(f"Structured JSON data written to {output_json_file}")
    print(f"Sorted CSV data written to {output_csv_file}")

if __name__ == "__main__":
    main()