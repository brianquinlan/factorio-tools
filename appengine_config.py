"""Initialization script for App Engine scripts.

See https://cloud.google.com/appengine/docs/python/tools/appengineconfig?csw=1#Python_Module_Configuration
"""

from appengine import icons

from factorio import names
from factorio import recipe

icons.init('factorio-data/icons')
names.names_from_json(open('factorio-data/names.json', 'r'))
recipe.Recipe.recipes_from_json(open('factorio-data/recipes.json', 'r'))
