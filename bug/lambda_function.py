import json
import pymysql
import os
import utils.util as ut


def lambda_handler(event, context):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    print(event)
    print(json.dumps(event))
    data = json.loads(event['body'])
    print(event['body'])
    return add_bug(data)


def add_bug(event):
    bug_id = event['bug_id']
    bug_name = event['bug_name']
    bug_desc = event['bug_desc']
    bug_creator = event['bug_creator']
    bug_priority = event['bug_priority']
    bug_time = event['bug_time']
    project_id = event['project_id']

    bug = {
        "bug_id": bug_id,
        "bug_name": bug_name,
        "bug_desc": bug_desc,
        "bug_creator": bug_creator,
        "bug_priority": bug_priority,
        "date_time": bug_time,
        "project_id": project_id,
    }

    if(bug_name == ""):
        return{
            "statusCode": 401,
            "body": 'Bug name is required'
        }
    rds_bug_name = getBugName(bug_name)
    if rds_bug_name != None:
        return{
            "statusCode": 401,
            "body": 'Bug already exists'
        }
    else:
        saveBugInfo(bug)

    return ut.buildResponse(200, {'message': 'Bug created successfully'})


def getBugName(bug_name):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    cur = connection.cursor()
    cur.execute(
        f'select bug_name from bugs where bug_name = "{bug_name}" ')
    rdsuser = cur.fetchone()
    cur.close()
    return rdsuser


def saveBugInfo(bug):
    connection = pymysql.connect(
        host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])
    print('worked')
    cur = connection.cursor()
    cur.execute(
        f'insert into bugs (id, bug_name, bug_desc, bug_priority, date_time, bug_creator, project_id) values ("{bug["bug_id"]}", "{bug["bug_name"]}", "{bug["bug_desc"]}", "{bug["bug_priority"]}", "{bug["date_time"]}", "{bug["bug_creator"]}", "{bug["project_id"]}")')
    cur.close()
    connection.commit()
