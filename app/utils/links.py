import os
import csv

def get_links_from_csv(file_path: str) -> list[str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]
