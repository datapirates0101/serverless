import pymysql
import utils.util as ut
import service.register as reg
import os
import bcrypt


def login(event):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    username = event['username']
    password = event['password']

    if(username == "" or password == ""):
        return ut.buildResponse(401, {'message': 'missing required fields'})

    rdsuser = reg.getUserName(username)
    if(rdsuser == None):
        return ut.buildResponse(401, {'message': 'username does not exist'})

    encodedPass = password.encode('utf-8')
    salt = os.environ['salt'].encode('utf-8')
    hashed = bcrypt.hashpw(encodedPass, salt)
    rdspassword = getPasswordByUsername(username)

    if(rdspassword[0] != hashed.decode()):
        return ut.buildResponse(401, {'message': 'incorrect password'})

    return ut.buildResponse(200, {'message': 'user logged in successfully'})


def getPasswordByUsername(username):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    cur = connection.cursor()
    cur.execute(f'select password from user where username = "{username}" ')
    rdsuserpass = cur.fetchone()
    cur.close()
    return rdsuserpass


def getUserName(username):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    cur = connection.cursor()
    cur.execute(f'select username from user where username = "{username}" ')
    rdsuser = cur.fetchone()
    cur.close()
    return rdsuser
