"""Data and computations related to production machines."""

class Producer(object):
    """A machine that can produce items."""
    crafting_category_to_producers = {}

    def __init__(self, name, crafting_categories, crafting_speed):
        """Initialize the producer.

        Args:
            name: The name of the producer e.g. 'electric-furnace'.
            crafting_categories: A sequence of crafting categories that the
                producer supports e.g. ['chemisty', 'smelting'].
            crafting_speed: The producers crafting rate e.g. 1.5.
        """
        self.name = name
        self.crafting_categories = frozenset(crafting_categories)
        self.crafting_speed = crafting_speed

    @classmethod
    def get_most_efficient_producer(cls, category):
        """Returns the most efficient Producer for a crafting category.

        Args:
            category: The crafting category e.g. 'chemisty' or 'smelting'.

        Returns:
            A producer that can produce that crafting category.

        Raises:
            KeyError: if no Producer can produce the given crafting category.
        """
        return max(cls.crafting_category_to_producers[category],
                   key=lambda p: p.crafting_speed)

    @classmethod
    def _add_producer(cls, producer):
        for crafting_category in producer.crafting_categories:
            cls.crafting_category_to_producers.setdefault(
                crafting_category, set()).add(producer)

    @classmethod
    def init(cls):
        """Load the producer information.

        A subset of the data taken from:
            - base/prototypes/entities/entities.lua
            - base/prototypes/entities/demo-entities.lua
        """
        cls._add_producer(Producer('electric-furnace', {'smelting'}, 2))
        cls._add_producer(Producer('assembling-machine-1', {'crafting'}, 0.5))
        cls._add_producer(
            Producer(
                'assembling-machine-2',
                {'crafting', 'advanced-crafting', 'crafting-with-fluid'}, 0.75))
        cls._add_producer(
            Producer(
                'assembling-machine-3',
                {'crafting', 'advanced-crafting', 'crafting-with-fluid'}, 1.25))
        cls._add_producer(Producer('chemical-plant', {'chemistry'}, 1.25))
        cls._add_producer(Producer('oil-refinery', {'oil-processing'}, 1))


Producer.init()
