import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from repository import PenguinRepository
from service import PenguinService

class PenguinGUI:
    def __init__(self, root):
        """
        Initializes the GUI Application.
        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Penguin Manager GUI")
        self.root.geometry("650x550")
        self.repo = PenguinRepository()
        self.service = PenguinService(self.repo)
        self.create_widgets()

    def create_widgets(self):
        """Creates and places all UI elements (buttons, text area) on the window."""

        # This is where logs and results will appear
        self.txt_output = scrolledtext.ScrolledText(self.root, height=18, font=("Consolas", 10))
        self.txt_output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        # Basic File Operations
        tk.Button(btn_frame, text="Load Data", command=self.load_data, width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Filter Data", command=self.filter_data, width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Sort Data", command=self.sort_data, width=15).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(btn_frame, text="Describe Attr", command=self.describe_attr, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Augment Data", command=self.augment_data, width=15).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Unique Counts", command=self.unique_counts, width=15).grid(row=1, column=2, padx=5, pady=5)

        # Visualization
        tk.Button(btn_frame, text="Scatter Plot", command=self.plot_scatter, width=15).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Histogram", command=self.plot_hist, width=15).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Boxplot", command=self.plot_boxplot, width=15).grid(row=2, column=2, padx=5, pady=5)
 
        tk.Button(btn_frame, text="Classify (B2)", command=self.classify, width=15).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Sorting Rpt (B3)", command=self.sorting_report, width=15).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Random Fact (B4)", command=self.show_fact, width=15).grid(row=3, column=2, padx=5, pady=5)

        tk.Button(btn_frame, text="ASCII Art (B5)", command=self.show_ascii, width=15).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Quit", command=self.root.quit, width=15, bg="#ffcccc").grid(row=4, column=2, padx=5, pady=5)

    def log(self, msg):
        """Helper to print messages to the text area."""
        self.txt_output.insert(tk.END, msg + "\n" + "-"*40 + "\n")
        self.txt_output.see(tk.END)

    # Button Handlers

    def load_data(self):
        fname = simpledialog.askstring("Input", "Enter filename (e.g., penguins_data.csv):")
        if fname:
            try:
                count = self.service.load_file(fname)
                self.log(f"Successfully loaded {count} rows.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def filter_data(self):
        attr = simpledialog.askstring("Input", "Attribute (e.g., species):")
        val = simpledialog.askstring("Input", "Value (e.g., Adelie):")
        if attr and val:
            try:
                res = self.service.filter_data(attr, val)
                self.log(f"Found {len(res)} matching items.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def describe_attr(self):
        attr = simpledialog.askstring("Input", "Attribute (e.g., body_mass_g):")
        if attr:
            try:
                stats = self.service.describe_attribute(attr)
                self.log(f"Stats for {attr}: {stats}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def unique_counts(self):
        attr = simpledialog.askstring("Input", "Attribute (e.g., island):")
        if attr:
            try:
                counts = self.service.unique_counts(attr)
                self.log(f"Unique counts for {attr}:\n{counts}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def sort_data(self):
        attr = simpledialog.askstring("Input", "Attribute:")
        algo = simpledialog.askstring("Input", "Algorithm (bubble/selection/quick/merge/insertion):", initialvalue="selection")
        if attr and algo:
            try:
                res = self.service.sort_data(attr, 'asc', algo)
                self.log(f"Sorted {len(res)} rows using {algo}. Top item:\n{res[0]}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def sorting_report(self):
        try:
            report = self.service.get_sorting_report()
            self.log(report)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def augment_data(self):
        pct = simpledialog.askfloat("Input", "Percentage (e.g. 20):")
        if pct:
            try:
                fname, count = self.service.augment_data(pct, 'create')
                self.log(f"Created {count} new penguins in {fname}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def plot_scatter(self):
        a1 = simpledialog.askstring("Input", "Attribute X:")
        a2 = simpledialog.askstring("Input", "Attribute Y:")
        if a1 and a2:
            try:
                self.service.generate_scatter(a1, a2)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def plot_hist(self):
        attr = simpledialog.askstring("Input", "Attribute:")
        bins = simpledialog.askinteger("Input", "Bins (e.g., 10):", initialvalue=10)
        if attr and bins:
            try:
                self.service.generate_hist(attr, bins)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def plot_boxplot(self):
        cat = simpledialog.askstring("Input", "Category (e.g., species):")
        val = simpledialog.askstring("Input", "Value (e.g., body_mass_g):")
        if cat and val:
            try:
                self.service.generate_boxplot(cat, val)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def show_fact(self):
        self.log(f"Fact: {self.service.get_random_fact()}")

    def show_ascii(self):
        self.log(self.service.get_ascii_penguin())

    def classify(self):
        vals = simpledialog.askstring("Input", "c_len, c_depth, f_len (space separated):")
        if vals:
            try:
                parts = vals.split()
                if len(parts) < 3: raise ValueError("Need 3 values.")
                s = self.service.classify_penguin(float(parts[0]), float(parts[1]), float(parts[2]))
                self.log(f"Prediction: {s}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PenguinGUI(root)
    root.mainloop()