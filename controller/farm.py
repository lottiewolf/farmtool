# This Python file uses the following encoding: utf-8

from model.farm_db import FarmDB
import os, os.path
import pandas as pd

class Farm:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, name=None, groups=None, supplies=None, animals=None, expenses=None, schedules=None):
        if cls._instance is None:
            raise RuntimeError('No farm created')
        return cls._instance

    @classmethod
    def create_farm(cls, name, groups, supplies, animals, expenses, schedules):
        if cls._instance is not None:
            raise RuntimeError('Farm already exists')

        print('Creating new Farm instance')
        cls._instance = cls.__new__(cls)
        cls._instance.name = name
        cls._instance.groups = groups
        cls._instance.supplies = supplies
        cls._instance.animals = animals
        cls._instance.expenses = expenses
        cls._instance.schedules = schedules
        return cls._instance

    def get_name(self):
        return self.name

    def get_groups(self):
        return self.groups

    def get_supplies(self):
        return self.supplies

    def get_animals(self):
        return self.animals

    def get_expenses(self):
        return self.expenses

    def get_schedules(self):
        return self.schedules

    def add_group(self, name):
        FarmDB.instance().add_group(name)
        self.groups = FarmDB.instance().refresh("groups")
        return self.groups

    def add_supply(self, name, purchase_qty, units, price, notes, serving_qty):
        FarmDB.instance().add_supply(name, purchase_qty, units, price, notes, serving_qty)
        self.supplies = FarmDB.instance().refresh("supplies")
        return self.supplies

    def add_animal(self, name, group, date_add, date_rem):
        FarmDB.instance().add_animal(name, group, date_add, date_rem)
        self.animals = FarmDB.instance().refresh("animals")
        return self.animals

    def add_expense(self, name, cost, group, animal, supply):
        FarmDB.instance().add_expense(name, cost, group, animal, supply)
        self.expenses = FarmDB.instance().refresh("expenses")
        return self.expenses

    def add_schedule(self, name, animal, supply, qty, day_time):
        FarmDB.instance().add_schedule(name, animal, supply, qty, day_time)
        self.schedules = FarmDB.instance().refresh("schedules")
        return self.schedules


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
