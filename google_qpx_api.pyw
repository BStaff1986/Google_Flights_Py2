from classes.google_flights import Google_Flights
import schedule
import time

# NOTE: Currently this code will fail in the IPython console but it will run
# successfully from the command line
    
def get_flights():
    print(time.strftime('%X'))
    Google_Flights()

schedule.every().day.at("8:15").do(get_flights)

while 1:
    schedule.run_pending()
    time.sleep(1)
