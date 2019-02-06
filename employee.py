from flask_sqlalchemy import SQLAlchemy
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)


# db=SQLAlchemy(app.conn)
class Employee(db.Model):
    __tablename__ = "Employee"
    EmpID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmpName = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'EmpID': self.EmpID, 'EmpName': self.EmpName}

    def get_all_emp(self):
        return [Employee.json(emp) for emp in Employee.query.all()]

    def get_limit_emp(self):
        return [Employee.json(emp) for emp in Employee.query.limit(10).all()]

    def get_single(_EmpID):
        return Employee.query.get(_EmpID)

    def add_new_emp(_EmpName):
        new_emp = Employee(EmpName=_EmpName)
        print("new_emp", new_emp)
        db.session.add(new_emp)
        db.session.commit()
        return "success"

    def delete_emp_by_Id(_EmpID):
        return Employee.query.filter_by(EmpID=_EmpID).delete()
        db.session.commit()

    def __repr__(self):
        book_object = {
            'EmpID': self.EmpID,
            'EmpName': self.EmpName,
        }
        return json.dumps(book_object)
