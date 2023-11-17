import csv
import json
from collections import defaultdict

class Item:
    def __init__(self, name, classname):
        self.name = name
        self.classname = classname

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name and self.classname == other.classname

    def __hash__(self):
        return hash((self.name, self.classname))

def read_csv(file_path):
    groups = defaultdict(set)
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
                            group_key = headers[i].strip()
                            item = Item(name, classname)
                            groups[group_key].add(item)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return groups

def sort_and_deduplicate_groups(groups):
    sorted_groups = {}
    seen = set()
    for key, items in groups.items():
        unique_items = [item for item in items if item not in seen]
        seen.update(unique_items)
        sorted_groups[key] = sorted(unique_items, key=lambda item: item.name)
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
            writer.writerow(['NAME', 'CLASSNAME'])
            for items in groups.values():
                for item in items:
                    writer.writerow([item.name, item.classname])
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

def main():
    input_file = 'data.csv'
    output_json_file = 'data.json'
    output_csv_file = 'cleaned-data.csv'

    groups = read_csv(input_file)
    sorted_groups = sort_and_deduplicate_groups(groups)
    json_output = convert_to_json(sorted_groups)
    write_json(output_json_file, json_output)
    write_csv(output_csv_file, sorted_groups)

    print(f"Structured to {output_json_file}")
    print(f"Cleaned to {output_csv_file}")

if __name__ == "__main__":
    main()