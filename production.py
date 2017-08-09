import sys
import os
import argparse
import re
import time
import datetime
from common import constants



def main():
    
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
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
