# A Python package and webapp for Factorio production planning

This repository contains a Python package that can be used to make Factorio-related scripts. For example:

```
>>> from factorio import recipe
>>> recipe.Recipe.recipes_from_json(open('factorio-data/recipes.json', 'r'))
>>> requirements = recipe.calculate_required_production_rates(([('electronic-circuit', 3)]))
>>> for item, _, consumers in requirements:  # Print the production requirements for 3 circuits
...     print item, sum(consumers.values())
... 
copper-cable 9.0
copper-ore 4.5
copper-plate 4.5
electronic-circuit 3
iron-ore 3.0
iron-plate 3.0
```

A running instance of the webapp can be found at http://factorio-production-planner.appspot.com/?destroyer-capsule=1

## Python page setup

Before using the Python package, you have to extract certain data from Factorio (e.g. names, production rates). You can that with:

```
/factorio-tools $ ./extract_factorio_data.py 
Extracting data
from: /Applications/factorio.app/Contents/data
to:   /factorio-tools/factorio-data
Done!
```

If you need any help using the package, just e-mail brian@sweetapp.com.

Good luck!
