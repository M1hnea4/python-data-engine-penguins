from exceptions import AppError

class ConsoleUI:
    def __init__(self, service):
        """
        Initializes the Console User Interface.

        :param service: An instance of PenguinService that handles the business logic.
        """
        self.service = service

    def start(self):
        """
        Starts the main application loop.
        It continuously reads user commands from the console, parses them, 
        and dispatches them to the appropriate handler methods.
        
        :return: None
        """
        print("Penguin Analyzer Started. Type 'help' for commands.")
        while True:
            try:
                cmd_input = input("> ").strip().split()
                if not cmd_input: continue
                
                cmd = cmd_input[0].lower()
                args = cmd_input[1:]

                if cmd == "quit":
                    break
                elif cmd == "help":
                    self.print_help()
                elif cmd == "print" and args == ["available_data"]:
                    self.handle_print_files()
                elif cmd == "load":
                    self.handle_load(args)
                elif cmd == "filter":
                    self.handle_filter(args)
                elif cmd == "describe":
                    self.handle_describe(args)
                elif cmd == "unique":
                    self.handle_unique(args)
                elif cmd == "sort":
                    self.handle_sort(args)
                elif cmd == "augment":
                    self.handle_augment(args)
                elif cmd == "scatter":
                    self.handle_scatter(args)
                elif cmd == "hist":
                    self.handle_hist(args)
                elif cmd == "boxplot":
                    self.handle_boxplot(args)
                elif cmd == "classify":
                    self.handle_classify(args)
                elif cmd == "random_fact":
                    print(f"Did you know? {self.service.get_random_fact()}")
                elif cmd == "draw_penguin":
                    print(self.service.get_ascii_penguin())
                # --- Lab 13 Commands ---
                elif cmd == "save_random":
                    self.handle_save_random(args)
                elif cmd == "generate" and len(args) > 0 and args[0] == "research_groups":
                    self.handle_research_groups(args)
                elif cmd == "split_into_groups":
                    self.handle_split_groups(args)
                # --- Bonus 3 Command ---
                elif cmd == "sorting_report":
                    self.handle_sorting_report()
                else:
                    print("Unknown command.")
            except Exception as e:
                print(f"Error: {e}")

    def handle_print_files(self):
        """
        Handles the 'print available_data' command.
        Retrieves and prints the list of CSV files in the current directory.
        
        :return: None
        """
        print("Files:", self.service.get_available_files())

    def handle_load(self, args):
        """
        Handles the 'load' command.
        
        :param args: A list containing the filename to load (e.g., ["penguins.csv"]).
        :return: None
        """
        if not args: return print("Usage: load <filename>")
        print(f"Loaded {self.service.load_file(args[0])} rows.")

    def handle_filter(self, args):
        """
        Handles the 'filter' command.
        Filters data by attribute and value, and optionally saves the result.
        
        :param args: A list containing [attribute, value] (e.g., ["species", "Adelie"]).
        :return: None
        """
        if len(args) < 2: return print("Usage: filter <attr> <value>")
        res = self.service.filter_data(args[0], args[1])
        print(f"The number of penguins that meets the criteria: {len(res)}")
        if len(res) == 0: return

        save = input("Do you want to save this data to a new file? (y/n) ").strip().lower()
        if save in ['y', 'yes']:
            fname = input("Please give the filename: ").strip()
            self.service.save_filtered_data(fname, res)
            print(f"The data was saved to file: {fname}.csv")
        else:
            print("Data not saved. Displaying first 5:")
            for p in res[:5]: print(p)

    def handle_describe(self, args):
        """
        Handles the 'describe' command.
        Calculates and prints statistics (min, max, mean) for a numeric attribute.
        
        :param args: A list containing the attribute name (e.g., ["body_mass_g"]).
        :return: None
        """
        if not args: return print("Usage: describe <attr>")
        stats = self.service.describe_attribute(args[0])
        print(f"{args[0]}: min={stats['min']:.2f} max={stats['max']:.2f} mean={stats['mean']:.2f}")

    def handle_unique(self, args):
        """
        Handles the 'unique' command.
        Prints counts of unique values for a given attribute.
        
        :param args: A list containing the attribute name (e.g., ["island"]).
        :return: None
        """
        if not args: return print("Usage: unique <attr>")
        counts = self.service.unique_counts(args[0])
        for k,v in counts.items(): print(f"{k}: {v}")

    def handle_sort(self, args):
        """
        Handles the 'sort' command.
        Sorts the dataset using a specific algorithm and order.
        
        :param args: A list containing [attribute, order, algorithm] (e.g., ["body_mass_g", "asc", "bubble"]).
        :return: None
        """
        if len(args) < 2: return print("Usage: sort <attribute> <asc|desc> [algo]")
        attr, order = args[0], args[1]
        algo = args[2] if len(args) > 2 else "selection"
        try:
            res = self.service.sort_data(attr, order, algo)
            print(f"Sorted {len(res)} rows using {algo}.")
            print("Top 5 results:")
            for p in res[:5]: print(p)
        except ValueError as e: print(str(e))

    def handle_augment(self, args):
        """
        Handles the 'augment' command.
        Increases the dataset size by duplicating or creating data.
        
        :param args: A list containing [percent, method] (e.g., ["50", "duplicate"]).
        :return: None
        """
        if len(args) < 2: return print("Usage: augment <percent> <method>")
        try:
            fname, count = self.service.augment_data(float(args[0]), args[1])
            print(f"Added {count} rows. Saved to {fname}.")
        except Exception as e: print(f"Augment error: {e}")

    def handle_scatter(self, args):
        """
        Handles the 'scatter' command.
        Generates a scatter plot for two attributes.
        
        :param args: A list containing [attr1, attr2] (e.g., ["culmen_length_mm", "body_mass_g"]).
        :return: None
        """
        if len(args) < 2: return print("Usage: scatter <attr1> <attr2>")
        self.service.generate_scatter(args[0], args[1])

    def handle_hist(self, args):
        """
        Handles the 'hist' command.
        Generates a histogram for a numeric attribute.
        
        :param args: A list containing [attribute, bins] (e.g., ["body_mass_g", "10"]).
        :return: None
        """
        if len(args) < 2: return print("Usage: hist <attr> <bins>")
        self.service.generate_hist(args[0], int(args[1]))

    def handle_boxplot(self, args):
        """
        Handles the 'boxplot' command.
        Generates a boxplot grouping a numeric attribute by a category.
        
        :param args: A list containing [category, numeric_attr] (e.g., ["species", "body_mass_g"]).
        :return: None
        """
        if len(args) < 2: return print("Usage: boxplot <category> <numeric>")
        self.service.generate_boxplot(args[0], args[1])

    def handle_classify(self, args):
        """
        Handles the 'classify' command.
        Predicts the species of a penguin based on 3 measurements using k-NN.
        
        :param args: A list containing [c_len, c_depth, f_len, k] (e.g., ["45.0", "15.0", "220.0", "5"]).
        :return: None
        """
        if len(args) < 3: return print("Usage: classify <c_len> <c_depth> <f_len> [k]")
        try:
            k = int(args[3]) if len(args) > 3 else 5
            s = self.service.classify_penguin(float(args[0]), float(args[1]), float(args[2]), k)
            print(f"Predicted Species: {s}")
        except ValueError: print("Attributes must be numeric.")

    def handle_save_random(self, args):
        """
        Handles the 'save_random' command (Lab 13).
        Saves a random subset of k penguins to a new file.
        
        :param args: A list containing [k, filename] (e.g., ["5", "small_test.csv"]).
        :return: None
        """
        if len(args) < 2:
            print("Usage: save_random <k> <filename>")
            return
        try:
            k = int(args[0])
            fname = args[1]
            saved_name = self.service.save_random_subset(k, fname)
            print(f"Successfully saved {k} random penguins to '{saved_name}'.")
        except Exception as e:
            print(f"Error: {e}")

    def handle_research_groups(self, args):
        """
        Handles the 'generate research_groups' command (Lab 13).
        Uses backtracking to find groups of size k with all 3 species.
        
        :param args: A list containing ["research_groups", k] (e.g., ["research_groups", "3"]).
        :return: None
        """
        if len(args) < 2:
            print("Usage: generate research_groups <k>")
            return
        try:
            k = int(args[1])
            groups = self.service.generate_research_groups(k)
            
            if not groups:
                print("No valid research groups found.")
            else:
                print(f"Found {len(groups)} valid groups:")
                for i, grp in enumerate(groups, 1):
                    names = [f"{p.species}({p.island})" for p in grp]
                    print(f"Group {i}: {', '.join(names)}")
        except Exception as e:
            print(f"Error: {e}")

    def handle_split_groups(self, args):
        """
        Handles the 'split_into_groups' command (Lab 13).
        Uses backtracking to split penguins into 2 groups under a weight threshold.
        
        :param args: A list containing [threshold] (e.g., ["15000"]).
        :return: None
        """
        if len(args) < 1:
            print("Usage: split_into_groups <threshold>")
            return
        try:
            threshold = float(args[0])
            splits = self.service.split_into_groups(threshold)
            
            if not splits:
                print("No valid splits found.")
            else:
                print(f"Found {len(splits)} valid ways to split:")
                for i, (g1, g2) in enumerate(splits, 1):
                    sum1 = sum(p.body_mass_g for p in g1)
                    sum2 = sum(p.body_mass_g for p in g2)
                    print(f"Split {i}:")
                    print(f"  Group 1 (n={len(g1)}, sum={sum1}): {[p.species for p in g1]}")
                    print(f"  Group 2 (n={len(g2)}, sum={sum2}): {[p.species for p in g2]}")
                    print("-" * 20)
        except Exception as e:
            print(f"Error: {e}")

    def handle_sorting_report(self):
        """
        Handles the 'sorting_report' command (Bonus 3).
        Prints the average execution times for sorting algorithms from the log file.
        
        :return: None
        """
        print(self.service.get_sorting_report())

    def print_help(self):
        """
        Prints the list of all available commands and usage instructions.
        
        :return: None
        """
        print("""Commands:
 - load <file>
 - filter <attr> <val>
 - describe <attr>
 - unique <attr>
 - sort <attr> <asc|desc> [algo]
 - augment <percent> <duplicate|create>
 - scatter <attr1> <attr2>
 - hist <attr> <bins>
 - boxplot <species|island> <attr>
 - classify <c_len> <c_depth> <f_len>
 - save_random <k> <filename>
 - generate research_groups <k>
 - split_into_groups <threshold>
 - sorting_report
 - random_fact
 - draw_penguin
 - quit""")