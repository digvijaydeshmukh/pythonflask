from flask import Flask, jsonify, request, Response

import json
from settings import *
from employee import *
from usermodel import *
from functools import wraps
import jwt, datetime
import calendar
# app=Flask(__name__)

# print("test",__name__)
app.config['SECRET_KEY'] = "test"

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def token_requierd(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers['Authorization']
        print(token)

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({"eroor": "need valid token"}), 401

    return wrapper


@app.route('/login', methods=['POST'])
def get_token():
    loginInfo = request.get_json()
    print("log", loginInfo)
    username = str(loginInfo["UserName"])
    password = str(loginInfo["Password"])
    match = User.username_pass_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        response = Response("token", status=200, mimetype="application/json")
        return token
    else:
        return Response('', 401, mimetype='application/json')


books = [
    {
        'id': 1,
        'name': 'First Book',
        'author': 'First Author',
        'prise': '$100'
    },
    {
        'id': 2,
        'name': 'Second Book',
        'author': 'Second Author',
        'prise': '$200'
    },
    {
        'id': 3,
        'name': 'Third Book',
        'author': 'Third Author',
        'prise': '$300'
    }
]


@app.route('/')
def World():
    return "Hello Form Python World"



# get all employeeModel data start
@app.route('/getuserinfo')
def custom_jsonencoder():
    user=User()
    data=user.getAllUser()

    respones = Response(json.dumps({'user':user.getAllUser()}), status=200, mimetype="application/json")
    return respones


@app.route('/emp')
def getEmp():
    employeeobj = Employee()
    print("hii", request)
    print("test", employeeobj.get_limit_emp())
    # return jsonify({'emp':employeeobj.get_limit_emp()})
    respones = Response(json.dumps({'emp': employeeobj.get_limit_emp()}), status=200, mimetype="application/json")
    return respones;


@app.route('/addemp', methods=['POST'])
def addemployee():
    getemp_data = request.get_json()
    print("getempdata", getemp_data['EmpName'])
    Employee.add_new_emp(getemp_data['EmpName'])
    response = Response("", 201, mimetype='application/json')
    # response.headers['Location'] = "/books/" + str(getemp_data['id'])
    return response


# employeemodel data end
# get all books Start
@app.route('/books')
@token_requierd
def get_AllBook():
    # token=request.args.get('token')
    # try:
    #     jwt.decode(token,app.config['SECRET_KEY'])
    # except:
    #     return jsonify({'error':'there something wrong'}),401
    return jsonify({'books': books})


# get all books end


# validation start of book parameter
def isValidbook(bookData):
    if ("name" in bookData and "author" in bookData and "prise" in bookData):
        return True
    else:
        return False


# validation End of book parameter

# post method start
@app.route('/books', methods=['POST'])
def add_newBook():
    get_bookData = request.get_json()
    if (isValidbook(get_bookData)):
        new_book = {
            'id': id(0),
            'name': get_bookData['name'],
            'author': get_bookData['author'],
            'prise': get_bookData['prise']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['id'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid Book object passed in request",
            "helpString": "Data Passed in Similar to this ({'id':number,'name':string,'author':string,'prise':string'})"

        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


# post method End

# put method start
def not_valid_put_data(req_data):
    if ("name" in req_data and "prise" in req_data and "author" in req_data):
        return True
    else:
        return False


@app.route('/book/<int:id>', methods=['PUT'])
def UpdatebookRecords(id):
    requested_data = request.get_json()
    if (not not_valid_put_data(requested_data)):
        invalidErrorMsg = {
            "error": "Valid Book object must be Passed in Request",
            "helpString": "Data Passed in Similar to this ({'name':string,'prise':string','author':string})"
        }
        respones = Response(json.dumps(invalidErrorMsg), status=400, mimetype="application/json")
        return respones;
    new_book = {
        'id': id,
        'name': requested_data['name'],
        'author': requested_data['author'],
        'prise': requested_data['prise']

    }
    i = 0;
    for book in books:
        currentId = book['id']
        if (currentId == id):
            books[i] = new_book
            i += 1
        respones = Response("", status=204)
        return respones


# put method End

# patch method start
@app.route('/books/<int:id>', methods=['PATCH'])
def updateSingleRecords(id):
    request_data = request.get_json();
    update_book = {}
    if ("name" in request_data):
        update_book["name"] = request_data['name']
    if ("author" in request_data):
        update_book["author"] = request_data['author']
    if ("prise" in request_data):
        update_book["prise"] = request_data['prise']
        for book in books:
            if (book["id"] == id):
                book.update(update_book)
                response = Response("", status=204)
                response.headers['Location'] = '/books/' + str(id)
                return response


# patch method ends

# delete method Start
@app.route('/book/<int:id>', methods=['DELETE'])
def deleteBook(id):
    i = 0;
    for book in books:
        if (book['id'] == id):
            books.pop(i)
            response = Response("", status=204)
            return response
            i += 1
        else:
            invalidErrorMsg = {
                "error": "book with id that provided not found"
            }
            response = Response(json.dumps(invalidErrorMsg), status=404, mimetype="application/json")
            return response


# delete method Endss

# get item throug id start
@app.route('/book/<int:id>')
@token_requierd
def get_bookById(id):
    book_value = {}
    for item in books:
        if item["id"] == id:
            book_value = {
                'name': item['name'],
                'author': item['author'],
                'prise': item['prise']
            }
            return jsonify(book_value)


# get item throug id End
app.run(port=5002)
