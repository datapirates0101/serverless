import json
import pymysql
import os
import utils.util as ut


def lambda_handler(event, context):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    data = json.loads(event['body'])
    project_id = data['project_id']
    cur = connection.cursor()
    cur.execute(f'SELECT * FROM bugs where project_id = "{project_id}" ')
    rdsbugs = cur.fetchall()
    cur.close()
    return ut.buildResponse(200, rdsbugs)
