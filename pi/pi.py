# Campus Gong Raspberry Pi module
# Victor Verchkovski 2019

from datetime import datetime
from playsound import playsound
from requests import get, post
from time import sleep
from sys import argv

url = 'localhost:8000' # rings gong audio
def ring():
    playsound('gong.mp3')


# gets the schedule from django app using the /get_schedule request
# format of the results is a list of (year, month, day, hour, minute)
# in string (json) format, we add these to the events set and return 
# to the scheduler
def get_schedule(pi_id):
    result = get(url+'/get_schedule/'+pi_id)
    if 'events' in result:
        return result['events']
    else:
        # notify issue
        return None


# checks if the candidate is still in the schedule or needs to be muted
# format of the response is:
# ['valid' : 'True' or 'False', 'mute' : 'True' or 'False']
def check_valid(pi_id, candidate):
    year, month, day, hour, minute = candidate
    result = get(url+'/check_valid?pi_id='+pi_id+'&year='+year+'&month='+month+'&day'+day+'&hour'+hour+'&minute'+minute)
    if 'valid' in result and result['valid'] == '1':
        return True
    elif 'mute' in result and result['mute'] == '1':
        return False
    else:
        # notify of issue
        # by default do not mute since we want the gongs to keep ringing
        # if the django app is down
        return True


# checks if the schedule needs updating 
# format of the response is:
# ['update' : 'True' or 'False']
def check_update():
    result = get(url+'/check_update')
    return True if 'update' in result and result['update'] == 'True' else False


# posts a message to the django app
def message(msg):
    post(url+'/response', {'message': msg})


# scheduler runs in an infinite loop, checking for a gong event every minute
# checking if the schedule needs to be updated every hour
def scheduler(pi_id):
    events = None
    prev_hour = -1
    while True:
        try:
            # get current time
            now = datetime.now()
            candidate = (now.year, now.month, now.day, now.hour, now.minute)
            
            # update schedule if necessary
            if not events or (prev_hour != now.hour and check_update()):
                events = get_schedule(pi_id)
                prev_hour = now.hour
            
            # check if we need to ring the gong
            if candidate in events:
                if check_valid(pi_id, candidate):
                    ring()
                    message('rang '+'-'.join(candidate))
                else:
                    message('did not ring invalid candidate '+'-'.join(candidate))
                events.remove(candidate)
    
            # check every minute
            time.sleep(61 - now.second)
    
        except:
            # notify error
            continue

# Test:
# independent
# playing sound
# correct datetime

# once django is up
# each request
# run through a day of rings

if __name__ == '__main__':
    pi_id = argv[0]
    scheduler(pi_id)
