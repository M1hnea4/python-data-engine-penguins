import unittest
import os
import csv
from unittest.mock import patch
from repository import PenguinRepository
from service import PenguinService
from exceptions import InvalidAttributeError, DataNotLoadedError
from domain import Penguin

# Helper to access unittest assertion methods without a class
tc = unittest.TestCase()
TEST_FILENAME = 'test_penguins_temp.csv'
LAB13_FILENAME = 'test_lab13_temp.csv'

def setup_test_data():
    """Creates a temporary CSV file with known data for testing."""
    headers = ['species', 'flipper_length_mm', 'culmen_length_mm', 
               'culmen_depth_mm', 'body_mass_g', 'island', 'sex']
    
    rows = [
        {'species': 'Adelie', 'flipper_length_mm': '190.0', 'culmen_length_mm': '39.0', 
         'culmen_depth_mm': '18.0', 'body_mass_g': '4000.0', 'island': 'Torgersen', 'sex': 'MALE'},
        {'species': 'Gentoo', 'flipper_length_mm': '220.0', 'culmen_length_mm': '45.0', 
         'culmen_depth_mm': '14.0', 'body_mass_g': '5000.0', 'island': 'Biscoe', 'sex': 'FEMALE'},
        {'species': 'Chinstrap', 'flipper_length_mm': '195.0', 'culmen_length_mm': '41.0', 
         'culmen_depth_mm': '19.0', 'body_mass_g': '3500.0', 'island': 'Dream', 'sex': 'MALE'},
        {'species': 'Adelie', 'flipper_length_mm': '185.0', 'culmen_length_mm': '37.0', 
         'culmen_depth_mm': '17.0', 'body_mass_g': '3700.0', 'island': 'Biscoe', 'sex': 'FEMALE'}
    ]

    with open(TEST_FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def cleanup_test_data():
    """Removes the temporary CSV file and any augmented/log files."""
    if os.path.exists(TEST_FILENAME): os.remove(TEST_FILENAME)
    if os.path.exists(LAB13_FILENAME): os.remove(LAB13_FILENAME)
    
    for f in os.listdir('.'):
        if (f.startswith("augmented_") and f.endswith(".csv")):
            try: os.remove(f)
            except: pass

def get_test_service():
    repo = PenguinRepository()
    repo.load_data(TEST_FILENAME)
    return PenguinService(repo)

# ==========================================
# CORE & BONUS TEST FUNCTIONS
# ==========================================

def test_filter_feature():
    service = get_test_service()
    results = service.filter_data('body_mass_g', 3800)
    tc.assertEqual(len(results), 2, "Filter by mass failed count")
    tc.assertEqual(results[0].body_mass_g, 4000.0)
    tc.assertEqual(results[1].body_mass_g, 5000.0)
    results = service.filter_data('species', 'Adelie')
    tc.assertEqual(len(results), 2, "Filter by species failed count")

def test_describe_feature():
    service = get_test_service()
    stats = service.describe_attribute('flipper_length_mm')
    tc.assertEqual(stats['min'], 185.0)
    tc.assertEqual(stats['max'], 220.0)
    tc.assertAlmostEqual(stats['mean'], 197.5, places=3)

def test_unique_feature():
    service = get_test_service()
    counts = service.unique_counts('island')
    tc.assertEqual(counts['Biscoe'], 2)
    tc.assertEqual(counts['Dream'], 1)

def test_sorting_feature():
    service = get_test_service()
    algorithms = ['selection', 'bubble', 'insertion', 'quick', 'merge']
    for algo in algorithms:
        sorted_list = service.sort_data('body_mass_g', 'asc', algo)
        tc.assertEqual(len(sorted_list), 4)
        tc.assertEqual(sorted_list[0].body_mass_g, 3500.0, f"{algo} failed min sort")
        tc.assertEqual(sorted_list[-1].body_mass_g, 5000.0, f"{algo} failed max sort")
    tc.assertTrue(os.path.exists('sorting_log.csv'), "Sorting log was not created")

def test_augment_feature():
    service = get_test_service()
    fname, count = service.augment_data(50, 'duplicate')
    tc.assertEqual(count, 2)
    repo2 = PenguinRepository()
    total = repo2.load_data(fname)
    tc.assertEqual(total, 6)

def test_classifier_feature():
    service = get_test_service()
    prediction = service.classify_penguin(45.0, 14.0, 220.0, k=1)
    tc.assertEqual(prediction, 'Gentoo', f"Classifier expected Gentoo got {prediction}")

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.figure')
def test_plots_feature(mock_fig, mock_show):
    service = get_test_service()
    try:
        service.generate_scatter('culmen_length_mm', 'body_mass_g')
        service.generate_hist('flipper_length_mm', 10)
        service.generate_boxplot('species', 'body_mass_g')
    except Exception as e:
        tc.fail(f"Plotting function crashed: {e}")

# LAB 13 

def test_save_random():
    service = get_test_service()
    filename = service.save_random_subset(2, LAB13_FILENAME)
    tc.assertTrue(os.path.exists(filename))
    repo2 = PenguinRepository()
    count = repo2.load_data(filename)
    tc.assertEqual(count, 2)

def test_research_groups_backtracking():
    service = get_test_service()
    # Test data has all 3 species (Adelie, Gentoo, Chinstrap). Size 4.
    groups = service.generate_research_groups(3)
    tc.assertGreater(len(groups), 0, "Should find at least one group with all 3 species")
    tc.assertEqual(len(groups[0]), 3)
    species = {p.species for p in groups[0]}
    tc.assertTrue({'Adelie', 'Gentoo', 'Chinstrap'}.issubset(species))

def test_split_groups_backtracking():
    service = get_test_service()
    # Masses: 4000, 5000, 3500, 3700. Total 16200.
    splits = service.split_into_groups(10000)
    tc.assertGreater(len(splits), 0, "Should find valid splits")
    g1, g2 = splits[0]
    tc.assertGreaterEqual(len(g1), 2)
    tc.assertGreaterEqual(len(g2), 2)
    tc.assertLessEqual(sum(p.body_mass_g for p in g1), 10000)

def test_backtracking_validations():
    service = get_test_service()
    with tc.assertRaises(ValueError):
        service.generate_research_groups(2)
    
    service.repo._data = [1]*11 
    with tc.assertRaises(ValueError):
        service.generate_research_groups(3)

def test_general_exceptions():
    repo = PenguinRepository()
    service = PenguinService(repo)
    with tc.assertRaises(DataNotLoadedError):
        service.filter_data('species', 'Adelie')
    service = get_test_service()
    with tc.assertRaises(InvalidAttributeError):
        service.filter_data('wing_color', 'blue')
    with tc.assertRaises(ValueError):
        service.describe_attribute('species')

def run_tests():
    try:
        setup_test_data()
        
        # Lab 11/12
        test_filter_feature()
        test_describe_feature()
        test_unique_feature()
        test_sorting_feature()
        test_augment_feature()
        test_classifier_feature()
        test_plots_feature()
        test_general_exceptions()
        
        # Lab 13
        test_save_random()
        test_research_groups_backtracking()
        test_split_groups_backtracking()
        test_backtracking_validations()
        
        print("-" * 40)
        print("--- ALL TESTS PASSED SUCCESSFULLY! ---")
        print("-" * 40)
        
    except AssertionError as e:
        print(f"\n!!! TEST FAILED !!!")
        print(f"Error details: {e}")
    except Exception as e:
        print(f"\n!!! UNEXPECTED ERROR OCCURRED !!!")
        print(e)
    finally:
        cleanup_test_data()

