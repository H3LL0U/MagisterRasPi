
from datetime import datetime
from time import ctime


def get_ntp_time():

    return datetime.now().ctime()

from datetime import datetime, timedelta

def add_day_to_date(date_str,days =1):
    # Parse the string to a datetime object
    date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
    
    # Add one day
    new_date_obj = date_obj + timedelta(days=days)
    
    # Format back to the original string format
    new_date_str = new_date_obj.strftime("%a %b %d %H:%M:%S %Y")
    
    return new_date_str


