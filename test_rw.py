#!/usr/bin/python3

import json
import uuid

def main():
    debug = 1

    json_data = {}

    name_2_find = "LAB-eai-1-dev"
    range_2_add = "40.0.0.1"

    #### uid
    uuid = uuid.uuid4()
    print(uuid)


    with open('./ts.json', 'r') as f:
        json_data = json.load(f)

    print("-------------------------------------------")
    print(json_data['objects'][0])
    print("*******************************************")

    for i in range(len(json_data['objects'])):
        if(json_data['objects'][i]['name'] == name_2_find):
            ##
            print("ranges for that name = ")
            print(json_data['objects'][i]['ranges'])

            json_data['objects'][i]['ranges'].append(range_2_add)

            print(json_data['objects'][i]['ranges'])


    print("-------------------------------------------")
    print(json_data['objects'][0])
    print("*******************************************")
    
    print(json.dumps(json_data))

    #with open('./ts.json', 'w') as F:
    #    json.dump(json_data, F)

#end of main

if __name__ == "__main__":
    main()
#end of testing