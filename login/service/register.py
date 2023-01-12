import pymysql
import utils.util as ut
import os
import bcrypt


def register(event):
    firstname = event['firstname']
    lastname = event['lastname']
    username = event['username']
    email = event['email']
    password = event['password']

    if(firstname == "" or lastname == "" or username == "" or email == "" or password == ""):
        return ut.buildResponse(401, {'message': 'missing required fields'})

    rdsuser = getUserName(username)
    print(rdsuser)
    if(rdsuser != None):
        return ut.buildResponse(401, {'message': 'username already exists'})

    rdsemail = getemail(email)
    if(rdsemail != None):
        return ut.buildResponse(401, {'message': 'email already exists'})

    encodedPass = password.encode('utf-8')
    salt = os.environ['salt'].encode('utf-8')
    hashedPass = bcrypt.hashpw(encodedPass, salt)

    user = {
        'firstname': firstname,
        'lastname': lastname,
        'username': username.lower(),
        'email': email.lower(),
        'password': hashedPass.decode()
    }

    saveUserInfo(user)

    return ut.buildResponse(200, {'message': 'user created successfully'})


def getUserName(username):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    cur = connection.cursor()
    cur.execute(f'select username from user where username = "{username}" ')
    rdsuser = cur.fetchone()
    cur.close()
    return rdsuser


def getemail(email):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    cur = connection.cursor()
    cur.execute(f'select email from user where email = "{email}" ')
    rdsemail = cur.fetchone()
    cur.close()
    return rdsemail


def saveUserInfo(user):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    print('worked')
    cur = connection.cursor()
    cur.execute(
        f'insert into user (firstname, lastname, username, email, password) values ("{user["firstname"]}", "{user["lastname"]}", "{user["username"]}", "{user["email"]}", "{user["password"]}")')
    cur.close()
    connection.commit()
