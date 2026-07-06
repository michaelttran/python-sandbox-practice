"""
Design a system for building a custom meal order at a fast-casual restaurant (think Chipotle-style). 
An order is built up from a series of optional and required steps — 
    protein, base, toppings (multiple), sauce, and size — 
    and some combinations require validation (e.g., a "kids meal" size can't have more than 2 toppings). 
    
Provide a clean way to construct one of these orders step-by-step, and make sure an invalid or incomplete 
order can't be produced.
"""
"""
    Questions:
        - Do we need to worry about pricing? -> let's skip this for this POC, it can be added to extensibility
        - Do we need to consider attaching a user to each order? -> let's keep this for extensibility
        - Do we include drinks? -> yes, let's allow cup sizes(s, m, l) and bottle(Mexican Coca Cola)
        - Should we allow half-portions of anything? -> let's finish the POC and then see how we can add, aim to get this done though
        - Tests? Let's add one unit test on if it's a kids meal, they can't have more than two toppings

    Requirements:
        - Primary capabilities
            - Build a complete order and validate that the combinations are valid

        - Rules & Completion
            - implement a builder design 

    Entities & Responsibilities:

        Order():
            - base
                - tacos(2)
                - tortilla
                - rice
        
            - protein
                - chicken
                - steak
                - pork
                - beans

            - toppings
                - onions
                - cilantro
                - lettuce
                - corn
                - sour_cream
                - guacamole
                - cheese

            - sauce
                - mild
                - medium
                - spicy

            - size
                - kids
                - small
                - medium
                - large
            
            - drink
                - kids
                - water_cup
                - small
                - medium
                - large
                - bottle


            Builder()
                - build -> _order

        Order():
            - Organizational class 

            Builder() -> makes construction readable and handles fields cleanly + implements logic validation
            on specific fields
                - def build() -> validates before returning
        
    Class Design:
        class Order:
            def __init__(self):
                self.base = Optional[str] | None
                self.protein = Optional[str] | None
                self.toppings = Optional[str] | None
                self.sauce = Optional[str] | None
                self.size = Optional[str] | None
                self.drink = Optional[str] | None

            Class Builder:
                def __init__(self):
                    self._order = Order()

                def base(self, base:str) -> "Order.Builder"

                def protein(self, protein:str) -> "Order.Builder"

                def toppings(self, toppings:str) -> "Order.Builder"

                def sauce(self, sauce:str) -> "Order.Builder"

                def size(self, size:str) -> "Order.Builder"

                def drink(self, drink:str) -> "Order.Builder"

                def build(self) -> "Order"

    Tests:
        - Add one test to validate kids meal <= 2 toppings

    Extensibility:
        - pricing
        - user ownership per order
        - half-portions
"""
from enum import Enum
from typing import Optional


class Base(Enum):
    TACOS = "tacos"
    TORTILLA = "tortilla"
    RICE = "rice"

base_lookup = {b.value: b for b in Base}

class Protein(Enum):
    CHICKEN = "chicken"
    STEAK = "steak"
    PORK = "pork"
    BEANS = "beans"

protein_lookup = {p.value: p for p in Protein}

class Toppings(Enum):
    ONIONS = "onions"
    CILANTRO = "cilantro"
    LETTUCE = "lettuce"
    CORN = "corn"
    SOUR_CREAM = "sour cream"
    GUACAMOLE = "guacamole"
    CHEESE = "cheese"

toppings_lookup = {t.value: t for t in Toppings}

class Sauce(Enum):
    MILD = "mild"
    MEDIUM = "medium"
    HOT = "hot"

sauce_lookup = {s.value: s for s in Sauce}

class Size(Enum):
    KIDS = "kids"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

size_lookup = {si.value: si for si in Size}

class Drink(Enum):
    KIDS = "kids"
    WATER_CUP = "water cup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    BOTTLE = "bottle"

