#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:23:05 2022

@author: cwolf
"""

from sqlalchemy import (create_engine, select, inspect)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import (Sequence, Column, Integer, ForeignKey, String, DateTime, Date, Float)
from farmtool.config.config_farm import ConfigFarm
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
            #self.Session = Session(self.engine)

            Base.metadata.create_all(self.engine)
        except:
            raise Exception("Could not create db")
        print("This is my sessionmaker result type: ",type(self.Session))

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

    def get_animals(self, gp_id=-1):
        if(gp_id==-1):
            statement = select(Animal)
            with self.Session.begin() as session:
                self.results = session.execute(statement).scalars().all()
        else:
            statement = select(Animal).where(Animal.group_id == gp_id)
            with self.Session.begin() as session:
                self.results = session.execute(statement).scalars().all()
        return self.results

    def get_expenses(self, gp_id=-1, anim_id=-1):
        statement = select(Expense)
        with self.Session.begin() as session:
            self.results = session.execute(statement).scalars().all()
        return self.results

    def get_schedules(self, anim_id=-1):
        if(anim_id==-1):
            statement = select(Schedule)
            with self.Session.begin() as session:
                self.results = session.execute(statement).scalars().all()
        else:
            statement = select(Schedule).where(Schedule.animal_id == anim_id)
            with self.Session.begin() as session:
                self.results = session.execute(statement).scalars().all()
        return self.results

    def add_group(self, new_name):
        gp = Group(name=new_name)
        with self.Session.begin() as session:
            session.add(gp)
        return self.get_groups()

    def add_supply(self, name, price, p_qty, units, notes, d_purchase, invoice):
        sup = Supply(name=name, price=price, purchase_qty=p_qty, units=units, notes=notes, date_purchased=d_purchase, invoice=invoice)
        with self.Session.begin() as session:
            session.add(sup)
        return self.get_supplies()

    def add_animal(self, name, group, d_add, d_rem):
        an = Animal(name=name, group=group, date_added=d_add, date_removed=d_rem)
        with self.Session.begin() as session:
            session.add(an)
        return self.get_animals()

    def add_expense(self, name, cost, group, animal, date):
        exs = Expense(name=name, amount=cost, group=group, animal=animal, date=date)
        with self.Session.begin() as session:
            session.add(exs)
        return self.get_expenses()

    def add_schedule(self, name, animal, supply, qty, fq, s_date, e_date):
        sch = Schedule(name=name, animal=animal, supply=supply, qty=qty, frequency=fq, date_started=s_date, date_ended=e_date)
        with self.Session.begin() as session:
            session.add(sch)
        return self.get_schedules()

    def flush(self, obj):
        #session = inspect(obj).session
        insp = inspect(obj)
        print("state of db obj?: "+str(insp.detached))
        #session.commit()


#   ORM Querying
#from sqlalchemy.orm import subqueryload
#for user in session.query(User).options(subqueryload(User.addresses)):
    #print(user, user.addresses)
    #eager loading of addresses, so it doesn't do n+1 sql queries

class Farm:
    def __getitem__(self, idx):
        return getattr(self, self.header()[idx])

    def __setitem__(self, idx, value):
        setattr(self, self.header()[idx], value)


class Group(Base, Farm):
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


class Animal(Base, Farm):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('farm_groups.id'), nullable=False)
    date_added = Column(Date, nullable=False)
    date_removed = Column(Date, nullable=True)

    group = relationship("Group", back_populates="animals")
    expenses = relationship("Expense", back_populates="animal")
    schedules = relationship("Schedule", back_populates="animal")

    def __repr__(self):
        return f"Animal(id={self.id!r}, name={self.name!r}, date_add={self.date_added!r}, date_rm={self.date_removed!r})"

    @classmethod
    def header(cls):
        return ["name", "date_added"]


class Expense(Base, Farm):
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


class Supply(Base, Farm):
    __tablename__ = 'supply'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    purchase_qty = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    date_purchased = Column(Date, nullable=False)
    invoice = Column(String)

    schedules = relationship("Schedule", back_populates="supply")

    def __repr__(self):
        return f"Supply(id={self.id!r}, name={self.name!r}, qty={self.purchase_qty!r}, units={self.units!r}, price={self.price!r}, inv={self.invoice!r}, date={self.date_purchased!r})"

    @classmethod
    def header(cls):
        return ["name", "price", "purchase_qty", "units", "notes", "date_purchased", "invoice"]


class Schedule(Base, Farm):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    animal_id = Column(Integer, ForeignKey('animal.id'), nullable=False)
    supply_id = Column(Integer, ForeignKey('supply.id'), nullable=False)
    qty = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    date_started = Column(Date, nullable=False)
    date_ended = Column(Date, nullable=True)

    animal = relationship("Animal", back_populates="schedules")
    supply = relationship("Supply", back_populates="schedules")

    def __repr__(self):
        return f"Schedule(id={self.id!r}, name={self.name!r}, qty={self.qty!r}, qty={self.qty!r}, date={self.date_started!r})"

    @classmethod
    def header(cls):
        return ["name", "animal_id", "supply_id", "qty", "frequency"]
