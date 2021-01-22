#!/usr/bin/python3 -W ignore::DeprecationWarning

import json
import requests
import time
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
move this to apifunction lib in future
"""
def login_api(key, mds, domain):
    payload = {"api-key" : key, "domain" : domain}
    response = apifunctions.api_call(mds, "login", payload, "")

    return response["sid"]
#end of api

def build_group_list():
    group_list = list()
    debug = 0

    url = "http://localhost:5000/group_list"

    headers = {"Accept" : "application/json"}

    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        ##got a good reply
        group_json = response.json()

        if(debug == 1):
            print(group_json['group_names'])

        for name in group_json['group_names']:
            group_list.append(name)
    else:
        if(debug == 1):
            print("NON 200 return code")
        pass
    #print(response.json())

    return(group_list)
#end of build_group_list

def check_cma(mds, cma, grp_list):
    debug = 1

    key = {}
    with open('apirw-key.json', 'r') as f:
        key = json.load(f)
        
        if(debug == 1):
            print(key)
            print(key['api-key'])
    
    if(debug == 1):
        print(mds)
        print(cma)

    sid = login_api(key['api-key'], mds, cma)

    if(debug == 1):
        print(sid)


    for grp in grp_list:
        print(grp, end="**\n")
        if(apifunctions.group_exist(mds, grp, sid)):
            print("exist")
            grp_json = {
                "name" : grp
            }
            get_grp_contents_json = apifunctions.api_call(mds, "show-group", grp_json, sid)

            print(json.dumps(get_grp_contents_json))
            print("******")
            print(get_grp_contents_json['members'])
            """
            need to sort, analyze here
            """

    time.sleep(5)
    apifunctions.api_call(mds, "logout", {}, sid)

def main():
    print("")

    cma_list = ["146.18.96.26","146.18.96.27"]
    groups_to_check = list()

    print(cma_list)

    print(cma_list[1])

    for cma in cma_list:
        print("-- " + cma)

    groups_to_check = build_group_list()
    print("-" * 10)
    print(groups_to_check)
    print("*" * 10)

    check_cma("146.18.96.16", cma_list[0], groups_to_check)


#end of main

if __name__ == "__main__":
    main()
#end of program