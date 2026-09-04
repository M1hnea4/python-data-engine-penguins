import csv
import os

def clean_penguins_data(input_file, output_file):
    """
    Reads the raw data, cleans it, and saves it to a new CSV file.

    :param input_file: The path to the raw CSV file.
    :param output_file: The path where the cleaned CSV file will be saved.
    :return: None
    """
    required_columns = [
        'species', 'flipper_length_mm', 'culmen_length_mm', 
        'culmen_depth_mm', 'body_mass_g', 'island', 'sex'
    ]

    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', newline='', encoding='utf-8') as fout:
        
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=required_columns)
        writer.writeheader()
        
        count = 0
        for row in reader:
            raw_species = row.get('Species', '')
            flipper = row.get('Flipper Length (mm)', '')
            culmen_len = row.get('Culmen Length (mm)', '')
            culmen_depth = row.get('Culmen Depth (mm)', '')
            mass = row.get('Body Mass (g)', '')
            island = row.get('Island', '')
            sex = row.get('Sex', '')
            
            values_to_check = [raw_species, flipper, culmen_len, culmen_depth, mass, island, sex]
            if any(v in [None, '', '.', 'NA'] for v in values_to_check):
                continue

            if 'Adelie' in raw_species: species = 'Adelie'
            elif 'Chinstrap' in raw_species: species = 'Chinstrap'
            elif 'Gentoo' in raw_species: species = 'Gentoo'
            else: species = raw_species

            writer.writerow({
                'species': species,
                'flipper_length_mm': flipper,
                'culmen_length_mm': culmen_len,
                'culmen_depth_mm': culmen_depth,
                'body_mass_g': mass,
                'island': island,
                'sex': sex
            })
            count += 1
            
    print(f"Successfully created '{output_file}' with {count} valid rows.")

if __name__ == "__main__":
    clean_penguins_data('penguins.csv', 'penguins_data.csv')