drink_lookup = {d.value: d for d in Drink}


class Order:
    def __init__(self):
        self.base: Optional[str] = None
        self.protein: Optional[str] = None
        self.toppings: list = []
        self.sauce: Optional[str] = None
        self.size: Optional[str] = None
        self.drink: Optional[str] = None

    class Builder:
        def __init__(self):
            self._order = Order()

        def base(self, base: str) -> "Order.Builder":
            if base not in base_lookup:
                raise ValueError(f"{base} not allowed in base options: {[b.value for b in Base]}")

            self._order.base = base
            return self

        def protein(self, protein: str) -> "Order.Builder":
            if protein not in protein_lookup:
                raise ValueError(f"{protein} not allowed in protein options: {[p.value for p in Protein]}")

            self._order.protein = protein
            return self

        def toppings(self, toppings: list) -> "Order.Builder":
            invalid = [t for t in toppings if t not in toppings_lookup]
            if invalid:
                raise ValueError(f"{invalid} not allowed in toppings options: {[t.value for t in Toppings]}")

            self._order.toppings = toppings
            return self

        def sauce(self, sauce: str) -> "Order.Builder":
            if sauce not in sauce_lookup:
                raise ValueError(f"{sauce} not allowed in sauce options: {[s.value for s in Sauce]}")

            self._order.sauce = sauce
            return self

        def size(self, size: str) -> "Order.Builder":
            if size not in size_lookup:
                raise ValueError(f"{size} not allowed in size options: {[s.value for s in Size]}")

            self._order.size = size
            return self

        def drink(self, drink: str) -> "Order.Builder":
            if drink not in drink_lookup:
                raise ValueError(f"{drink} not allowed in drink options: {[d.value for d in Drink]}")

            self._order.drink = drink
            return self

        def build(self) -> "Order":
            missing = [f for f in ("base", "protein", "size") if getattr(self._order, f) is None]
            if missing:
                raise ValueError(f"Missing required fields: {missing}")

            t_len = len(self._order.toppings)
            if self._order.size == Size.KIDS.value and t_len > 2:
                raise ValueError(
                    f"kids meal can only have 2 toppings, has {t_len}: {self._order.toppings}"
                )

            return self._order

    def pprint(self):
        print(
            f"base: {self.base} \nprotein: {self.protein} \ntoppings: {self.toppings} "
            f"\nsauce: {self.sauce} \nsize: {self.size} \ndrink: {self.drink}"
        )


def main():
    print("Starting..\n")

    order = (Order.Builder()
             .base("rice")
             .protein("chicken")
             .toppings(["corn", "guacamole"])
             .sauce("mild")
             .size("kids")
             .drink("bottle")
             .build())

    order.pprint()

    print("Finished.")


if __name__ == "__main__":
    main()


import unittest

class TestOrder(unittest.TestCase):
    def test_kids_meal_topping_limit(self):
        with self.assertRaises(ValueError):
            (Order.Builder()
                .base("rice")
                .protein("chicken")
                .toppings(["onions", "cilantro", "lettuce"])
                .size("kids")
                .build())

    def test_kids_meal_two_toppings_ok(self):
        order = (Order.Builder()
                    .base("rice")
                    .protein("chicken")
                    .toppings(["onions", "cilantro"])
                    .size("kids")
                    .build())
        self.assertEqual(order.size, "kids")

    def test_kids_meal_topping_limit_regardless_of_call_order(self):
        # size() called before toppings() — this now correctly still raises,
        # since the check lives in build(), not size()
        with self.assertRaises(ValueError):
            (Order.Builder()
                .base("rice")
                .protein("chicken")
                .size("kids")
                .toppings(["onions", "cilantro", "lettuce"])
                .build())

    def test_missing_required_field_raises(self):
        with self.assertRaises(ValueError):
            Order.Builder().base("rice").build()  # missing protein, size


if __name__ == "__main__":
    unittest.main()