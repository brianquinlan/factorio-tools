import os.path
import sys

import jinja2
import webapp2

from factorio import recipe
from factorio import names

from appengine import produced_item


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    undefined=jinja2.StrictUndefined,
    autoescape=True)

def get_selected_items(requirements):
    class SelectedItem(object):
        def __init__(self, name, rate):
            self.name = name
            self.username = names.get_best_item_name(name)
            self.rate = rate

    return sorted(
        [SelectedItem(name, rate) for (name, rate) in requirements],
        key=lambda selected_item: selected_item.username)

def get_produceable_items():
    class Item(object):
        def __init__(self, name):
            self.name = name
            self.username = names.get_best_item_name(name)

    return sorted(
        [Item(result) for result in recipe.Recipe.get_results()],
        key=lambda item: item.username)


class MainPage(webapp2.RequestHandler):

    def get(self):
        requirements = []
        for item in self.request.arguments():
            requirements.append(
                (item, self.request.get_range(item, min_value=1, default=1)))

        required_production = recipe.calculate_required_production_rates(
            requirements)
        products = produced_item.required_production_rates_to_produced_items(
            required_production)
        template_values = {
            'items_to_produce': get_produceable_items(),
            'products': products,
            'selected_items': get_selected_items(requirements),
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
