#!/usr/bin/python3

import requests
import json
import time

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
    
    with open('./example1.json', 'r') as f:
        group_json = json.load(f)
    
    for i in range(len(group_json['objects'])):
        print(group_json['objects'][i]['name'])
        result_json['group_names'].append(group_json['objects'][i]['name'])

    return(result_json)
#end of funtion

@app.route('/group_content', methods=['POST'])
def group_content():
    #
    debug = 1

    group_json = {}
    result_json = {}
    
    group_2_find = request.get_json(force=True)
    grp_name = group_2_find['name']

    print(grp_name)

    with open('./example1.json', 'r') as f:
        group_json = json.load(f)
    
    for i in range(len(group_json['objects'])):
        if(group_json['objects'][i]['name'] == grp_name):
            result_json['name'] = group_json['objects'][i]['name']
            result_json['ranges'] = group_json['objects'][i]['ranges']

            print(group_json['objects'][i]['name'])
            print(group_json['objects'][i]['ranges'])

    return(result_json)
#end of funtion

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#end of program