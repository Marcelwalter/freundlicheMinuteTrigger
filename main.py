import requests
import datetime
import sys
import time 
import os
import signal
import argparse
#from signal import signal, SIGTERM


# ProPresenter API details
PRO_PRESENTER_IP = "127.0.0.1"
PRO_PRESENTER_PORT = "1025"
BASE_URL = f"http://{PRO_PRESENTER_IP}:{PRO_PRESENTER_PORT}/v1"

# The name of the presentation and timer
PRESENTATION_NAME = "FreundlicheMinute"
TIMER_NAME = "Freundliche Minute"

# Making sure only one instance of this script can run at the same time
# This works by storing current the process ID into a PID file
# If there is already a PID file, try to kill the process of it
# https://www.youtube.com/watch?v=H98hWrVRYFo 
CWD = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
PID = os.path.sep.join([CWD,'PID'])
PIDFILE = os.path.sep.join([PID,'pidfile'])

print(CWD)

def single_process():
    #Create PID folder
    if not os.path.exists(PID):
        os.makedirs(PID)

    MYPID = os.getpid()

    if os.path.isfile(PIDFILE):
            #print("Old process ID found!")
            try:
                    with open(PIDFILE,'r') as pidfile:
                            OLDPID = int(pidfile.read())
            except Exception as e:
                    OLDPID = None
                    #print(f"Could not convert the pid: {e}")
            if OLDPID:
                    try:
                            os.kill(OLDPID,signal.SIGTERM)
                            #print("Successfully killed the old process!")
                    except ProcessLookupError as e:
                            #print("No such process running!")
                            print('')
                    except Exception as e:
                            #print(f"Failed to kill the old process because: {e}")
                            raise SystemExit
            #else:
            #        print("The older process cannot be found!")

    #else:
    #        print("There is no previous instance running at the moment!")

    with open(PIDFILE,'w') as pidfile:
            pidfile.write(str(MYPID))


def get_current_playlist():
    """Retrieve the current playlist details from ProPresenter."""
    url = f"{BASE_URL}/playlist/active?chunked=false"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_playlist_by_name(name):
    """Retrieve the playlist 'Gottesdienst' details from ProPresenter."""
    url = f"{BASE_URL}/playlist/{name}"
    response = requests.get(url)
    response.raise_for_status()
    #new_json = json.dumps(response.json(), indent=2)
    #print(new_json)
    return response.json()

def get_current_playlist_items(playlist_uuid):
    """Retrieve the current playlist items from ProPresenter."""
    url = f"{BASE_URL}/playlist/{playlist_uuid}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def find_presentation_uuid(playlist, presentation_name):
    """Find the UUID of the specified presentation in the playlist."""

    for item in playlist['items']:
        if item['type'] == 'presentation' and item['id']['name'] == presentation_name:
            #new_json = json.dumps(item, indent=4)
            #print(new_json)
            #print(item['presentation_info']['presentation_uuid'])
            return item['presentation_info']['presentation_uuid']
    return None

def create_timer(countdown_seconds):
    # Create the timer with countdown_seconds
    timerJSON = {
        "allows_overrun": False,
        "count_down_to_time": {
            "period": "is_24_hour",
            "time_of_day": countdown_seconds
        },
        "name": TIMER_NAME
        }

    url = f"{BASE_URL}/timer"
    response = requests.post(url, json = timerJSON)
    response.raise_for_status()

def put_timer(timer, countdown_seconds):
    url = f"{BASE_URL}/timer/{TIMER_NAME}/start"

    # Set the timer with countdown_seconds
    timer_data = {
        "allows_overrun": False,
        "count_down_to_time": {
            "period": "is_24_hour",
            "time_of_day": countdown_seconds
        },
        "id": {
            "index": timer['id']['index'],
            "name": TIMER_NAME,
            "uuid": timer['id']['uuid']
        }
    }

    response = requests.put(url, json=timer_data)
    response.raise_for_status()

def get_timers(timer_name):
    url = f"{BASE_URL}/timers"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()   

