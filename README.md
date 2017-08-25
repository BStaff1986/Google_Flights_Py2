<p align='center'><h1>Google QPX Express API Python Script</h1></p>

<h3>Purpose</h3><br>
<p>
The purpose of this program is to acquire, parse, organize, and store flight information offered by Google's QPX Express API.
</p>

<h3>Set up directions</h3><br>
<p>
Before running this program, the user will need to make a few changes:
<ul>
  <li> <a href='https://developers.google.com/qpx-express/v1/prereqs'>Acquire a working API Key</a> for Google's QPX Express API</li>
    <ul>
      <li>Enter the API Key into ./files/requests_info/api_key.txt</li>
    </ul>
  <li> Enter your proxy username, password, and proxy host name and port into ./files/requests_info/proxy_login.txt</li>
  <li> Place an Excel file (titled 'flight_basket.xlsx') containing the city-pairs of interest into ./files/flight_basket/</li>
    <ul>
      <li> Follow the format seen below.</li>
      <li> Be sure to check to see if the city name is mapped to an airport code in ./classes/basket.py If it does not appear that row will be dropped.</li>
    </ul>
</ul>
</p>

<h3>Program Description</h3><br>
<p>
  In the home directory of this project you will find a file titled google_qpx_api.pyw. This script simply runs   ./classes/google_flights.py every morning at 8:00 am. Here is a general overview of the work flow of 
</p>


<p align='center'>
  <img src='https://github.com/BStaff1986/Google_Flights_Py2/blob/master/qpx_flowchart.PNG'><br>
  <i>An overview of google_flights.py</i>
</p>
<p>
  As seen in the flowchart, the program is divided into 3 phases: setup, process, and export.<br>
<h4>Setup Phase</h4><br>
  In the setup phase, four Python class objects are created to prepare the program: Date_Maker, DataFrame, Basket_Proffer, and Flight_Generator.<br>
  <ol>
    <li><b>Date_Maker</b> creates a dictionary containing all the dates necessary to fulfill the API requests and label the outputs. The dictionary includes today's date, the departure date for 4-and-8 week advanced bookings, and 7-and-14 day return flight dates.</li>
  <li><b>DataFrame</b> simply initializes a pandas DataFrame object that will later store all the parsed information received from Google’s API. The class includes methods to add the parsed data to the DataFrame and to export the DataFrame to an Excel file.</li>
  <li><b>Basket_Proffer</b> ensures that a list of flights to be priced with the Google API exists. It checks for basket.csv, which is a table of airport codes for the origin-destination pairs with their return dates included. If this file does not exist, it will look for flight_basket.xlsx which is a similar table but contains city-names instead of airport codes. If this file also does not exist, an error that ends the program will be raised.</li>
  <li><b>Flight_Generator</b> reads in the list of flights(basket.csv) and creates a generator object. The generator object allows for each flight to be handled individually.</li>
  </ol>
</p>
<p>
<h4>Process Phase</h4><br>
The processing phase begins by passing a flight from the flight generator object to the <b>JSON_Requester</b> class.  This class handles everything necessary for interacting with Google’s API. It formats the flight information into the JSON format expected by Google, logs onto the proxy network, and posts the request. Google’s JSON response is then saved to the hard-drive and passed to the <b>Parser</b> object. This object finds all the information of interest and organizes it in a series of nested dictionaries. These dictionaries are then passed to the previously created DataFrame, where they are stored.
</p>
<p>
<h4>Export Phase</h4><br>
The final phase is initiated when the generator object created by Flight_Generator no longer has any flights to pass to JSON_Requester. When this occurs, the export_to_excel method of the DataFrame is called. All of the data stored in the DataFrame is then saved in an Excel file to ./files/flight_results.
</p>
