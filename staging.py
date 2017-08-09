import sys
import os
import argparse
import re
import time
import datetime
from common import constants



def main():
    
    dict1=dict()
    parser = argparse.ArgumentParser(description='Verify AlertingScheme passed.')
    parser.add_argument('AlertingScheme', help='Add a AlertingScheme string'
        #,required=True
        )
    args = parser.parse_args()
    if args.AlertingScheme is not None:
        print "Alerting Scheme has been set (value is %s)" % args.AlertingScheme
    else:
        print "Please run again, this time provide an argument"
        sys.exit(1)
    try:
    	_as = args.AlertingScheme
        if(reg_check(_as)):
            add_alerts(_as)
            bool1=compareNotification(dict1,time.time())
            if bool1==False:
                recoursion_check(dict1,time.time() + datetime.timedelta(minutes=5))
    except Exception as e:
        sys.exit(1)


def reg_check(input_str):
    reg="([A-Z])\w+"
    #reg="^[\w-]+"
    regex = re.compile(reg, re.IGNORECASE)
    result=regex.match(input_str)
    if result!=None:
        return True
    else:
        raise Exception("-E- this is an illegal argument")
        return False

def add_alerts(input_str):
    #print 'example=SUN-THU@09:00-18:00&FRI@10:00-13:00'
    #print 'example=SUN-SAT@09:00-18:00'
    #print 'example=SUN&TUE'
    #print 'example=09:00-14:00&16:00-18:00'
    #print 'example='
    #print 'example='
    item_arr=input_str.split('&')
    for item in item_arr:
        patch_arr = item.split('@')
        for patch in patch_arr:
            validatePatch(str(patch))
        createAlert(item)

def validatePatch(input_str):
    str_case=input_str[:1]
    if str_case.isdigit():
        time=input_str.split('-')
        for t in time:
            if not isTimeFormat(t):
                sys.exit(1)
    else:
        day=input_str.split('-')
        for d in day:
            if d.upper() not in constants.DAYS:
                print "This is not a recognizable day"
                sys.exit(1)
    #valid = re.match('^[\w-]+$', str) is not None

def isTimeFormat(input_str):
    try:
        time.strptime(input_str, '%H:%M')
        return True
    except ValueError:
        return False

def createAlert(input_str):
    item_arr=input_str.split('@')
    dict1=dict()
    if len(item_arr)==1:
        if item_arr[0][:1].isdigit():
            print "make an alert for all 7 days"
            createAlert("SUN-SAT@"+input_str)
        else:
            print "make an alert for all 24 hours"
            createAlert(input_str+"@00:00-23:59")
    else:
        time_arr=item_arr[1].split('-')
        start_time = time.strptime(time_arr[0], "%H:%M")
        end_time = time.strptime(time_arr[1], "%H:%M")
        start_time=int(start_time.tm_hour)*60+int(start_time.tm_min)
        end_time=int(end_time.tm_hour)*60+int(end_time.tm_min)
        # Now for the day
        day_arr=item_arr[0].split('-')
        day_arr=[d.upper() for d in day_arr]
        #MON-FRI
        #FRI-MON
        daysflag=False
        for d in constants.DAYS:
            if d==day_arr[0]:
                daysflag=True
                dict1[d] = [start_time,end_time]; # Add new entry
            if d==day_arr[1]:
                daysflag=False
                dict1[d] = [start_time,end_time]; # Add new entry
            if daysflag==True:
                dict1[d] = [start_time,end_time]; # Add new entry
        if daysflag==True:
            for d in constants.DAYS:
                if d==day_arr[1]:
                    daysflag=False
                    dict1[d] = [start_time,end_time]; # Add new entry
                if daysflag==True:
                    dict1[d] = [start_time,end_time]; # Add new entry
        return True

def compareNotification(dict1,now_time)
        temp_time=time.strptime(now_time, "%H:%M")
        temp_time=int(temp_time.tm_hour)*60+int(temp_time.tm_min)
        now_day = datetime.datetime.fromtimestamp(now_time).strftime('%a')
        arr_compare=dict1[now_day]
        if arr_compare[0] <= temp_time <= arr_compare[1]:
            print "NOW"
            return True
        else:
            return False
def recoursion_check(dict1,next_time)
        temp_time=time.strptime(next_time, "%H:%M")
        temp_time=int(temp_time.tm_hour)*60+int(temp_time.tm_min)
        now_day = datetime.datetime.fromtimestamp(next_time).strftime('%a')
        arr_compare=dict1[now_day]
        if arr_compare[0] <= temp_time <= arr_compare[1]:
            print next_time
            return True
        else:
            recoursion_check(dict1,next_time + datetime.timedelta(minutes=5))


if __name__ == "__main__":
    main()
