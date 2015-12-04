"""Builds objects representing a produced factorio item for templating."""

import math

from factorio import recipe
from factorio import production
from factorio import names

from appengine import icons


def get_wiki_url(username):
    """Constructs a URL refering to the factorio wiki given an item name.

    Args:
        username: The English name of a factorio item or recipe e.g.
            'Iron gear wheel'.

    Returns:
        A URL documenting the given factio item.
    """
    return 'http://www.factorioforums.com/wiki/index.php?title=%s' % (
        username.replace(' ', '_'))


class ProductedItem(object):
    """ABC representing a produced item."""
    def __init__(self):
        self.suppliers = {}
        self.consumers = {}

    @property
    def is_user_requested(self):
        """True iff the item was requested directly by the user."""
        return None in self.consumers

    @property
    def name(self):
        """The factorio name of the produced item e.g. 'basic-armor'."""
        raise NotImplementedError()

    @property
    def username(self):
        """The English name of the produced item e.g. 'Iron armor'."""
        return names.get_best_recipe_name(self.name)

    @property
    def icon(self):
        """The URL of an icon representing the produced item."""
        return icons.get_icon_for_item(self.name)

    @property
    def url(self):
        """A URL where the user can get more information about the item."""
        return get_wiki_url(self.username)

    @property
    def required_production_rate(self):
        """A float representing the number of the item which must be produced.

        The time scale is factorio time units.
        """
        return sum(self.consumers.values())

    @property
    def production_machine_username(self):
        """The English name of the machine used to produce the item.

        e.g. 'Chemical plant'. May be None if the produced item is a base
        material such as water.
        """
        raise NotImplementedError()

    @property
    def num_production_machines_required(self):
        """An int representing the number of production machines required.

        The number of production machines required depends on the required
        production rate. May be None if the produced item is a base material
        such as water.
        """
        raise NotImplementedError()


    @property
    def production_machine_icon(self):
        """The URL of an icon representing the production machine.

        May be None if the produced item is a base material such as water.
        """
        raise NotImplementedError()

    @property
    def production_machine_url(self):
        """A URL where the user can get more information about the machine.

        May be None if the produced item is a base material such as water.
        """
        return get_wiki_url(self.production_machine_username)


class BaseProductedItem(ProductedItem):
    """Represents a required base product e.g. water."""

    def __init__(self, name):
        super(BaseProductedItem, self).__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def num_production_machines_required(self):
        return None

    @property
    def production_machine_icon(self):
        return None

    @property
    def production_machine_url(self):
        return None

    @property
    def production_machine_username(self):
        return None


class RecipeProductedItem(ProductedItem):
    """Represents a required product produced from a recipe."""

    def __init__(self, product_recipe):
        super(RecipeProductedItem, self).__init__()
        self._recipe = product_recipe

    @property
    def name(self):
        return self._recipe.name

    @property
    def _producer(self):
        """The production.Producer instance used to manufacture the item.

        May be None if there is no production machine for the items category of
        manufacture e.g. 'crafting'.
        """
        try:
            return production.Producer.get_most_efficient_producer(
                self._recipe.category)
        except KeyError:
            return None

    @property
    def num_production_machines_required(self):
        if self._producer is None:
            return None
        return int(math.ceil(
            self.required_production_rate * self._recipe.crafting_time
            / self._recipe.count_produced
            / self._producer.crafting_speed
            ))

    @property
    def production_machine_icon(self):
        if self._producer is None:
            return None
        return icons.get_icon_for_item(self._producer.name)

    @property
    def production_machine_url(self):
        if self._producer is None:
            return None
        return get_wiki_url(self.production_machine_username)

    @property
    def production_machine_username(self):
        if self._producer is None:
            return None
        return names.get_best_item_name(self._producer.name)


def _leaves_last_sort(products):
    """Order the sequence of ProductedItems with roots first and leaves last."""
    remaining = set(products)
    seen = set()
    result = []
    while remaining:
        new_seen = set(p for p in remaining
                       if all(s in seen for s in p.suppliers))
        result.extend(sorted(new_seen,
                             reverse=True,
                             key=lambda product: product.name))
        seen.update(new_seen)
        remaining.difference_update(new_seen)

    result.reverse()
    return result


def required_production_rates_to_produced_items(required_production_rates):
    """Return a list of ProductedItems representing the production requirements.

    Args:
        required_production_rates: A sequence of 3-tuples
            (<item>, <suppliers>, <consumers>) where <item> is
            the name of the item being produced, <suppliers> is a dictionary
            {<item>: <rate>} of ingredients required to produce the item and
            <consumers> is a dictionary {<item>: <rate>} of items that consume
            this one as part of their production. See factorio.recipe.

    Returns:
        A list of ProductedItems, with one ProductedItem per item in the input
        sequence.
    """
    item_name_to_produced_item = {}
    for item_name, _, _ in required_production_rates:
        if item_name in recipe.REFINED_FLUIDS:
            product = BaseProductedItem(item_name)
        else:
            try:
                product = RecipeProductedItem(
                    recipe.Recipe.get_recipe_by_single_result(item_name))
            except KeyError:
                product = BaseProductedItem(item_name)
        item_name_to_produced_item[item_name] = product

    for item_name, suppliers, consumers in required_production_rates:
        item_name_to_produced_item[item_name].suppliers = {
            item_name_to_produced_item[subitem_name]: rate
            for subitem_name, rate in suppliers.items()}
        item_name_to_produced_item[item_name].consumers = {
            item_name_to_produced_item.get(subitem_name): rate
            for subitem_name, rate in consumers.items()}
    return _leaves_last_sort(item_name_to_produced_item.values())
