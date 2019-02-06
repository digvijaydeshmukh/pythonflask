from flask import Flask
from flask_cors import CORS
import pyodbc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pymssql
import urllib

app = Flask(__name__)
CORS(app)
# it is for local database
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C://Users//d.manedeshmukh//PycharmProjects//practise1/database.db'

conn = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=SG-DB-07\SQL2014;DATABASE=Test;UID=sa;PWD=password.1')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# employee = Employee(name='new person')
# session.add(employee)
# session.commit()
# getcon = conn.cursor ()
# getcon.execute("select @@version")
#
# row=getcon.fetchone()
# while row:
#     print (row[0])
#     row=getcon.fetchone()
# print(sqlalchemy.__version__)
#
# print ("Connected to Database!",getcon)
# metadata = MetaData()
# Employee = Table('Employee', metadata,
#   Column('empId', Integer, primary_key=True),
#   Column('empname', String)
# )
# rs = app.conn.execute('SELECT * FROM Employee')
#
# for row in rs:
#     print(row)
