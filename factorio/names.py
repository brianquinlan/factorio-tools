import json

_NAMES = None


def names_from_json(json_stream):
    global _NAMES
    _NAMES = json.load(json_stream)
    assert 'recipe-names' in _NAMES
    assert 'item-names' in _NAMES


def get_best_item_name(item_id):
    return _NAMES['item-names'].get(item_id) or item_id

def get_best_recipe_name(recipe_id):
    print 'Looking up: %r' % recipe_id
    try:
        return (
            _NAMES['recipe-names'].get(recipe_id) or
            _NAMES['item-names'].get(recipe_id) or
            recipe_id)
    except:
        return 'Hello'