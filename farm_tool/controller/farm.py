# This Python file uses the following encoding: utf-8

from farm_tool.model.farm_db import FarmDB


class Farm:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Instantiating database...')
            cls._instance = cls.__new__(cls)
            cls._instance.connect()
        return cls._instance

    def connect(self):
        self.db = FarmDB.instance()

    def get_groups(self):
        self.groups = self.db.get_groups()
        return self.groups

    def get_supplies(self):
        # This dropdown should be populated from a model, subclassed from QAbstractListModel.
        self.supplies = self.db.get_supplies()
        return self.supplies

    def get_animals(self):
        self.animals = self.db.get_animals()
        return self.animals

    def get_expenses(self):
        self.expenses = self.db.get_expenses()
        return self.expenses

    def get_schedules(self):
        self.schedules = self.db.get_schedules()
        return self.schedules

    def get_group_list(self):
        self.groups = self.get_groups()
        self.g_list = []
        for g in self.groups:
            self.g_list.append(g.name)
        return self.g_list

    def get_animal_list(self):
        self.anims = self.get_animals()
        self.a_list = []
        for a in self.anims:
            self.a_list.append(a.name)
        return self.a_list

    def get_supply_list(self):
        self.sups = self.get_supplies()
        self.s_list = []
        for s in self.sups:
            self.s_list.append(s.name)
        return self.s_list

    def add_group(self, name):
        self.groups = self.db.add_group(name)
        return self.groups

    def add_supply(self, name, purchase_qty, units, price, notes, serving_qty):
        self.supplies = self.db.add_supply(name, purchase_qty, units, price, notes, serving_qty)
        return self.supplies

    def add_animal(self, name, group, date_add, date_rm):
        self.animals = self.db.add_animal(name, group, date_add, date_rm)
        return self.animals

    def add_expense(self, name, cost, group, animal, date):
        self.expenses = self.db.add_expense(name, cost, group, animal, date)
        return self.expenses

    def add_schedule(self, name, animal, supply, qty, day_time):
        self.schedules = self.db.add_schedule(name, animal, supply, qty, day_time)
        return self.schedules

