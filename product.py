from factorio import recipe
from factorio import production
from factorio import names

import math
import os.path

class IconStore(object):
    def __init__(self):
        self.m = {}
        icon_dir = os.path.join(os.path.dirname(__file__), 'factorio-data/icons')
        for root, dirs, files in os.walk(icon_dir):
            for f in files:
                self.m[os.path.splitext(f)[0]] = os.path.join(root, f).replace(icon_dir, '')[1:]

    def get(self, name):
        # TODO(brian@sweetapp.com): Some items may not have an icon, use some
        # sort of generic default icon here.
        return self.m.get(name, '')

icons = IconStore()

class Product(object):
    def __init__(self, recipe, name):
        self._recipe = recipe
        self._name = name
        self.suppliers = {}
        self.consumers = {}

    @classmethod
    def from_recipe(cls, recipe):
        return cls(recipe, None)
    
    @classmethod
    def from_name(cls, name):
        return cls(None, name)

    def __repr__(self):
        suppliers = {p.name: count for p, count in self.suppliers.items()}
        consumers = {p.name: count for p, count in self.consumers.items()}
        return '<%s recipe=%r suppliers=%r consumers=%r>' % (
            self.__class__.__name__, self._recipe, suppliers, consumers)

    @property
    def is_user_requested(self):
        return None in self.consumers
    
    @property
    def icon(self):
        return icons.get(self.name)

    @property
    def name(self):
        return self._name or self._recipe.name

    @property
    def url(self):
        return 'http://www.factorioforums.com/wiki/index.php?title=%s' % (self.username.replace(' ', '_'))
    
    @property
    def username(self):
        return names.get_best_recipe_name(self.name)

    @property
    def required_production_rate(self):
        return sum(self.consumers.values())

    @property
    def _producer(self):
        if self._recipe is None:
            return None
        else:
            try:
                return production.Producer.get_most_efficient_producer(
                    self._recipe.category)
            except KeyError:
                return None
    
    @property
    def num_production_machines_required(self):
        if self._producer is None:
            return None
        else:
            return int(math.ceil(
                self.required_production_rate * self._recipe.crafting_time
                / self._recipe.count_produced
                / self._producer.crafting_speed
                ))

    @property
    def production_machine_icon(self):
        if self._producer is None:
            return None
        else:
            return icons.get(self._producer.name)

    @property
    def production_machine_url(self):
        return 'http://www.factorioforums.com/wiki/index.php?title=%s' % (self.production_machine_username.replace(' ', '_'))
    
    @property
    def production_machine_username(self):
        if self._producer is None:
            return None
        else:
            return names.get_best_item_name(self._producer.name)
    

def _leaves_first_sort(products):
    remaining = set(products)
    seen = set()
    o = []
    while remaining:
        new_seen = set(p for p in remaining if all(s in seen for s in p.suppliers))
        o.extend(sorted(new_seen, reverse=True, key=lambda p: p.name))
        seen.update(new_seen)
        remaining.difference_update(new_seen)

    o.reverse()
    return o


def required_production_rates_to_products(required_production_rates):
    r = {}
    for item_name, _, _ in required_production_rates:
        if item_name in recipe.REFINED_FLUIDS:
            product = Product.from_name(item_name)
        else:
            try:
                product = Product.from_recipe(
                    recipe.Recipe.get_recipe_by_single_result(item_name))
            except KeyError:
                product = Product.from_name(item_name)
        r[item_name] = product

    for item_name, suppliers, consumers in required_production_rates:
        r[item_name].suppliers = {r[subitem_name]: rate
                                  for subitem_name, rate in suppliers.items()}
        r[item_name].consumers = {r.get(subitem_name): rate
                                  for subitem_name, rate in consumers.items()}
    return _leaves_first_sort(r.values())