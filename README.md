<p align='center'><h1>Google QPX Express API Python Script</h1></p>
<img src='https://github.com/BStaff1986/Google_Flights_Py2/blob/master/qpx_flowchart.png'><p>

<b>Purpose: </b>The purpose of this program is to acquire, parse, organize, and store flight information offered by Google's QPX Express API.<p>

<b>Set up directions: </b>Before running this program, the user will need to make a few changes:
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
</ul><p>

<b>Description: </b>Continue...
