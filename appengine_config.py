"""Initialization script for App Engine scripts.

See https://cloud.google.com/appengine/docs/python/tools/appengineconfig?csw=1#Python_Module_Configuration
"""

from factorio import names
from factorio import recipe

recipe.Recipe.recipes_from_json(open("factorio-data/recipes.json", 'r'))
names.names_from_json(open("factorio-data/names.json", 'r'))
