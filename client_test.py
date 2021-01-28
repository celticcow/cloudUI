#!/usr/bin/python3

import json
import requests

"""
client example code for hitting the firewall json group listing
"""

def main():
    print("client test")
    debug = 1

    root_url = "http://localhost:5000/"
    headers = {"Accept" : "application/json"}

    ### group listing ###
    group_list = list()

    url1 = root_url + "group_list"
    response = requests.get(url1, headers=headers)
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
    ### group listing ###

    ### get group contents ###

    for grp in group_list:
        print(grp)

        url2 = root_url + "group_content"
        grp_json = {
            "name" : grp
        }

        #could also pass in json=grp_json arg instead of data=
        response = requests.post(url2, headers=headers, data=json.dumps(grp_json))

        if(response.status_code == 200):
            ##got a good reply
            flask_grp_members = response.json()
            if(debug == 1):
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print(flask_grp_members)
                print(flask_grp_members['ranges'])
        else:
            print("non 200 response for group members")
    # end of for loop of groups

    ### add to group ###
    add_host_2_group = {
        "name" : "LAB-eai-1-dev",
        "ip2add" : "40.0.0.9"
    }

    url3 = root_url + "add_to_group"
    response = requests.post(url3, headers=headers, data=json.dumps(add_host_2_group))

    if(response.status_code == 200):
        ##got a good reply
        flask_add_result = response.json()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(flask_add_result)
    else:
        print("add code not 200")
     
#end of main

if __name__ == "__main__":
    main()
#end of client test