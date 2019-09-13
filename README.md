# Weather Proxy API

Starts api which provides a current weather information 
from other weather services using specified format:


### Request
`GET: /weather/current/`

`curl -i -H 'Accept: application/json' http://localhost:5000/weather/current/`

### Response

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 175
Server: Werkzeug/0.15.6 Python/3.7.4
Date: Fri, 13 Sep 2019 16:52:37 GMT
```

```json
{
  "humidity": {
    "percent": 100
  },
  "location": {
    "lat": 55.03,
    "lon": 82.92
  },
  "pressure": {
    "atm": 764
  },
  "temperature": {
    "C": 2.0
  },
  "timestamp": "2019-09-13T14:45:44+07:00",
  "title": "Novosibirsk"
}
```
