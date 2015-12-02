"""Maps internal factorio names to English names.

For example
    'basic-armor' => 'Iron Armor'.
    'heavy-oil-cracking' => 'Heavy oil cracking to light oil'
"""

import json

_ITEM_NAMES = None
_RECIPE_NAMES = None


def names_from_json(json_stream):
    """Loads the names from a stream containing JSON data."""
    global _ITEM_NAMES, _RECIPE_NAMES
    names = json.load(json_stream)
    _ITEM_NAMES = names['item-names']
    _RECIPE_NAMES = names['recipe-names']


def get_best_item_name(item_id):
    """Returns the best English name for an item.

    Args:
        item_id: The internal factorio name of an item e.g. 'basic-armor'.

    Returns:
        The English name of the item (e.g. 'Iron Armor'). If no user-friendly
        name is available then the input name is returned.
    """
    return _ITEM_NAMES.get(item_id, item_id)


def get_best_recipe_name(recipe_id):
    """Returns the best English name for a recipe.

    Args:
        recipe_id: The internal factorio name of a recipe e.g.
        'heavy-oil-cracking'.

    Returns:
        The English name of the item (e.g. 'Heavy oil cracking to light oil',
        'iron-gear-wheel'). If no user-friendly name is available then the input
        name is returned.
    """
    return _RECIPE_NAMES.get(recipe_id) or get_best_item_name(recipe_id)
