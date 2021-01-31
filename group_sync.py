#!/usr/bin/python3 -W ignore::DeprecationWarning

import json
import requests
import time
import smtplib
import ipaddress
import logging
import logging.handlers
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

"""
take 2 lists, send you the difference between the 2
"""
def ListDiff(li1, li2):
    return(list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

"""
List1 has things List2 doens't
"""
def ListDiff1(li1, li2):
    return(list(set(li1)-set(li2)))
"""
List2 has things List1 doesn't
"""
def ListDiff2(li1, li2):
    return(list(set(li2)-set(li1)))

#end of difference set functions

def smail(e_subject, e_message):
    FROM = 'greg@fedex.com'
    TO = ["gregory.dunlap@fedex.com"]
    SUBJECT = e_subject#"JSON Add Request"
   
    message = 'Subject: {}\n\n{}'.format(SUBJECT, e_message)

    server = smtplib.SMTP('mapper.gslb.fedex.com')
    server.sendmail(FROM, TO, message)
    
    server.quit()
#end of smtp function

def sendtosyslog(message):
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.INFO)

    handler = logging.handlers.SysLogHandler(address='/dev/log')

    my_logger.addHandler(handler)
    my_logger.info(message)
#end of sendtosyslog

def build_group_list():
    group_list = list()
    debug = 0

    url = "http://localhost:5000/group_list"

    headers = {"Accept" : "application/json"}

    try:
        response = requests.get(url, headers=headers)
    except:
        ## unable to get response from the flask
        smail("FLASK Error", "Group Sync Error : can not reach flask")
        sendtosyslog("group_sync : error can not reach flask")
        exit()

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

def whatami(item):
    if('/' in item):
        try:
            if(ipaddress.ip_network(item)):
                return("network")
        except:
            return("NA")

    elif('-' in item):
        parts = item.split('-')
        try:
            if(ipaddress.ip_address(parts[0]) and ipaddress.ip_address(parts[1])):
                #is it 0 - 1 in order
                return("range")
        except:
            return("NA")
    else:
        try:
            if(ipaddress.ip_address(item)):
                return("host")
        except:
            return("NA")
    #catch all
    return("NA")
#end of whatami