def set_timer(end_time_str):
    """Set the timer to count down to the specified end time.
    If there is no countdown with specified name, a new one will be created"""

    now = datetime.datetime.now()
    end_time = datetime.datetime.strptime(end_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day)
    
    if end_time <= now:
        print("Specified time has already passed. Timer will not be set.")
        return

    # Calculate the countdown time in seconds
    countdown_seconds = int((end_time - now).total_seconds())

    countdown_to_time_in_seconds = end_time.hour * 3600 + end_time.minute * 60

    #print(countdown_to_time_in_seconds)

    """Gets all configured timers"""
    timers = get_timers(TIMER_NAME)
    
    for item in timers:
        if item['id']['name'] == 'Freundliche Minute':
            put_timer(item, countdown_to_time_in_seconds)
            return
        
    create_timer(countdown_to_time_in_seconds)
    start_timer()

def start_timer():
    url = f"{BASE_URL}/timer/{TIMER_NAME}/start"
    response = requests.get(url)
    response.raise_for_status()

def trigger_presentation(presentation_uuid, trigger_time_str):
    """Trigger the presentation at the specified time."""
    now = datetime.datetime.now()
    trigger_time = datetime.datetime.strptime(trigger_time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day)
    
    if trigger_time <= now:
        print("Specified time has already passed. Presentation will not be triggered.")
        return

    # Calculate the delay until trigger time in seconds
    delay = (trigger_time - now).total_seconds()
    
    print(f"Waiting for {int(delay)} seconds to trigger presentation...")

    # Wait until the specified time
    time.sleep(delay)

    # Trigger the presentation
    url = f"{BASE_URL}/presentation/{presentation_uuid}/trigger"
    response = requests.get(url)
    response.raise_for_status()
    print(f"Presentation '{PRESENTATION_NAME}' triggered.")

def main(trigger_time_str, playlist_name):
    # Get the uuid current playlist
    playlists = get_current_playlist()

    if  playlists['presentation']['playlist'] != None:
        print('Using current Playlist')
        playlist_uuid = playlists['presentation']['playlist']['uuid']
            
        # Get all playlist items
        playlist_details = get_current_playlist_items(playlist_uuid)
 
    else:
       #get playlist details of Gottesdienst instead
       playlist_details = get_playlist_by_name(playlist_name)
       print(f'Current playlist not found. Using backup Playlist: {playlist_name}')

    # Find the UUID of the desired presentation
    presentation_uuid = find_presentation_uuid(playlist_details, PRESENTATION_NAME)
    if not presentation_uuid:
        print(f"Presentation '{PRESENTATION_NAME}' not found in the current playlist.")
        return

    # Set the timer
    set_timer(trigger_time_str)

    # Trigger the presentation at the specified time
    trigger_presentation(presentation_uuid, trigger_time_str)


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("time", help="Uhrzeit der Freundlichen Minute in HH:MM.", type=str)

    # Optional arguments
    parser.add_argument("-bp", "--backupplaylist", help="Name der Playlist in der die Freundliche Minute gespielt werden soll, wenn keine aktive Playlist gefunden wird.", type=str, default='Gottesdienst')
    parser.add_argument("-n", "--name", help="Name der Präsentation die gespielt werden soll.", type=str, default='FreundlicheMinute')
    parser.add_argument("-t", "--timer", help="Name des Timers der gestartet werden soll.", type=str, default='Freundliche Minute')
    parser.add_argument("-np", "--networkport", help="Port auf dem ProPresenter Control zuhört.", type=str, default='1025')
    parser.add_argument("-i", "--ip", help="IP Adresse auf welcher ProPresenter zu erreichen ist.", type=str, default='10.0.30.2')

    # Print version
    parser.add_argument("--version", action="version", version='%(prog)s - Version 1.0')

    # Parse arguments
    args = parser.parse_args()

    return args

if __name__ == "__main__":

    try:
        args = parseArguments()
    except SystemExit as e:
        print("exit" )
        sys.exit(1)

    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print("  " + str(a) + ": " + str(args.__dict__[a]))
    
    trigger_time_str = args.time
    backup_playlist = args.backupplaylist
    PRESENTATION_NAME = args.name
    TIMER_NAME = args.timer
    PRO_PRESENTER_PORT = args.networkport
    PRO_PRESENTER_IP = args.ip

    single_process()
    
    main(trigger_time_str, backup_playlist)

    if os.path.isfile(PIDFILE):
        try:
            os.remove(PIDFILE)
            #print("The PIDfile has been removed!")
        except:
            #print("The remove has failed!")
            sys.exit(1)
        sys.exit(0)

    else:
        #print("No pid to remove!")
        sys.exit(0)