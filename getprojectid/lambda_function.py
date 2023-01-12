import json
import pymysql
import os
import utils.util as ut

connection = pymysql.connect(
    host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])


def lambda_handler(event, context):
    print(event)
    data = json.loads(event['body'])
    project_title = data['project_name']
    cur = connection.cursor()
    cur.execute(
        f'select id from projects where project_name = "{project_title}" ')
    rdsprojectid = cur.fetchone()
    cur.close()
    return ut.buildResponse(200, rdsprojectid)
