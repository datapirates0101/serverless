import json
import pymysql
import os
import utils.util as ut

def lambda_handler(event, context):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    cur = connection.cursor()
    cur.execute("SELECT * FROM projects")
    rdsprojects = cur.fetchall()
    cur.close()
    return ut.buildResponse(200, rdsprojects)

