import json
import pymysql
import os
import utils.util as ut

connection = pymysql.connect(
    host=os.environ['endpoint'], user=os.environ['username'], passwd=os.environ['password'], db=os.environ['database_name'])


def lambda_handler(event, context):
    print(event)
    print(json.dumps(event))
    data = json.loads(event['body'])
    print(event['body'])
    return add_project(data)


def add_project(event):
    project_id = event['project_id']
    project_name = event['project_name']
    project_desc = event['project_desc']
    project_creator = event['project_creator']
    project_tech = event['project_tech']
    date_time = event['date_time']

    project = {
        "project_id": project_id,
        "project_name": project_name,
        "project_desc": project_desc,
        "project_creator": project_creator,
        "project_tech": project_tech,
        "date_time": date_time
    }

    if(project_name == ""):
        return{
            "statusCode": 401,
            "body": 'Project name is required'
        }
    project_name = getProjectName(project_name)
    if project_name != None:
        return{
            "statusCode": 401,
            "body": 'Project already exists'
        }
    else:
        saveProjectInfo(project)

    return ut.buildResponse(200, {'message': 'Project created successfully'})


def getProjectName(project_name):
    cur = connection.cursor()
    cur.execute(
        f'select project_name from projects where project_name = "{project_name}" ')
    rdsuser = cur.fetchone()
    cur.close()
    return rdsuser


def saveProjectInfo(project):
    print('worked')
    cur = connection.cursor()
    cur.execute(
        f'insert into projects (id, project_name, project_desc, project_creator, date_time, tech) values ("{project["project_id"]}", "{project["project_name"]}", "{project["project_desc"]}", "{project["project_creator"]}", "{project["date_time"]}", "{project["project_tech"]}")')
    cur.close()
    connection.commit()
