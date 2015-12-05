"""Tests for appengine.produced_item."""

import os.path
import unittest

from factorio import names
from factorio import recipe

from appengine import icons
from appengine import produced_item


class TestProducedItem(unittest.TestCase):
    def setUp(self):
        icons.init(os.path.join(os.path.dirname(__file__), 'icons'))
        names.names_from_json(
            open(os.path.join(os.path.dirname(__file__),
                              'test-names.json'), 'r'))
        recipe.Recipe.recipes_from_json(
            open(os.path.join(os.path.dirname(__file__),
                              'test-recipe.json'), 'r'))

    def test_base_product(self):
        rates = recipe.calculate_required_production_rates([('copper-ore', 5)])

        copper_ore_item = (
            produced_item.required_production_rates_to_produced_items(rates)[0])
        self.assertEqual(copper_ore_item.is_user_requested, True)
        self.assertEqual(copper_ore_item.name, 'copper-ore')
        self.assertEqual(copper_ore_item.username, 'Copper ore')
        self.assertEqual(copper_ore_item.icon,
                         '/appengine/tests/icons/copper-ore.png')
        self.assertEqual(
            copper_ore_item.url,
            'http://www.factorioforums.com/wiki/index.php?title=Copper_ore')
        self.assertEqual(copper_ore_item.required_production_rate, 5)
        self.assertIsNone(copper_ore_item.production_machine_username)
        self.assertIsNone(copper_ore_item.num_production_machines_required)
        self.assertIsNone(copper_ore_item.production_machine_icon)
        self.assertIsNone(copper_ore_item.production_machine_url)

    def test_smelting_product(self):
        rates = recipe.calculate_required_production_rates(
            [('copper-plate', 5)])

        copper_plate_item, copper_ore_item = (
            produced_item.required_production_rates_to_produced_items(rates))
        self.assertEqual(copper_plate_item.is_user_requested, True)
        self.assertEqual(copper_plate_item.name, 'copper-plate')
        self.assertEqual(copper_plate_item.username, 'Copper plate')
        self.assertEqual(copper_plate_item.icon,
                         '/appengine/tests/icons/copper-plate.png')
        self.assertEqual(
            copper_plate_item.url,
            'http://www.factorioforums.com/wiki/index.php?title=Copper_plate')
        self.assertEqual(copper_plate_item.required_production_rate, 5)
        self.assertEqual(copper_plate_item.production_machine_username,
                         'Electric furnace')
        # <rate> = <#-machines> * <#-recipe-results> * <machine-speed>
        #          ---------------------------------------------------
        #                        <energy-required>
        # 5 = x * 1 * 2 / 3.5
        # 5 = 4/7x
        # (7/4)5 = x
        # x = 8.75
        self.assertEqual(copper_plate_item.num_production_machines_required, 9)
        self.assertEqual(
            copper_plate_item.production_machine_icon,
            '/appengine/tests/icons/electric-furnace.png')
        self.assertEqual(
            copper_plate_item.production_machine_url,
            'http://www.factorioforums.com/wiki/index.php?title='
            'Electric_furnace')

        self.assertEqual(copper_ore_item.is_user_requested, False)
        self.assertEqual(copper_ore_item.name, 'copper-ore')

    def test_chemistry_product(self):
        rates = recipe.calculate_required_production_rates(
            [('sulfur', 100)])

        sulfur_item, petrolium_gas_item, water_item = (
            produced_item.required_production_rates_to_produced_items(rates))
        self.assertEqual(sulfur_item.is_user_requested, True)
        self.assertEqual(sulfur_item.name, 'sulfur')
        self.assertEqual(sulfur_item.username, 'Sulfur')
        self.assertEqual(sulfur_item.icon,
                         '/appengine/tests/icons/sulfur.png')
        self.assertEqual(
            sulfur_item.url,
            'http://www.factorioforums.com/wiki/index.php?title=Sulfur')
        self.assertEqual(sulfur_item.required_production_rate, 100)
        self.assertEqual(sulfur_item.production_machine_username,
                         'Chemical plant')
        # <rate> = <#-machines> * <#-recipe-results> * <machine-speed>
        #          ---------------------------------------------------
        #                        <energy-required>
        # 100 = x * 2 * 1.25 / 1
        # 100 = 2.5x
        # 100/2.5 = x
        # x = 40
        self.assertEqual(sulfur_item.num_production_machines_required, 40)
        self.assertEqual(
            sulfur_item.production_machine_icon,
            '/appengine/tests/icons/chemical-plant.png')
        self.assertEqual(
            sulfur_item.production_machine_url,
            'http://www.factorioforums.com/wiki/index.php?title='
            'Chemical_plant')

        self.assertEqual(petrolium_gas_item.is_user_requested, False)
        self.assertEqual(petrolium_gas_item.name, 'petroleum-gas')

        self.assertEqual(water_item.is_user_requested, False)
        self.assertEqual(water_item.name, 'water')

    def test_crafting_product(self):
        rates = recipe.calculate_required_production_rates(
            [('copper-cable', 20)])

        copper_cable_item, copper_plate_item, copper_ore_item = (
            produced_item.required_production_rates_to_produced_items(rates))
        self.assertEqual(copper_cable_item.is_user_requested, True)
        self.assertEqual(copper_cable_item.name, 'copper-cable')
        self.assertEqual(copper_cable_item.username, 'Copper cable')
        self.assertEqual(copper_cable_item.icon,
                         '/appengine/tests/icons/copper-cable.png')
        self.assertEqual(
            copper_cable_item.url,
            'http://www.factorioforums.com/wiki/index.php?title=Copper_cable')
        self.assertEqual(copper_cable_item.required_production_rate, 20)
        self.assertEqual(copper_cable_item.production_machine_username,
                         'Assembling machine 3')
        # <rate> = <#-machines> * <#-recipe-results> * <machine-speed>
        #          ---------------------------------------------------
        #                        <energy-required>
        # 20 = x * 2 * 1.25 / 0.5
        # 20 = 5x
        # 20/5 = x
        # x = 4
        self.assertEqual(copper_cable_item.num_production_machines_required, 4)
        self.assertEqual(
            copper_cable_item.production_machine_icon,
            '/appengine/tests/icons/assembling-machine-3.png')
        self.assertEqual(
            copper_cable_item.production_machine_url,
            'http://www.factorioforums.com/wiki/index.php?title='
            'Assembling_machine_3')

        self.assertEqual(copper_plate_item.is_user_requested, False)
        self.assertEqual(copper_plate_item.name, 'copper-plate')

        self.assertEqual(copper_ore_item.is_user_requested, False)
        self.assertEqual(copper_ore_item.name, 'copper-ore')

if __name__ == '__main__':
    unittest.main()
