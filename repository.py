import csv
import os
from domain import Penguin

class PenguinRepository:
    def __init__(self, directory='.'):
        """
        Initializes the repository with a specific directory.
        
        :param directory: The directory path where CSV files are located (default is current dir).
        """
        self.directory = directory
        self._data = []

    def list_csv_files(self):
        """
        Scans the repository directory for files ending in .csv.
        
        :return: A list of strings representing the names of available CSV files.
        """
        if not os.path.exists(self.directory):
            return []
        return [f for f in os.listdir(self.directory) if f.endswith('.csv')]

    def load_data(self, filename):
        """
        Reads a CSV file from the repository directory and converts rows into Penguin objects.
        Valid rows are added to the internal data list; invalid rows are skipped.
        
        :param filename: The name of the CSV file to load.
        :return: The number of valid penguin records loaded (int).
        :raises FileNotFoundError: If the specified file does not exist in the directory.
        """
        filepath = os.path.join(self.directory, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filename} not found.")
        
        new_data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    new_data.append(Penguin.from_dict(row))
                except ValueError:
                    continue # Skip bad rows
        
        self._data = new_data
        return len(self._data)

    def get_all(self):
        """
        Retrieves the list of currently loaded Penguin objects.
        
        :return: A list of Penguin instances.
        """
        return self._data

    def save_data(self, filename, penguins):
        """
        Writes a list of Penguin objects to a CSV file.
        Overwrites the file if it already exists.
        
        :param filename: The name of the file to write to.
        :param penguins: A list of Penguin objects to serialize.
        :return: None
        """
        filepath = os.path.join(self.directory, filename)
        fieldnames = ['species', 'flipper_length_mm', 'culmen_length_mm', 
                      'culmen_depth_mm', 'body_mass_g', 'island', 'sex']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in penguins:
                writer.writerow({
                    'species': p.species,
                    'flipper_length_mm': p.flipper_length_mm,
                    'culmen_length_mm': p.culmen_length_mm,
                    'culmen_depth_mm': p.culmen_depth_mm,
                    'body_mass_g': p.body_mass_g,
                    'island': p.island,
                    'sex': p.sex
                })

    def log_sorting_performance(self, log_entry):
        """
        Appends a sorting performance record to the 'sorting_log.csv' file.
        Creates the file with headers if it does not exist.
        
        :param log_entry: A dictionary containing the run details (date, time, rows, algo, duration).
        :return: None
        """
        filepath = os.path.join(self.directory, 'sorting_log.csv')
        file_exists = os.path.isfile(filepath)
        
        fieldnames = ['date_of_run', 'time_of_run', 'number_of_rows', 
                      'sorting_algorithm', 'execution_time_in_seconds']
        
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)