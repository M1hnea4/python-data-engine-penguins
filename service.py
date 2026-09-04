
import os
import csv
import random
import time
import math
import datetime
import matplotlib.pyplot as plt 
from domain import Penguin
from exceptions import DataNotLoadedError, InvalidAttributeError

class PenguinService:
    def __init__(self, repo):
        """
        Initializes the PenguinService.
        
        :param repo: The repository instance used for data access.
        """
        self.repo = repo

    def _ensure_data(self):
        """
        Checks if data is loaded in the repository.
        Raises an exception if no data is present.
        
        :raises DataNotLoadedError: If the repository data list is empty.
        :return: None
        """
        if not self.repo.get_all():
            raise DataNotLoadedError("No data loaded.")

    def get_available_files(self):
        """
        Retrieves a list of available CSV files from the repository's directory.
        
        :return: A list of strings representing filenames (e.g., ['penguins.csv']).
        """
        return self.repo.list_csv_files()

    def load_file(self, filename):
        """
        Loads data from a specified CSV file into the repository.
        
        :param filename: The name of the file to load (str).
        :return: The number of rows successfully loaded (int).
        """
        return self.repo.load_data(filename)

    def filter_data(self, attribute, value):
        """
        Filters the dataset based on a specific attribute and value.
        For numeric attributes, returns items strictly greater than the value.
        For string attributes, returns items exactly matching the value.
        
        Time Complexity: O(N)
        Space Complexity: O(N)
        
        :param attribute: The attribute to filter by (str).
        :param value: The threshold (for numeric) or match value (for string).
        :return: A list of Penguin objects matching the criteria.
        :raises InvalidAttributeError: If the attribute does not exist.
        :raises ValueError: If a non-numeric value is provided for a numeric attribute.
        """
        self._ensure_data()
        data = self.repo.get_all()
        filtered = []
        
        # Determine if numeric based on the first item
        try:
            first_val = data[0].get_attr(attribute)
            is_numeric = isinstance(first_val, (int, float))
        except InvalidAttributeError:
            raise InvalidAttributeError(f"Attribute {attribute} invalid.")

        if is_numeric:
            try:
                numeric_val = float(value)
                filtered = [p for p in data if p.get_attr(attribute) > numeric_val]
            except ValueError:
                raise ValueError("Numeric value required.")
        else:
            filtered = [p for p in data if str(p.get_attr(attribute)) == value]
            
        return filtered

    def save_filtered_data(self, filename, data):
        """
        Saves a list of Penguin objects to a CSV file.
        
        :param filename: The name of the file to save to (str).
        :param data: The list of Penguin objects to save.
        :return: The final filename used (including .csv extension).
        """
        if not filename.endswith('.csv'): filename += '.csv'
        self.repo.save_data(filename, data)
        return filename

    def describe_attribute(self, attribute):
        """
        Computes statistics (min, max, mean) for a numeric attribute.
        
        Time Complexity: O(N)
        Space Complexity: O(1)
        
        :param attribute: The numeric attribute to describe (str).
        :return: A dictionary with keys 'min', 'max', and 'mean'.
        :raises ValueError: If the attribute is non-numeric.
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        val = data[0].get_attr(attribute)
        if not isinstance(val, (int, float)):
            raise ValueError(f"Attribute '{attribute}' is non-numeric.")

        values = [p.get_attr(attribute) for p in data]
        return {
            "min": min(values), 
            "max": max(values), 
            "mean": sum(values) / len(values)
        }

    def unique_counts(self, attribute):
        """
        Counts the occurrences of each unique value for a given attribute.
        
        Time Complexity: O(N)
        Space Complexity: O(U) where U is the number of unique values.
        
        :param attribute: The attribute to count (str).
        :return: A dictionary mapping unique values to their counts.
        """
        self._ensure_data()
        counts = {}
        for p in self.repo.get_all():
            val = p.get_attr(attribute)
            counts[val] = counts.get(val, 0) + 1
        return counts

    # [Requirement: Sorting & Bonus 3]
    def get_sorting_report(self):
        """
        [Bonus 3] Reads sorting_log.csv and calculates average times.
        """
        log_file = os.path.join(self.repo.directory, 'sorting_log.csv')
        
        if not os.path.exists(log_file):
            return "No sorting log found. Run some 'sort' commands first!"
        
        report_data = {} 
        
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    n = int(row['number_of_rows'])
                    algo = row['sorting_algorithm']
                    duration = float(row['execution_time_in_seconds'])
                    
                    if n < 100: cat = "< 100"
                    elif 500 <= n <= 1000: cat = "500-1000"
                    elif 1000 < n <= 2000: cat = "1000-2000"
                    elif 5000 <= n <= 10000: cat = "5000-10000"
                    elif n > 10000: cat = "> 10000"
                    else: cat = "Other"
                    
                    if cat not in report_data: report_data[cat] = {}
                    if algo not in report_data[cat]: report_data[cat][algo] = []
                    report_data[cat][algo].append(duration)
                except ValueError:
                    continue 

        # Format the output
        output = ["\n--- Sorting Performance Report ---"]
        categories = ["< 100", "500-1000", "1000-2000", "5000-10000", "> 10000", "Other"]
        
        for cat in categories:
            if cat in report_data:
                output.append(f"\nDataset Size: {cat}")
                for algo, times in report_data[cat].items():
                    avg_time = sum(times) / len(times)
                    output.append(f"  - {algo}: {avg_time:.6f} sec (avg of {len(times)} runs)")
        
        return "\n".join(output)
    
    def sort_data(self, attribute, order, algorithm="selection"):
        """
        Sorts the dataset based on an attribute and logs the performance.
        
        Time Complexity: Depends on Algorithm (O(N^2) or O(N log N))
        Space Complexity: O(N) (due to copying the list)
        
        :param attribute: The attribute to sort by (str).
        :param order: 'asc' for ascending or 'desc' for descending.
        :param algorithm: The algorithm to use ('bubble', 'insertion', 'selection', 'quick', 'merge').
        :return: A new list of sorted Penguin objects.
        """
        self._ensure_data()
        data = self.repo.get_all()[:] 
        
        reverse = (order == 'desc')
        start_time = time.time()
        
        if algorithm == 'bubble':
            sorted_data = self._bubble_sort(data, attribute, reverse)
        elif algorithm == 'insertion':
            sorted_data = self._insertion_sort(data, attribute, reverse)
        elif algorithm == 'selection':
            sorted_data = self._selection_sort(data, attribute, reverse)
        elif algorithm == 'quick':
            sorted_data = self._quick_sort(data, attribute, reverse)
        elif algorithm == 'merge':
            sorted_data = self._merge_sort(data, attribute, reverse)
        else:
            raise ValueError("Unknown algorithm.")

        end_time = time.time()
        duration = end_time - start_time
        
        log_entry = {
            'date_of_run': datetime.date.today(),
            'time_of_run': datetime.datetime.now().strftime("%H:%M:%S"),
            'number_of_rows': len(data),
            'sorting_algorithm': algorithm,
            'execution_time_in_seconds': f"{duration:.6f}"
        }
        self.repo.log_sorting_performance(log_entry)
        
        return sorted_data

    # --- A. Bubble Sort O(N^2) ---
    def _bubble_sort(self, data, attr, reverse):
        """
        Implements the Bubble Sort algorithm.
        
        :param data: List of Penguin objects.
        :param attr: Attribute to sort by.
        :param reverse: Boolean, True for descending order.
        :return: Sorted list.
        """
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                val1 = data[j].get_attr(attr)
                val2 = data[j+1].get_attr(attr)
                if (val1 < val2) if reverse else (val1 > val2):
                    data[j], data[j+1] = data[j+1], data[j]
        return data

    # --- B. Insertion Sort O(N^2) ---
    def _insertion_sort(self, data, attr, reverse):
        """
        Implements the Insertion Sort algorithm.
        
        :param data: List of Penguin objects.
        :param attr: Attribute to sort by.
        :param reverse: Boolean, True for descending order.
        :return: Sorted list.
        """
        for i in range(1, len(data)):
            key_item = data[i]
            key_val = key_item.get_attr(attr)
            j = i - 1
            while j >= 0:
                curr_val = data[j].get_attr(attr)
                if (key_val > curr_val) if reverse else (key_val < curr_val):
                    data[j + 1] = data[j]
                    j -= 1
                else:
                    break
            data[j + 1] = key_item
        return data

    # --- C. Selection Sort O(N^2) ---
    def _selection_sort(self, data, attr, reverse):
        """
        Implements the Selection Sort algorithm.
        
        :param data: List of Penguin objects.
        :param attr: Attribute to sort by.
        :param reverse: Boolean, True for descending order.
        :return: Sorted list.
        """
        for i in range(len(data)):
            idx = i
            for j in range(i+1, len(data)):
                val_j = data[j].get_attr(attr)
                val_idx = data[idx].get_attr(attr)
                if (val_j > val_idx) if reverse else (val_j < val_idx):
                    idx = j
            data[i], data[idx] = data[idx], data[i]
        return data

    # --- D. Quick Sort O(N log N) ---
    def _quick_sort(self, data, attr, reverse):
        """
        Implements the Quick Sort algorithm recursively.
        
        :param data: List of Penguin objects.
        :param attr: Attribute to sort by.
        :param reverse: Boolean, True for descending order.
        :return: Sorted list.
        """
        if len(data) <= 1:
            return data
        
        pivot = data[len(data) // 2]
        pivot_val = pivot.get_attr(attr)
        
        left = []
        middle = []
        right = []

        for x in data:
            val = x.get_attr(attr)
            if val == pivot_val:
                middle.append(x)
            elif (val > pivot_val) if reverse else (val < pivot_val):
                left.append(x)
            else:
                right.append(x)
        
        return self._quick_sort(left, attr, reverse) + middle + self._quick_sort(right, attr, reverse)

    # --- E. Merge Sort O(N log N) ---
    def _merge_sort(self, data, attr, reverse):
        """
        Implements the Merge Sort algorithm recursively.
        
        :param data: List of Penguin objects.
        :param attr: Attribute to sort by.
        :param reverse: Boolean, True for descending order.
        :return: Sorted list.
        """
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self._merge_sort(data[:mid], attr, reverse)
        right = self._merge_sort(data[mid:], attr, reverse)
        
        return self._merge(left, right, attr, reverse)

    def _merge(self, left, right, attr, reverse):
        """
        Merges two sorted lists into one sorted list.
        Helper function for Merge Sort.
        
        :param left: First sorted list.
        :param right: Second sorted list.
        :param attr: Attribute to compare.
        :param reverse: Boolean, True for descending order.
        :return: Merged sorted list.
        """
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            val_l = left[i].get_attr(attr)
            val_r = right[j].get_attr(attr)
            
            condition = (val_l > val_r) if reverse else (val_l < val_r)
            if condition or val_l == val_r:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # [Requirement: Augment Data]

    def augment_data(self, percent, method):
        """
        Increases the size of the dataset by a given percentage using a specified method.
        
        :param percent: The percentage to increase the data by (float).
        :param method: 'duplicate' to copy existing rows, or 'create' to generate synthetic ones.
        :return: A tuple containing (new_filename, count_of_added_rows).
        """
        self._ensure_data()
        data = self.repo.get_all()
        count_to_add = int(len(data) * (percent / 100))
        
        new_entries = []
        
        if method == 'duplicate':
            new_entries = random.choices(data, k=count_to_add)
            
        elif method == 'create':
            stats = {}
            for field in ['flipper_length_mm', 'culmen_length_mm', 'culmen_depth_mm', 'body_mass_g']:
                vals = [p.get_attr(field) for p in data]
                stats[field] = (min(vals), max(vals))
            
            species_opts = list(set(p.species for p in data))
            island_opts = list(set(p.island for p in data))
            sex_opts = list(set(p.sex for p in data))
            
            for _ in range(count_to_add):
                p = Penguin(
                    species=random.choice(species_opts),
                    island=random.choice(island_opts),
                    flipper_length=random.uniform(*stats['flipper_length_mm']),
                    culmen_length=random.uniform(*stats['culmen_length_mm']),
                    culmen_depth=random.uniform(*stats['culmen_depth_mm']),
                    body_mass=random.uniform(*stats['body_mass_g']),
                    sex=random.choice(sex_opts)
                )
                new_entries.append(p)
        
        full_list = data + new_entries
        new_filename = f"augmented_{int(time.time())}.csv"
        self.repo.save_data(new_filename, full_list)
        return new_filename, len(new_entries)

    # [Requirement: Plots]

    def generate_scatter(self, attr1, attr2):
        """
        Generates and displays a scatter plot for two attributes using matplotlib.
        
        :param attr1: The attribute for the X-axis (str).
        :param attr2: The attribute for the Y-axis (str).
        :return: None
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        try:
            x = [p.get_attr(attr1) for p in data]
            y = [p.get_attr(attr2) for p in data]
        except ValueError:
            raise InvalidAttributeError("Scatter plot requires numeric attributes.")

        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='navy', alpha=0.6)
        plt.xlabel(attr1)
        plt.ylabel(attr2)
        plt.title(f"Scatter Plot: {attr1} vs {attr2}")
        plt.grid(True)
        plt.show()

    def generate_hist(self, attr, bins):
        """
        Generates and displays a histogram for a numeric attribute.
        
        :param attr: The attribute to plot (str).
        :param bins: The number of bins for the histogram (int).
        :return: None
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        try:
            values = [p.get_attr(attr) for p in data]
        except ValueError:
            raise InvalidAttributeError("Histogram requires numeric attribute.")

        plt.figure(figsize=(10, 6))
        plt.hist(values, bins=bins, color='skyblue', edgecolor='black')
        plt.xlabel(attr)
        plt.ylabel('Frequency')
        plt.title(f"Histogram of {attr}")
        plt.show()

    def generate_boxplot(self, category_attr, value_attr):
        """
        Generates and displays a boxplot showing the distribution of a numeric attribute grouped by a category.
        
        :param category_attr: The categorical attribute (e.g., 'species') (str).
        :param value_attr: The numeric attribute to analyze (e.g., 'body_mass_g') (str).
        :return: None
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        groups = {}
        for p in data:
            cat = p.get_attr(category_attr)
            val = p.get_attr(value_attr)
            if cat not in groups: groups[cat] = []
            groups[cat].append(val)
            
        labels = list(groups.keys())
        values = list(groups.values())

        plt.figure(figsize=(10, 6))
        plt.boxplot(values, labels=labels)
        plt.xlabel(category_attr)
        plt.ylabel(value_attr)
        plt.title(f"Boxplot: {value_attr} by {category_attr}")
        plt.grid(True)
        plt.show()

    # [Bonus 2: k-NN Classifier]

    def classify_penguin(self, c_len, c_depth, f_len, k=5):
        """
        Classifies a penguin into a species based on 3 attributes using the k-Nearest Neighbors algorithm.
        
        :param c_len: Culmen Length (float).
        :param c_depth: Culmen Depth (float).
        :param f_len: Flipper Length (float).
        :param k: The number of neighbors to consider (int).
        :return: The predicted species name (str).
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        distances = []
        for p in data:
            dist = math.sqrt(
                (p.culmen_length_mm - c_len)**2 +
                (p.culmen_depth_mm - c_depth)**2 +
                (p.flipper_length_mm - f_len)**2
            )
            distances.append((dist, p.species))
        
        distances.sort(key=lambda x: x[0])
        nearest = distances[:k]
        
        votes = {}
        for _, species in nearest:
            votes[species] = votes.get(species, 0) + 1
            
        return max(votes, key=votes.get)

    # [Bonus 4: Random Fact]

    def get_random_fact(self):
        """
        Returns a random fact about penguins from a predefined list.
        
        :return: A string containing the fact.
        """
        facts = [
            "Penguins are flightless birds.",
            "The Emperor Penguin is the tallest species.",
            "Penguins live almost exclusively in the Southern Hemisphere.",
            "Penguins swallow pebbles to help digest food.",
            "A group of penguins in the water is called a raft.",
            "Penguins have a gland above their eye to filter salt from water.",
            "The fastest penguin is the Gentoo, reaching 36 km/h.",
            "Penguins lose all their feathers at once (catastrophic molt).",
            "There are no penguins at the North Pole.",
            "Penguin black and white coloring is called countershading.",
            "Some prehistoric penguins were as tall as humans.",
            "Penguins can drink sea water.",
            "Male Emperor penguins incubate eggs for months in the cold.",
            "The smallest species is the Little Blue Penguin.",
            "Penguins spend about half their lives in water."
        ]
        return random.choice(facts)

    # [Bonus 5: ASCII Penguin]

    def get_ascii_penguin(self):
        return r"""
                 .88888888:.
                88888888.88888.
              .8888888888888888.
              888888888888888888
              88' _`88'_  `88888
              88 88 88 88  88888
              88_88_::_88_:88888
              88:::,::,:::::8888
              88`:::::::::'`8888
             .88  `::::'    8:88.
            8888            `8:888.
          .8888'             `888888.
         .8888:..  .::.  ...:'8888888:.
        .8888.'     :'     `'::`88:88888
       .8888        '         `.888:8888.
      888:8         .           888:88888
    .888:88        .:           888:88888:
    8888888.       ::           88:888888
    `.::.888.      ::          .88888888
    .::::::.888.    ::         :::`8888'.:.
    ::::::::::.888  '         .::::::::::::
    ::::::::::::.8    '      .:8::::::::::::.
    ::::::::::::::.        .:888:::::::::::::
    :::::::::::::::88:.__.:88888:::::::::::::
    `::::::::::::::8888888888888::::::::::::'
     `::::::::::::::88888888888::::::::::::'
        """
    # [Lab 13: Random Subset]

    def save_random_subset(self, k, filename):
        """
        Selects k random penguins from the loaded dataset and saves them to a new CSV file.
        
        :param k: The number of penguins to select (int).
        :param filename: The name of the file to save to (str).
        :return: The filename used.
        :raises ValueError: If k is invalid or larger than the dataset.
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        if not isinstance(k, int) or k <= 0:
            raise ValueError("k must be a positive integer.")
        if k > len(data):
            raise ValueError(f"k ({k}) cannot be larger than the dataset size ({len(data)}).")
            
        subset = random.sample(data, k)
        
        if not filename.endswith('.csv'): 
            filename += '.csv'
            
        self.repo.save_data(filename, subset)
        return filename

    # [Lab 13: Backtracking - Research Groups]

    def generate_research_groups(self, k):
        """
        Generates all possible research groups of size k that contain at least one penguin of each species.
        Uses recursive backtracking.
        Constraint: The dataset size must be <= 10.
        
        :param k: The size of the research group (int).
        :return: A list of groups, where each group is a list of Penguin objects.
        :raises ValueError: If the dataset is too large or k < 3.
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        if len(data) > 10:
            raise ValueError("Dataset too large for backtracking (max 10 rows). Filter your data first.")
        if k < 3:
            raise ValueError("Group size k must be at least 3 to cover all species.")
        
        results = []
        
        def backtrack_combinations(start_index, current_group):
            if len(current_group) == k:
                # Must have all 3 species
                species_in_group = {p.species for p in current_group}
                if {'Adelie', 'Gentoo', 'Chinstrap'}.issubset(species_in_group):
                    results.append(list(current_group))
                return

            for i in range(start_index, len(data)):
                current_group.append(data[i])
                backtrack_combinations(i + 1, current_group)
                current_group.pop() # Back

        backtrack_combinations(0, [])
        return results

    # [Lab 13: Backtracking - Split Groups]

    def split_into_groups(self, threshold):
        """
        Generates all possible ways to split the dataset into two valid groups (G1, G2).
        Validity constraints:
        - Each group has at least 2 penguins.
        - Total mass of G1 <= threshold.
        - Total mass of G2 <= threshold.
        Uses recursive backtracking.
        Constraint: The dataset size must be <= 10.
        
        :param threshold: The maximum allowed total mass for a group (float).
        :return: A list of tuples (group1, group2), where each group is a list of Penguin objects.
        :raises ValueError: If the dataset is too large or too small (< 4).
        """
        self._ensure_data()
        data = self.repo.get_all()
        
        if len(data) > 10:
            raise ValueError("Dataset too large for backtracking (max 10 rows).")
        if len(data) < 4:
            raise ValueError("Need at least 4 penguins to split into two groups of size 2+.")

        valid_splits = []
        
        def backtrack_split(index, g1, g2, sum1, sum2):
            if sum1 > threshold or sum2 > threshold:
                return

            if index == len(data):
                if len(g1) >= 2 and len(g2) >= 2:
                    valid_splits.append((list(g1), list(g2)))
                return

            p = data[index]
            mass = p.body_mass_g

            g1.append(p)
            backtrack_split(index + 1, g1, g2, sum1 + mass, sum2)
            g1.pop() 

            if index > 0:
                g2.append(p)
                backtrack_split(index + 1, g1, g2, sum1, sum2 + mass)
                g2.pop() 

        backtrack_split(0, [], [], 0, 0)
        return valid_splits