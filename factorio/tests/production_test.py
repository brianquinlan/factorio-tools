import os.path
import unittest

from factorio import production

class TestProduction(unittest.TestCase):


    def test_get_most_efficient_crafting_machine(self):
        assembling_machine_3 = production.Producer.get_most_efficient_producer('crafting')
        self.assertEqual(assembling_machine_3.name, 'assembling-machine-3')
        self.assertEqual(
            assembling_machine_3.crafting_categories,
            {'crafting', 'crafting-with-fluid', 'advanced-crafting'})
        self.assertEqual(assembling_machine_3.crafting_speed, 1.25)


if __name__ == '__main__':
    unittest.main()