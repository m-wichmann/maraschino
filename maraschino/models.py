# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean
from maraschino.database import Base

class Module(Base):
    """Table for one Maraschino module"""
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    column = Column(Integer)
    position = Column(Integer)
    poll = Column(Integer)
    delay = Column(Integer)

    def __init__(self, name, column, position=None, poll=None, delay=None):
        self.name = name
        self.column = column
        self.position = position
        self.poll = poll
        self.delay = delay

    def __repr__(self):
        return '<Module %r>' % (self.name)


class Setting(Base):
    """Table for one setting value"""
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True)
    value = Column(String(500))

    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<Setting %r>' % (self.key)


class Application(Base):
    """Table for one application in the applications module"""
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    url = Column(String(1000))
    description = Column(String(100))
    image = Column(String(100))
    position = Column(Integer)

    def __init__(self, name, url, description=None, image=None, position=None):
        self.name = name
        self.url = url
        self.description = description
        self.image = image

        if position == None:
            self.position = highest_position(Application)
        else:
            self.position = position

    def __repr__(self):
        return '<Application %r>' % (self.name)


class Disk(Base):
    """Table for one disk in the diskspace module"""
    __tablename__ = 'disks'
    id = Column(Integer, primary_key=True)
    path = Column(String(500))
    position = Column(Integer)

    def __init__(self, path, position=None):
        self.path = path

        if position == None:
            self.position = highest_position(Disk)
        else:
            self.position = position

    def __repr__(self):
        return '<Disk %r>' % (self.path)


class XbmcServer(Base):
    """Table for the XBMC server config"""
    __tablename__ = 'xbmc_servers'
    id = Column(Integer, primary_key=True)
    label = Column(String(500))
    position = Column(Integer)
    hostname = Column(String(500))
    port = Column(String(10))
    username = Column(String(100))
    password = Column(String(100))
    mac_address = Column(String(100))

    def __init__(self, label, position, hostname, port='8080', username=None, password=None, mac_address=None):
        self.label = label

        if position == None:
            self.position = highest_position(Disk)
        else:
            self.position = position

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.mac_address = mac_address

    def __repr__(self):
        return '<XbmcServer %r>' % (self.label)


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1
