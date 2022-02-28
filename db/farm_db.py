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
from sqlalchemy import (Sequence, Column, Integer, ForeignKey, String, DateTime, Date)


Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    horses_id = Column(Integer, ForeignKey('horses.id'))
    #horse = relationship("Horse", back_populates="expenses")

def __repr__(self):
         return "<Address(email_address='%s')>" % self.email_address


class Horse(Base):
    __tablename__ = 'horses'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))
    #d = DATE(
    #   storage_format="%(month)02d/%(day)02d/%(year)04d",
    #   regexp=re.compile("(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)")
    #)
    #Column("date", Date),
    #sa.Column('date', sa.Date(), nullable=True)
    #Horse.addresses = relationship("Address", order_by=Address.id, back_populates="user")
    #date_born = Column(Date, nullable=False)
    #date_arrived = Column(Date, nullable=False)
    #date_depart = Column(Date, nullable=True)
    #date_death = Column(Date, nullable=True)

def __repr__(self):
    return "<Horse(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)
    
indy = Horse(name='Indy', fullname='Independence', nickname='indy')

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

session.add(indy)
session.add_all([
     Horse(name='wendy', fullname='Wendy Williams', nickname='windy'),
     Horse(name='mary', fullname='Mary Contrary', nickname='mary'),
     Horse(name='fred', fullname='Fred Flintstone', nickname='freddy')])

#"d": datetime.date(2010, 5, 1),
#table.insert(),
#            {
#                "dt": datetime.datetime(2010, 5, 1, 12, 11, 10),
#                "d": datetime.date(2010, 5, 1),
#            }


