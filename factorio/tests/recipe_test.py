import os.path
import unittest

from factorio import recipe

class TestRecipe(unittest.TestCase):

    def setUp(self):
        recipe.Recipe.recipes_from_json(
            open(os.path.join(os.path.dirname(__file__),
                              'test-recipe.json'), 'r'))

    def test_correct_craft_load(self):
        copper_recipe = recipe.Recipe.get_recipe_by_name('copper-cable')
        self.assertEqual(copper_recipe.name, 'copper-cable')
        self.assertEqual(copper_recipe.category, 'crafting')
        self.assertEqual(copper_recipe.crafting_time, 0.5)
        self.assertEqual(copper_recipe.ingredients, {'copper-plate': 1})
        self.assertEqual(copper_recipe.result, 'copper-cable')
        self.assertEqual(copper_recipe.result_type, None)
        self.assertEqual(copper_recipe.count_produced, 2)

    def test_correct_crafting_with_fluid(self):
        engine_recipe = recipe.Recipe.get_recipe_by_name('electric-engine-unit')
        self.assertEqual(engine_recipe.name, 'electric-engine-unit')
        self.assertEqual(engine_recipe.category, 'crafting-with-fluid')
        self.assertEqual(engine_recipe.crafting_time, 20)
        self.assertEqual(engine_recipe.ingredients, {'electronic-circuit': 2,
          'engine-unit': 1,
          'lubricant': 2})
        self.assertEqual(engine_recipe.result, 'electric-engine-unit')
        self.assertEqual(engine_recipe.result_type, None)
        self.assertEqual(engine_recipe.count_produced, 1)

    def test_correct_chemistry_load(self):
        plastic_bar_recipe = recipe.Recipe.get_recipe_by_name('plastic-bar')
        self.assertEqual(plastic_bar_recipe.name, 'plastic-bar')
        self.assertEqual(plastic_bar_recipe.category, 'chemistry')
        self.assertEqual(plastic_bar_recipe.crafting_time, 1)
        self.assertEqual(plastic_bar_recipe.ingredients, 
                         {'coal': 1, 'petroleum-gas': 3})
        self.assertEqual(plastic_bar_recipe.result, 'plastic-bar')
        self.assertEqual(plastic_bar_recipe.result_type, 'item')
        self.assertEqual(plastic_bar_recipe.count_produced, 2)

    def test_calculate_required_production_rates(self):
        required_rates = recipe.calculate_required_production_rates(
            [('electronic-circuit', 2)])
        self.assertEqual(
            required_rates,
            [('copper-cable',
              {'copper-plate': 3.0},
              {'electronic-circuit': 6.0}),
             ('copper-ore', {}, {'copper-plate': 3.0}),
             ('copper-plate', {'copper-ore': 3.0}, {'copper-cable': 3.0}),
             ('electronic-circuit',
              {'copper-cable': 6.0, 'iron-plate': 2.0},
              {None: 2}),
             ('iron-ore', {}, {'iron-plate': 2.0}),
             ('iron-plate', {'iron-ore': 2.0}, {'electronic-circuit': 2.0})])

    def test_calculate_required_production_rates_complex_chain(self):
        required_rates = recipe.calculate_required_production_rates(
            [('destroyer-capsule', 1)])

        # Calculated from:
        # A) http://www.factorioforums.com/wiki/index.php?title=Destroyer_capsule
        # B) http://www.factorioforums.com/wiki/index.php?title=Plastic_bar
        # C) http://www.factorioforums.com/wiki/index.php?title=Steel_Plate
        self.assertEqual(
            required_rates,
            [('advanced-circuit',
              {'copper-cable': 68.0,
               'electronic-circuit': 34.0,
               'plastic-bar': 34.0},
              {'distractor-capsule': 12.0, 'speed-module': 5.0}),
             ('coal', {}, {'plastic-bar': 17.0}), # B
             ('copper-cable',
              {'copper-plate': 140.5},
              {'advanced-circuit': 68.0, 'electronic-circuit': 213.0}),
             ('copper-ore', {}, {'copper-plate': 220.5}),
             ('copper-plate',
              {'copper-ore': 220.5},
              {'copper-cable': 140.5, 'piercing-bullet-magazine': 80.0}),  # A
             ('defender-capsule',
              {'electronic-circuit': 32.0,
               'iron-gear-wheel': 48.0,
               'piercing-bullet-magazine': 16.0},
              {'distractor-capsule': 16.0}),
             ('destroyer-capsule',
              {'distractor-capsule': 4.0, 'speed-module': 1.0},
              {None: 1}),
             ('distractor-capsule',
              {'advanced-circuit': 12.0, 'defender-capsule': 16.0},
              {'destroyer-capsule': 4.0}),
             ('electronic-circuit',
              {'copper-cable': 213.0, 'iron-plate': 71.0},
              {'advanced-circuit': 34.0,
               'defender-capsule': 32.0,
               'speed-module': 5.0}),
             ('iron-gear-wheel',
              {'iron-plate': 96.0},
              {'defender-capsule': 48.0}),
             ('iron-ore', {}, {'iron-plate': 247.0}),
             ('iron-plate',
              {'iron-ore': 247.0},
              {'electronic-circuit': 71.0,  # A
               'iron-gear-wheel': 96.0,     # A
               'steel-plate': 80.0}),       # C
             ('petroleum-gas', {}, {'plastic-bar': 51.0}),  # B
             ('piercing-bullet-magazine',
              {'copper-plate': 80.0, 'steel-plate': 16.0},
              {'defender-capsule': 16.0}),
             ('plastic-bar',
              {'coal': 17.0, 'petroleum-gas': 51.0},
              {'advanced-circuit': 34.0}),  # A
             ('speed-module',
              {'advanced-circuit': 5.0, 'electronic-circuit': 5.0},
              {'destroyer-capsule': 1.0}),  # A
             ('steel-plate',
              {'iron-plate': 80.0},
              {'piercing-bullet-magazine': 16.0})])  # A

    def test_calculate_required_production_rates_overlapping_dependencies(self):
        # 'iron-plate' is used by 'basic-inserter', 'electronic-circuit' and
        # 'iron-gear-wheel'
        required_rates = recipe.calculate_required_production_rates(
            [('basic-inserter', 5)])
        self.assertEqual(
            required_rates,
            [('basic-inserter',
              {'electronic-circuit': 5.0,
               'iron-gear-wheel': 5.0,
               'iron-plate': 5.0},
              {None: 5}),
             ('copper-cable',
              {'copper-plate': 7.5},
              {'electronic-circuit': 15.0}),
             ('copper-ore', {}, {'copper-plate': 7.5}),
             ('copper-plate', {'copper-ore': 7.5}, {'copper-cable': 7.5}),
             ('electronic-circuit',
              {'copper-cable': 15.0, 'iron-plate': 5.0},
              {'basic-inserter': 5.0}),
             ('iron-gear-wheel',
              {'iron-plate': 10.0},
              {'basic-inserter': 5.0}),             
             ('iron-ore', {}, {'iron-plate': 20.0}),
             ('iron-plate',
              {'iron-ore': 20.0},
              {'basic-inserter': 5.0,
               'electronic-circuit': 5.0,
               'iron-gear-wheel': 10.0})])


if __name__ == '__main__':
    unittest.main()