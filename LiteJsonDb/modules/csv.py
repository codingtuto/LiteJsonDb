import csv
import os
from typing import Dict, Any, Union

class CSVExporter:
    def __init__(self, database_dir: str):
        self.database_dir = database_dir

    # ==================================================
    #                EXPORT DATA TO CSV
    # --------------------------------------------------
    # Exports JSON data to a CSV file. Supports either
    # a single collection or an entire database.
    # ==================================================
    def export(self, data: Union[Dict[str, Any], Any], filename: str = "export.csv") -> str:
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
            print(f"🐛 \033[91mWhoops! An error occurred during CSV export. It seems that something went wrong: {e}\033[0m")
            return ""