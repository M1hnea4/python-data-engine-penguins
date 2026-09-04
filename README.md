# 🐧 Python Data Engineering & K-NN Classifier (Zero-Pandas)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-K--NN-FF6F00?style=for-the-badge)
![Data Visualization](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=for-the-badge)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge)

A comprehensive data processing, visualization, and machine learning engine built entirely from scratch to analyze the Palmer Penguins dataset. **This project was strictly developed without external data manipulation libraries (like Pandas or DataFrames)** to demonstrate a deep understanding of core data structures, algorithmic sorting, and memory management.

### ⚙️ Core Engine Features
* **Custom Data Pipeline:** Built custom CSV parsers and generators to filter, aggregate (`describe`, `unique`), and augment data by manually manipulating Python lists and dictionaries.
* **Algorithmic Sorting Engine:** Implemented custom sorting algorithms (Bubble, Insertion, Selection, Quick, or Merge sort) from scratch, including an automated benchmarking system that logs execution times for datasets scaling past 10,000 records.
* **Machine Learning (Bonus):** Built a custom **K-Nearest Neighbors (k-NN)** classifier from the ground up to predict penguin species based on culmen length, culmen depth, and flipper length.

### 📊 Visualization & UI
* **Graphical User Interface (GUI):** A fully interactive desktop application built to handle all commands intuitively, abstracting the command-line interface.
* **Integrated Data Visualization:** Uses Matplotlib/Seaborn to dynamically generate scatter plots, histograms, and boxplots based on user-defined dynamic attributes.

### 🏗️ Architecture & QA
* Designed using a strict Layered Architecture (`domain`, `repository`, `service`, `ui`, `gui`).
* Handled edge cases using custom exception classes and validated business logic through the `unittest` framework.
