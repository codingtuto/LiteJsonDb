import csv
import os
from typing import Dict, Any, Union

class CSVExporter:
    """
    A class for exporting data to CSV files.

    This class provides functionality to export JSON-like data (dictionaries or lists of dictionaries)
    to CSV files. It supports writing either a single collection or an entire database.
    """
    def __init__(self, database_dir: str):
        """
        Initializes the CSVExporter with the directory where CSV files will be saved.

        Args:
            database_dir (str): The directory where the CSV files will be saved.
        """
        self.database_dir = database_dir

    def export(self, data: Union[Dict[str, Any], Any], filename: str = "export.csv") -> str:
        """
        Exports JSON data to a CSV file. Supports either a single collection or an entire database.

        Args:
            data (Union[Dict[str, Any], Any]): The data to export. This can be a dictionary,
                a list of dictionaries, or any other data structure that can be written to CSV.
            filename (str, optional): The name of the CSV file to create. Defaults to "export.csv".

        Returns:
            str: The path to the created CSV file, or an empty string if the export failed.
        """
        filepath = os.path.join(self.database_dir, filename)
        try:
            with open(filepath, mode="w", newline='', encoding="utf-8") as csv_file:
                if isinstance(data, dict):
                    data = [data[key] for key in data.keys()]
                if data:
                    headers = data[0].keys() if isinstance(data, list) else data.keys()
                    writer = csv.DictWriter(csv_file, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data if isinstance(data, list) else [data])
            return filepath
        except Exception as e:
            print(f"\033[91m#bugs\033[0m CSV export error: {e}")
            return ""