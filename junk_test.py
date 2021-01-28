#!/usr/bin/python3

import ipaddress
import smtplib

def ListDiff(li1, li2):
    return(list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def ListDiff1(li1, li2):
    return(list(set(li1)-set(li2)))


def ListDiff2(li1, li2):
    return(list(set(li2)-set(li1)))

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

def smail(e_message):
    FROM = 'greg@fedex.com'
    TO = ["gregory.dunlap@fedex.com"]
    SUBJECT = "JSON Add Request"
   
    message = 'Subject: {}\n\n{}'.format(SUBJECT, e_message)

    server = smtplib.SMTP('mapper.gslb.fedex.com')
    server.sendmail(FROM, TO, message)
    
    server.quit()

def main():
    print("testing only")

    list1 = ["192.168.50.2", "192.168.20.0/24", "192.168.1.4-192.168.1.99"]
    list2 = ["192.168.50.2", "192.168.1.4-192.168.1.99", "192.168.20.0/24"]
    list3 = ["192.168.50.2"]

    print(type(list1))
    print(list1)
    print("S P A C E")
    print(list2)

    list1.sort()
    list2.sort()

    print("-------------------------------")
    print(list1)
    print(list2)

    if(list1 == list2):
        print("equal")
    else:
        print("NOT equal")
    
    print(ListDiff(list1, list2))
    print(ListDiff(list1, list3))
    print(ListDiff(list3, list1))

    print(ListDiff1(list1, list3))
    print(ListDiff1(list3, list1))


    print(ListDiff2(list1, list3))
    print(ListDiff2(list3, list1))

    print(whatami('192.168.1.1'))
    print(whatami('192.168.1.0/24'))
    print(whatami('192.168.1.5-192.168.4.5'))

    smail("need to add stuff\nand more stuff\nbut not too much")
    smail("BOOM")

    print("END")


if __name__ == "__main__":
    main()   