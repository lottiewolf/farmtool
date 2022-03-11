# This Python file uses the following encoding: utf-8

import os, os.path
import pandas as pd

class Farm:
    def __init__(self, name, groups, supplies):
        self.name = name
        self.groups = groups
        self.supplies = supplies

    def get_name(self):
        return self.name

    def get_groups(self):
        return self.groups

    def get_supplies(self):
        return self.supplies


class Animal:
    def __init__(self, name, group, added, removed):
        self.name = name
        self.group = group
        self.date_added = added
        self.date_removed = removed

    def get_all_expenses(self):
        # returns all expenses with this animal FK
        pass

    def get_schedules(self):
        #returns all schedules with this animal FK
        pass


class Group:
    def __init__(self, name):
        self.name = name

    def get_animals(self):
        #return all animals with this group FK, could be empty
        pass

    def get_expenses(self):
        # returns all expenses with this group FK
        pass


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
    def __init__(self, name, animal, supply, day_time, qty):
        self.name = name
        self.animal = animal
        self.supply = supply
        self.day_time = day_time
        self.qty = qty
