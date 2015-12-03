"""Generates URLs for factorio icons."""

import os.path

_NAME_TO_ICON = {}

def init(icon_directory_path):
    """Initializes the factorio icon manager.

    Args:
        icon_directory_path: The path of the factorio-data icon directory. Must
                be relative to the directory containing app.yaml.
    """
    for root, _, file_names in os.walk(icon_directory_path):
        for file_name in file_names:
            item_name = os.path.splitext(file_name)[0]
            _NAME_TO_ICON[item_name] = (
                '/' + os.path.relpath(os.path.join(root, file_name)))

def get_icon_for_item(name):
    """Return the url of the best icon for the given icon or recipe name.

    Args:
        name: The name of a factorio item (e.g. 'iron-gear-wheel' or recipe
            (e.g. 'basic-oil-processing').

    Returns:
        A URL refering to the icon of the requested item (e.g.
        '/factorio-data/icons/assembling-machine-3.png') or a default icon if
        no icon could be found.
    """
    if name in _NAME_TO_ICON:
        return _NAME_TO_ICON[name]
    else:
        return '/img/missing-item.png'
