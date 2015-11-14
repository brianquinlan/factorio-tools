
"""
crafting speeds:
../entity/entities.lua
"""

class Producer(object):
    crafting_category_to_producers = {}

    def __init__(self, name, crafting_categories, crafting_speed):
        self.name = name
        self.crafting_categories = crafting_categories
        self.crafting_speed = crafting_speed

    @classmethod
    def get_most_efficient_producer(cls, category):
        return max(cls.crafting_category_to_producers[category],
                   key=lambda p: p.crafting_speed)

    @classmethod
    def _add_producer(cls, producer):
        for crafting_category in producer.crafting_categories:
            cls.crafting_category_to_producers.setdefault(
                crafting_category, set()).add(producer)

    @classmethod
    def init(cls):
        cls._add_producer(Producer('electric-furnace', {'smelting'}, 2))
        cls._add_producer(
            Producer(
                'assembling-machine-3',
                {"crafting", "advanced-crafting", "crafting-with-fluid"}, 1.25))
        cls._add_producer(
            Producer(
                'chemical-plant',
                {"chemistry"}, 1.25))


Producer.init()