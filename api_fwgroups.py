#!/usr/bin/python3

import requests
import json
import time
import os
import shutil
import pathlib

from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
api information
"""

app = Flask(__name__)
FlaskJSON(app)

"""
Helper functions / not api functions
"""
def makefilebackup(file_name):
    print("backup")

    file_parts = file_name.split('.')
    print(file_parts[0])
    print(file_parts[1])

    stamp = int(time.time())
    new_file_name = file_parts[0] + "-" + str(stamp) + "." + file_parts[1]

    print(new_file_name)

    data1 = pathlib.Path(file_name).parent.absolute()

    f1 = str(data1) + "/" + file_name
    f2 = str(data1) + "/" + new_file_name

    print(data1)

    shutil.copy(f1, f2)
#end of makefilebackup

"""
return list of groups that are in teh json file 
on remote server. 
this assumes the json file is on local disk.
"""
@app.route('/group_list')
def group_list():
    #
    debug = 1

    group_json = {}
    result_json = {}
    result_json['group_names'] = []
    
    with open('./group1.json', 'r') as f:
        group_json = json.load(f)
    
    for i in range(len(group_json['objects'])):
        print(group_json['objects'][i]['name'])
        result_json['group_names'].append(group_json['objects'][i]['name'])

    return(result_json)
#end of funtion

"""
return contents of group names range info
"""
@app.route('/group_content', methods=['POST'])
def group_content():
    #
    debug = 1

    group_json = {}
    result_json = {}
    
    group_2_find = request.get_json(force=True)
    grp_name = group_2_find['name']

    print(grp_name)

    with open('./group1.json', 'r') as f:
        group_json = json.load(f)
    
    for i in range(len(group_json['objects'])):
        if(group_json['objects'][i]['name'] == grp_name):
            result_json['name'] = group_json['objects'][i]['name']
            result_json['ranges'] = group_json['objects'][i]['ranges']

            print(group_json['objects'][i]['name'])
            print(group_json['objects'][i]['ranges'])

    return(result_json)
#end of funtion

"""
"""
@app.route('/add_to_group', methods=['POST'])
def add_to_group():
    #
    debug = 1

    group_json = {}

    group_2_add_2 = request.get_json(force=True)
    grp_name = group_2_add_2['name']
    grp_data = group_2_add_2['ip2add']

    with open('./group1.json', 'r') as f:
        group_json = json.load(f)
    
    for i in range(len(group_json['objects'])):
        if(group_json['objects'][i]['name'] == grp_name):
            if(debug == 1):
                print("-------------------------------------------")
                print(group_json['objects'][i]['name'])
                print(group_json['objects'][i]['ranges'])
                print("-------------------------------------------")

            group_json['objects'][i]['ranges'].append(grp_data)

    #print(grp_name, end=" ")
    #print(grp_data)
    print("+++++++++++++++++++++++++++++++++++++++")

    makefilebackup("group1.json")

    with open('./group1.json', 'w') as F:
        json.dump(group_json, F)

    return(group_json)
#end of function

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#end of program