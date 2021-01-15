#!/usr/bin/python3

import json
import uuid
import time
import os
import shutil
import pathlib

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

def main():
    debug = 1

    json_data = {}

    name_2_find = "LAB-eai-1-dev"
    range_2_add = "40.0.0.1"

    #### uid
    tmp_uid = uuid.uuid4()
    print(tmp_uid)

    stamp = time.time()
    print(int(stamp))

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

    makefilebackup('ts.json')

    with open('./ts.json', 'w') as F:
        json.dump(json_data, F)

#end of main

if __name__ == "__main__":
    main()
#end of testing