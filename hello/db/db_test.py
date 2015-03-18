# -*- coding: utf-8 -*-
import hashlib
import urllib
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
 
class User(Base):
    __tablename__ = 'users'
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
 
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = hashlib.sha1(password).hexdigest()
 
    def __repr__(self):
        return "User('%s','%s', '%s')" % \
        (self.name, self.username, self.password)
 
if __name__ == '__main__':
    #params = urllib.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=IRVING-VAIO\SQLEXPRESS;DATABASE=testdb;UID=sa;PWD=irving")
    #engine = create_engine("mssql:///?odbc_connect=%s" % params)
    #engine = create_engine('sqlite:///:memory:', echo=True)
    #engine = create_engine("mssql://sa:irving@IRVING-VAIO/testdb")
    #engine = create_engine('mssql+pymssql://sa:irving@vaio', echo=True)
    engine = create_engine('mssql+pymssql://sa:irving@irving-VAIO:1433/testdb', echo=True)
    #engine = create_engine('mssql+pyodbc://sa:irving@vaio')
    
    Base.metadata.create_all(engine)
 
    Session = sessionmaker(bind=engine)
    session = Session()
 
 
    user_1 = User("user1", "username1", "password_1")
    session.add(user_1)
    row = session.query(User).filter_by(name='user1').first()
    if row:
        print 'Found user1'
        print row
    else:
        print 'Can not find user1'
 
    session.rollback() # 資料庫回到新增 user1 之前的狀態
 
    row = session.query(User).filter_by(name='user1').first()
    if row:
        print 'Found user1 after rollback'
        print row
    else:
        print 'Can not find user1 after rollback'
 
    user_2 = User("user2", "username2", "password_2")
    session.add(user_2)
    session.commit()