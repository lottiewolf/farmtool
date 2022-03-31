#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:23:05 2022

@author: cwolf
"""

from sqlalchemy import (create_engine, select)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import (Sequence, Column, Integer, ForeignKey, String, DateTime, Date, Float)
from config.config_farm import ConfigFarm
import pandas as pd

Base = declarative_base()


class FarmDB():
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print("Connecting to database...")
            cls._instance = cls.__new__(cls)
            cls._instance.new_instance()
        return cls._instance

    def new_instance(self):
        try:
            settings = ConfigFarm.instance()
            self.engine = create_engine('sqlite:///'+str(settings.get_db_path()), echo=True)
            self.Session = sessionmaker(bind=self.engine, future=True, expire_on_commit=False)   # This session maker should go in an __init__ file, next version

            Base.metadata.create_all(self.engine)
        except:
            raise Exception("Could not create db")

    def get_groups(self):
        statement = select(Group)
        with self.Session.begin() as session:
            self.results = session.execute(statement).scalars().all()

        return self.results

    def get_supplies(self):
        statement = select(Supply)
        with self.Session.begin() as session:
            self.results = session.execute(statement).scalars().all()

        return self.results

    def get_animals(self):
        statement = select(Animal)
        with self.Session.begin() as session:
            self.results = session.execute(statement).scalars().all()

        return self.results

    def get_expenses(self):
        statement = select(Expense)
        with self.Session.begin() as session:
            self.results = session.execute(statement).scalars().all()

        return self.results

    def get_schedules(self):
        statement = select(Schedule)
        with self.Session.begin() as session:
            self.results = session.execute(statement).scalars().all()

        return self.results

    def add_group(self, new_name):
        gp = Group(name=new_name)
        with self.Session.begin() as session:
            session.add(gp)
        return self.get_groups()

    def add_supply(self, new_name, p_qty, new_units, new_price, new_notes, s_qty):
        sup = Supply(name=new_name, purchase_qty=p_qty, units=new_units, price=new_price, notes=new_notes, serving_qty=s_qty)
        with self.Session.begin() as session:
            session.add(sup)
        return self.get_supplies()

    def add_animal(self, new_name, new_group, d_add, d_rem):
        an = Animal(name=new_name, group=new_group, date_add=d_add, date_rm=d_rem)
        with self.Session.begin() as session:
            session.add(an)
        return self.get_animals()

    def add_expense(self, new_name, new_cost, new_group, new_animal, new_supply):
        exs = Supply(name=new_name, cost=new_cost, group=new_group, animal=new_animal, supply=new_supply)
        with self.Session.begin() as session:
            session.add(exs)
        return self.get_expenses()

    def add_schedule(self, new_name, new_animal, new_supply, new_qty, new_day_time):
        sch = Schedule(name=new_name, animal=new_animal, supply=new_supply, qty=new_qty, day_time=new_day_time)
        with self.Session.begin() as session:
            session.add(sch)
        return self.get_schedules()

#   ORM Querying

#import func SQLAlchemy
# gives us count, max, etc...
#derived tables (temp tables)....

#from sqlalchemy.orm import subqueryload

#for user in session.query(User).options(subqueryload(User.addresses)):
    #print(user, user.addresses)
    #eager loading of addresses, so it doesn't do n+1 sql queries
#           Column('timestamp', DateTime),
#           Column('amount', Numeric(10, 2)),
#           Column('type', Enum('a', 'b', 'c')) #this creates a data constraint
#           Column('email_address', String(100), nullable=False),
#           Column('user_id', Integer, ForeignKey('user.id')),


class Group(Base):
    __tablename__ = 'farm_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    animals = relationship("Animal", back_populates="group")
    expenses = relationship("Expense", back_populates="group")

    def __repr__(self):
        return f"Group(id={self.id!r}, name={self.name!r})"

    @classmethod
    def header(cls):
        return ["name"]

    def __getitem__(self, idx):
        return getattr(self, self.header()[idx])


class Animal(Base):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('farm_groups.id'), nullable=False)
    date_add = Column(Date, nullable=False)
    date_rm = Column(Date, nullable=True)

    group = relationship("Group", back_populates="animals")
    expenses = relationship("Expense", back_populates="animal")
    schedules = relationship("Schedule", back_populates="animal")

    def __repr__(self):
        return f"Animal(id={self.id!r}, name={self.name!r}, date_add={self.date_add!r}, date_rm={self.date_rm!r})"

    @classmethod
    def header(cls):
        return ["name", "group_id", "date_add", "date_rm"]

    def __getitem__(self, idx):
        return getattr(self, self.header()[idx])


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    group_id = Column(Integer, ForeignKey('farm_groups.id'), nullable=False)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    date = Column(Date, nullable=False)

    #the two of these fk together can not be null, needs verifying
    group = relationship("Group", back_populates="expenses")
    animal = relationship("Animal", back_populates="expenses")

    def __repr__(self):
        return f"Expense(id={self.id!r}, name={self.name!r}, amount={self.amount!r}, date={self.date!r})"

    @classmethod
    def header(cls):
        return ["name", "amount", "group_id", "animal_id", "date"]

    def __getitem__(self, idx):
        return getattr(self, self.header()[idx])


class Supply(Base):
    __tablename__ = 'supply'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    purchase_qty = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    serving_qty = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    date_purchase = Column(Date, nullable=True)

    schedules = relationship("Schedule", back_populates="supply")

    def __repr__(self):
        return f"Supply(id={self.id!r}, name={self.name!r}, purchase_qty={self.purchase_qty!r}, units={self.units!r}, price={self.price!r}, serving_qty={self.serving_qty!r}, notes={self.notes!r}, date_purchase={self.date_purchase!r})"

    @classmethod
    def header(cls):
        return ["name", "purchase_qty", "units", "price", "serving_qty", "notes", "date_purchase"]

    def __getitem__(self, idx):
        return getattr(self, self.header()[idx])


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    supply_id = Column(Integer, ForeignKey('supply.id'), nullable=False)
    qty = Column(Float, nullable=False)
    day_time = Column(Date, nullable=False)

    animal = relationship("Animal", back_populates="schedules")
    supply = relationship("Supply", back_populates="schedules")

    def __repr__(self):
        return f"Schedule(id={self.id!r}, name={self.name!r}, purchase_qty={self.purchase_qty!r}, units={self.units!r}, price={self.price!r}, serving_qty={self.serving_qty!r}, notes={self.notes!r}, date_purchase={self.date_purchase!r})"

    @classmethod
    def header(cls):
        return ["name", "animal_id", "supply_id", "qty", "day_time"]

    def __getitem__(self, idx):
        return getattr(self, self.header()[idx])
