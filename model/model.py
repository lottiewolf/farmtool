# This Python file uses the following encoding: utf-8

class Animal:
    def __init__(self, name, group, added, removed):
        self.name = name
        self.group = group
        self.date_added = added
        self.date_removed = removed

class Group:
    def __init__(self, name):
        self.name = name

class Expense:
    def __init__(self, name, animal, group, amount):
        self.name = name
        self.animal = animal
        self.group = group
        self.amount = amount

class Supply:
    def __init__(self, name, purchase_qty, units, price, notes, serving_qty):
        self.name = name
        self.purchase_qty = purchase_qty
        self.units = units
        self.price = price
        self.notes = notes
        self.serving_qty = serving_qty

    def price_per_unit(self):
        return (self.price/self.qty)

    def price_per_serving(self):
        return (self.price_per_unit*self.serving_qty)

class Schedule:
    def __init__(self, animal, supply, day_time):
        self.animal = animal
        self.supply = supply
        self.day_time = day_time
