from __future__ import division

import os
import json
import pprint


REFINED_FLUIDS = ['heavy-oil', 'light-oil', 'petroleum-gas']


class Recipe:
    recipes_by_name = {}
    recipes_by_single_result = {}

    @classmethod
    def from_json(cls, obj):
        assert obj['type'] == 'recipe'

        if 'result' in obj or ('results' in obj and len(obj['results']) == 1):
            return SingleResultRecipe.from_json(obj)
        # assert False, 'Unexpected recipe: %r' % obj

    @classmethod
    def recipes_from_json(cls, json_stream):
        recipe_objects = json.load(json_stream)
        for recipe_object in recipe_objects.values():
            recipe = Recipe.from_json(recipe_object)
            if recipe is None:
                continue
            cls.recipes_by_name[recipe.name] = recipe
            if isinstance(recipe, SingleResultRecipe):
                cls.recipes_by_single_result[recipe.result] = recipe

    @classmethod
    def get_recipe_by_name(cls, name):
        return cls.recipes_by_name[name]

    @classmethod
    def get_recipe_by_single_result(cls, name):
        return cls.recipes_by_single_result[name]


class SingleResultRecipe(Recipe):
    def __init__(self,
                 name,
                 ingredients,
                 result,
                 result_type,
                 category='crafting',
                 crafting_time=0.5,
                 count_produced=1):
        self.name = name
        self.category = category
        self.crafting_time = crafting_time
        self.ingredients = ingredients
        self.result = result
        self.result_type = result_type
        self.count_produced = count_produced
    
    def __repr__(self):
        return (
            '<%s(name=%r result=%r crafting_time=%r category=%r, '
            'ingredients=%r count_produced=%r)' % (
                self.__class__.__name__,
                self.name,
                self.result,
                self.crafting_time,
                self.category,
                self.ingredients,
                self.count_produced))

    def crafting_rate(self):
        return self.count_produced / self.crafting_time

    @classmethod
    def from_json(cls, obj):
        assert obj['type'] == 'recipe', 'expected recipe, got %r, %r' % (
            obj['type'], obj)

        if 'results' in obj:
            assert len(obj['results']) == 1, (
                'only a single result is allowed: %r' % obj)
            result = obj['results'][0]['name']
            count_produced = obj['results'][0]['amount']
            result_type = obj['results'][0]['type']
        else:
            result = obj['result']
            count_produced = obj.get('result_count', 1)
            result_type = None

        ingredients = {}
        for ingredient in obj['ingredients']:
            if isinstance(ingredient, dict):
                ingredients[ingredient['name']] = ingredient['amount']
            else:
                ingredients[ingredient[0]] = ingredient[1]
        return cls(name=obj['name'],
                   ingredients=ingredients,
                   result=result,
                   result_type=result_type,
                   category=obj.get('category', 'crafting'),
                   crafting_time=obj.get('energy_required', 0.5),
                   count_produced=count_produced)


class _ProductionNode(object):
    def __init__(self, item_name):
        self.item_name = item_name
        self.suppliers = {}
        self.consumers = {}

    def add_supplier(self, item_name, required_rate):
        self.suppliers[item_name] = self.suppliers.get(
            item_name, 0) + required_rate

    def add_requirement(self, item_name, required_rate):
        self.consumers[item_name] = self.consumers.get(
            item_name, 0) + required_rate


def calculate_required_production_rates(items_and_crafting_rates):
    requirements = {}
    for item_name, required_crafting_rate in items_and_crafting_rates:
        _update_requirements(
            None, item_name, required_crafting_rate, requirements)
    return sorted([(r.item_name, r.suppliers, r.consumers)
                   for r in requirements.values()], key=lambda o: o[0])


def _update_requirements(parent_name,
                         item_name,
                         required_crafting_rate,
                         production_node_to_required_rate):
    if parent_name:
        production_node_to_required_rate.setdefault(
            parent_name, _ProductionNode(parent_name)).add_supplier(
                item_name, required_crafting_rate)

    if item_name in REFINED_FLUIDS:
        production_node_to_required_rate.setdefault(
            item_name, _ProductionNode(item_name)).add_requirement(
                parent_name, required_crafting_rate)
        return        
    try:
        item = Recipe.get_recipe_by_single_result(item_name)
    except KeyError:
        production_node_to_required_rate.setdefault(
            item_name, _ProductionNode(item_name)).add_requirement(
                parent_name, required_crafting_rate)
        return

    production_node_to_required_rate.setdefault(
        item_name, _ProductionNode(item_name)).add_requirement(
            parent_name, required_crafting_rate)

    for subitem_name, count in item.ingredients.items():
        _update_requirements(
            item_name,
            subitem_name,
            count * required_crafting_rate / item.count_produced,
            production_node_to_required_rate)


if __name__ == '__main__':
    Recipe.recipes_from_json(open('recipes.json', 'r'))
    requirements = calculate_required_production_rates([('plastic-bar', 1)])
    # requirements = foo([('power-armor-mk2', 1)])
    pprint.pprint(requirements)


'''
crafting speeds:
../entity/entities.lua

/Applications/factorio.app/Contents/data/base/graphics/icons

Electric Furnace base crafting speed is 2
Crafting Iron Plate has a base time of 3.5
Crafting Steel Plate has a base time of 17.5 and consumes 5 Iron Plate

  {
    type = "recipe",
    name = "iron-plate",
    category = "smelting",
    energy_required = 3.5,
    ingredients = {{"iron-ore", 1}},
    result = "iron-plate"
  },

  {
    type = "recipe",
    name = "iron-gear-wheel",
    ingredients = {{"iron-plate", 2}},
    result = "iron-gear-wheel"
  },

  {
    type = "recipe",
    name = "basic-transport-belt",
    ingredients =
    {
      {"iron-plate", 1},
      {"iron-gear-wheel", 1}
    },
    result = "basic-transport-belt",
    result_count = 2
  },

  {
    type = "recipe",
    name = "fast-transport-belt",
    enabled = false,
    ingredients =
    {
      {"iron-gear-wheel", 5},
      {"basic-transport-belt", 1}
    },
    result = "fast-transport-belt"
  },
'''