import ntplib

from time import ctime


def get_ntp_time():
    # Create an NTP client instance
    client = ntplib.NTPClient()
    
    try:
        # Send a request to an NTP server (e.g., pool.ntp.org)
        response = client.request('pool.ntp.org', version=3)
        
        # Convert the response time to a human-readable format
        ntp_time = ctime(response.tx_time)
        return ntp_time  # Return as timestamp to set system time
    
    except Exception as e:
        print(f"Error while fetching NTP time: {e}")
        return None

from datetime import datetime, timedelta

def add_day_to_date(date_str,days =1):
    # Parse the string to a datetime object
    date_obj = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
    
    # Add one day
    new_date_obj = date_obj + timedelta(days=days)
    
    # Format back to the original string format
    new_date_str = new_date_obj.strftime("%a %b %d %H:%M:%S %Y")
    
    return new_date_str


