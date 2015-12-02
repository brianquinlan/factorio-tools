"""Tests for factorio.names."""

import os.path
import unittest

from factorio import names

class TestNames(unittest.TestCase):

    def setUp(self):
        names.names_from_json(
            open(os.path.join(os.path.dirname(__file__),
                              'test-names.json'), 'r'))

    def test_get_best_item_name(self):
        self.assertEqual(names.get_best_item_name('basic-armor'), 'Iron armor')

    def test_get_best_item_name_missing(self):
        self.assertEqual(
            names.get_best_item_name('missing-name'),
            'missing-name')

    def test_get_best_recipe_name(self):
        self.assertEqual(
            names.get_best_recipe_name('light-oil-cracking'),
            'Light oil cracking to petroleum gas')

    def test_get_best_recipe_name_missing_with_item(self):
        self.assertEqual(
            names.get_best_recipe_name('basic-armor'),
            'Iron armor')

    def test_get_best_recipe_name_missing_name_missing(self):
        self.assertEqual(
            names.get_best_recipe_name('missing-name'),
            'missing-name')

if __name__ == '__main__':
    unittest.main()
