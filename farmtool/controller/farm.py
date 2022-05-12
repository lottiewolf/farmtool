# This Python file uses the following encoding: utf-8

from farmtool.model.farm_db import FarmDB


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
        self.supplies = self.db.get_supplies()
        return self.supplies

    def get_animals(self, gp_id=-1):
        self.animals = self.db.get_animals(gp_id)
        return self.animals

    def get_expenses(self):
        self.expenses = self.db.get_expenses()
        return self.expenses

    def get_schedules(self, a_id=-1):
        self.schedules = self.db.get_schedules(a_id)
        return self.schedules

    def add_group(self, name):
        self.groups = self.db.add_group(name)
        return self.groups

    def add_supply(self, name, price, purchase_qty, units, notes, p_date, file):
        self.supplies = self.db.add_supply(name, price, purchase_qty, units, notes, p_date, file)
        return self.supplies

    def add_animal(self, name, group, date_add, date_rm):
        self.animals = self.db.add_animal(name, group, date_add, date_rm)
        return self.animals

    def add_expense(self, name, cost, group, animal, date):
        self.expenses = self.db.add_expense(name, cost, group, animal, date)
        return self.expenses

    def add_schedule(self, name, animal, supply, qty, fq, s_date, e_date):
        self.schedules = self.db.add_schedule(name, animal, supply, qty, fq, s_date, e_date)
        return self.schedules

    def flush(self, obj):
        return self.db.flush(obj)
