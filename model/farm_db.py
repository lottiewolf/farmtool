#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 11:23:05 2022

@author: cwolf
"""
import sqlalchemy
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import (Sequence, Column, Integer, ForeignKey, String, DateTime, Date, Float)
import os, os.path
import pandas as pd

Base = declarative_base()


class FarmDB():
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print("Creating new DB instance")
            cls._instance = cls.__new__(cls)
            cls._instance.new_instance()
        return cls._instance

    def new_instance(self):
        try:
            self.engine = create_engine('sqlite:///db/farmtool.db', echo=True)
            Session = sessionmaker(bind=self.engine)

            Base.metadata.create_all(self.engine)

            with Session() as session:
                session.commit()
                session.close()
            #result = engine.execute("select * from table")

            #load all data from the database into df??? (but probably not) and
            # then delete the lines below

            self.folder_path = os.path.join(os.getcwd(), "data")
            self.group_file = os.path.join(self.folder_path, "__groups.csv")
            self.supply_file = os.path.join(self.folder_path, "__supplies.csv")
            self.animal_file = os.path.join(self.folder_path, "__animals.csv")
            self.expense_file = os.path.join(self.folder_path, "__expenses.csv")
            self.schedule_file = os.path.join(self.folder_path, "__schedules.csv")
            self.gp_df=pd.read_csv(self.group_file)
            self.su_df=pd.read_csv(self.supply_file)
            self.an_df=pd.read_csv(self.animal_file)
            self.ex_df=pd.read_csv(self.expense_file )
            self.sc_df=pd.read_csv(self.schedule_file )
        except:
            raise Exception("File error: Could not read db")

    def add_group(self, name):
        self.row = pd.Series([0, name], index=self.gp_df.columns)
        self.gp_df = self.gp_df.append(self.row, ignore_index=True)
        try:
            self.gp_df.to_csv(self.group_file, index=False)
        except:
            raise Exception("File error: Could not write to DB")

    def add_supply(self, name, purchase_qty, units, price, notes, serving_qty):
        self.row = pd.Series([0, name, purchase_qty, units, price, notes, serving_qty], index=self.su_df.columns)
        self.su_df = self.su_df.append(self.row, ignore_index=True)
        try:
            self.su_df.to_csv(self.supply_file, index=False)
        except:
            raise Exception("File error: Could not write to DB")

    def add_animal(self, name, group, date_add, date_rem):
        self.row = pd.Series([0, name, group, date_add, date_rem], index=self.an_df.columns)
        self.an_df = self.an_df.append(self.row, ignore_index=True)
        try:
            self.an_df.to_csv(self.animal_file, index=False)
        except:
            raise Exception("File error: Could not write to DB")

    def add_expense(self, name, cost, group, animal, supply):
        self.row = pd.Series([0, name, cost, group, animal, supply], index=self.ex_df.columns)
        self.ex_df = self.ex_df.append(self.row, ignore_index=True)
        try:
            self.ex_df.to_csv(self.expense_file, index=False)
        except:
            raise Exception("File error: Could not write to DB")

    def add_schedule(self, name, animal, supply, qty, day_time):
        self.row = pd.Series([0, name, animal, supply, qty, day_time], index=self.sc_df.columns)
        self.sc_df = self.sc_df.append(self.row, ignore_index=True)
        try:
            self.sc_df.to_csv(self.schedule_file, index=False)
        except:
            raise Exception("File error: Could not write to DB")

    def refresh(self, flag):
        try:
            if flag == "groups":
                self.df=pd.read_csv(self.group_file)
            elif flag == "supplies":
                self.df=pd.read_csv(self.supply_file)
            elif flag == "animals":
                self.df=pd.read_csv(self.animal_file)
            elif flag == "expenses":
                self.df=pd.read_csv(self.expense_file)
            elif flag == "schedules":
                self.df=pd.read_csv(self.schedule_file)
            else:
                raise Exception("No flag found")
        except:
            raise Exception("File error: Could not read db")
        return self.df



#
    #d = DATE(
    #   storage_format="%(month)02d/%(day)02d/%(year)04d",
    #   regexp=re.compile("(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)")
    #)
#metadata.drop_all
#table.create(
#table.drop

#           Column('timestamp', DateTime),
#           Column('amount', Numeric(10, 2)),
#           Column('type', Enum('a', 'b', 'c')) #this creates a data constraint
#           Column('email_address', String(100), nullable=False),
#           Column('user_id', Integer, ForeignKey('user.id')),

#   ORM

#ed_user = User(....
#session.add(ed_user)
#our_user = session.query(User).filter_by(name='ed').first()
#this ^ is unit of work in a nutshell, ORM doing its thing
#session.rollback()
#session.flush()

#   ORM Querying

#print(User.name == "ed")
#query = session.query(User).filter(User.name == 'ed').order_by(User.id)
#query.all()

#for row in session.query(User, User.name):
#    print(row.User, row.name)
 #u = session.query(User).order_by(User.id)[2] #grabs the second element, array slices [1:3]

#q = session.query(User.fullname)
#q.all()
#q2 = q.filter(or_(User.name == 'mary', User.name == 'ed'))
#q2[1]


#session.commit()

#session.query(User, Address).join(User.addresses).all()
#session.query(User, Address).join(Address).all() # only if simple
#                           .filter(Address.email_address == 'jack@......first()

#a1, a2 = aliased(Address), aliased(Address)
# to create aliases inside the SQL

#import func SQLAlchemy
# gives us count, max, etc...
#derived tables (temp tables)....

#from sqlalchemy.orm import subqueryload

#for user in session.query(User).options(subqueryload(User.addresses)):
    #print(user, user.addresses)
    #eager loading of addresses, so it doesn't do n+1 sql queries
#options(contains eager)....
#delete cascade delete orphans


class Group(Base):
    __tablename__ = 'farm_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    animals = relationship("Animal", back_populates="group")
    expenses = relationship("Expense", back_populates="group")

    def __repr__(self):
        return f"Group(id={self.id!r}, name={self.name!r})"


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


class Supply(Base):
    __tablename__ = 'supply'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    purchase_qty = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    serving_qty = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
    date_purchase = Column(Date, nullable=False)

    schedules = relationship("Schedule", back_populates="supply")

    def __repr__(self):
        return f"Supply(id={self.id!r}, name={self.name!r}, purchase_qty={self.purchase_qty!r}, units={self.units!r}, price={self.price!r}, serving_qty={self.serving_qty!r}, notes={self.notes!r}, date_purchase={self.date_purchase!r})"


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
