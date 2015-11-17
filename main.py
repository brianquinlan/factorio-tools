import os.path
import sys

import jinja2
import webapp2

from factorio import recipe

import product

recipe.Recipe.recipes_from_json(open("factorio-data/recipes.json", 'r'))

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    undefined=jinja2.StrictUndefined,
    autoescape=True)



class MainPage(webapp2.RequestHandler):

    def get(self):
        required_production = recipe.calculate_required_production_rates(
            [('science-pack-3', 2)]) # [('power-armor-mk2', 1), ('rocket-silo', 1), ('assembling-machine-3', 1)])
        products = product.required_production_rates_to_products(
            required_production)
        template_values = {
            'products': products
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
