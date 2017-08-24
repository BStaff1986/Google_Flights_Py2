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
In the home directory of this project you will find a file titled google_qpx_api.pyw. This script simply runs ./classes/google_flights.py every morning at 8:00 am. Here is a general overview of the work flow of 
</p>


<p align='center'>
<img src='https://github.com/BStaff1986/Google_Flights_Py2/blob/master/qpx_flowchart.PNG'><br>
  <i>An overview of google_flights.py</i>
</p>