def check_cma(mds, cma, grp_list):
    debug = 0

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
    #sid = apifunctions.login("gdunlap", "1qazxsw2", mds, cma)

    if(debug == 1):
        print(sid)

    for grp in grp_list:
        print(grp, end="**\n")
        if(apifunctions.group_exist(mds, grp, sid)):
            print("exist")

            cma_group_contents_list = list()

            grp_json = {
                "name" : grp
            }
            get_grp_contents_json = apifunctions.api_call(mds, "show-group", grp_json, sid)

            if(debug == 1):
                print(json.dumps(get_grp_contents_json))
                print("******")
                print(get_grp_contents_json['members'])

            tmp1 = get_grp_contents_json['members']
            #print(type(tmp1))

            for mem in get_grp_contents_json['members']:
                #print(mem)
                #print("_____________________")
                #print(mem['type'])

                if(mem['type'] == "host"):
                    if(debug == 1):
                        print(mem['ipv4-address'])
                    cma_group_contents_list.append(mem['ipv4-address'])
                elif(mem['type'] == "network"):
                    if(debug == 1):
                        print(mem['subnet4'])
                        print(mem['subnet-mask'])
                        print(mem['mask-length4'])

                    toadd = mem['subnet4'] + "/" + str(mem['mask-length4'])
                    cma_group_contents_list.append(toadd)

                elif(mem['type'] == "address-range"):
                    if(debug == 1):
                        print(mem['ipv4-address-first'])
                        print(mem['ipv4-address-last'])

                    toadd = mem['ipv4-address-first'] + "-" + mem['ipv4-address-last']
                    cma_group_contents_list.append(toadd)
                else:
                    #something went wrong here.
                    pass

            #grp_mem_len = len(get_grp_contents_json['members']
            #for i in len(get_grp_contents_json['members']):
                #print(get_grp_contents_json['members'][i])

            ## get flask group contents : use grp_json
            flask_grp_members = {}

            url = "http://localhost:5000/group_content"

            headers = {"Accept" : "application/json"}

            #response = requests.get(url, headers=headers, params=grp_json)
            response = requests.post(url, headers=headers, json=grp_json)
            if(response.status_code == 200):
                ##got a good reply
                flask_grp_members = response.json()
                if(debug == 1):
                    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                    print(flask_grp_members)
                    print(flask_grp_members['ranges'])

                json_file_list = flask_grp_members['ranges']
               
                ####
                # need to compare 
                if(debug == 1):
                    print("++++++++++++++++++++++++++++")
                    print(cma_group_contents_list)
                    print(json_file_list)

                cma_group_contents_list.sort()
                json_file_list.sort()


                file_need  = ListDiff1(cma_group_contents_list, json_file_list)
                cma_need   = ListDiff2(cma_group_contents_list, json_file_list)

                print("CMA Need :")
                print(cma_need)
                print("File Need :")
                print(file_need)
                ##
                # need to direct this some where.
                ##
                print("add this somewhere : ")
                print("add to group : " + grp, end="\n")
                print(file_need)

                ## if the file need is more than 0 meaning it has data to send ... email
                if(len(file_need) > 0):
                    file_message = "Modify json file\nadd the following to this group " + grp + "\n" + str(file_need) + "\nfound for cma : " + cma
                    smail("JSON Add Request", file_message)
                print("++++++++++++++++++++++++++++")

                for citem in cma_need:
                    print("--", end="")
                    print(citem)
                    print(whatami(citem))

                    """
                    need record of what's going on here.
                    """
                    if(whatami(citem) == "host"):
                        print("adding")
                        print(citem)
                        print(" to the group " + grp)

                        sendtosyslog("group_sync : adding " + citem + " host to the group + " + grp)
                        ####
                        #apifunctions.add_a_host_with_group()
                        apifunctions.add_a_host_with_group(mds, "host-"+str(citem), citem, grp, sid)
                    elif(whatami(citem) == "network"):
                        parts = citem.split('/')
                        sendtosyslog("group_sync : adding " + citem + " network to the group + " + grp)
                        apifunctions.add_a_network_with_group(mds, "network-"+str(parts[0]), parts[0], apifunctions.calcDottedNetmask(int(parts[1])), grp, sid)
                    elif(whatami(citem) == "range"):
                        parts = citem.split('-')
                        sendtosyslog("group_sync : adding " + citem + " address range to the group + " + grp)
                        apifunctions.add_a_range_with_group(mds, "range-"+citem, parts[0], parts[1], grp, sid)
                    else:
                        print("error 003 : not a host/network/range item")
                        sendtosyslog("group_sync error 003 : not a host/network/range item " + citem)
            
            else:
                print("error 001 : non 200 response code for group_contents")
                sendtosyslog("group_sync error 001 : non 200 response code for group_contents")


            """
            need to sort, analyze here
            """
        else:
            #group does not exist on cma
            print("error 002 : group does not exist on cma ")
            sendtosyslog("group_sync error 002 : group " + grp + " does not exist on cma " + cma)
            smail("error 002 on " + cma, "group " + grp + " does not exist on cma " + cma)
    #end of for loop

    """
    time to close this work out
    """
    #publish
    time.sleep(5)
    publish_results = apifunctions.api_call(mds, "publish", {}, sid)

    print("publish results : " + json.dumps(publish_results))

    time.sleep(20)
    logout_result = apifunctions.api_call(mds, "logout", {}, sid)

    print("logout results : " + json.dumps(logout_result))
#end of check cma

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

    check_cma("146.18.96.16", cma_list[1], groups_to_check)


#end of main

if __name__ == "__main__":
    main()
#end of program