#!/bin/bash
echo 'FROM python:3.7-alpine' > Dockerfile
echo 'WORKDIR /wpapi' >> Dockerfile
echo 'RUN apk add --no-cache gcc musl-dev linux-headers' >> Dockerfile
echo 'COPY requirements.txt requirements.txt' >> Dockerfile
echo 'RUN pip install -r requirements.txt' >> Dockerfile
echo 'COPY . .' >> Dockerfile
echo '' >> Dockerfile

service='service'
while :; do
  case "$service" in
    'OpenWeatherMapAPI'|'FakeWeatherAPI') break ;;
    *)
        if [ "$service" = "" ]
        then
            service='OpenWeatherMapAPI'
        else
            read -p 'Select weather api [OpenWeatherMapAPI, FakeWeatherAPI] (default OpenWeatherMapAPI): ' service
        fi
        ;;
  esac
done

read -sp 'Weather api token: ' token
echo ''

read -p 'City geo location, latitude [-90, 90] (default 55.03): ' latitude
if [ "$latitude" = "" ]
    then
        latitude='55.03'
fi

read -p 'City geo location, longitude [-180, 180] (default 82.92): ' longitude
if [ "$longitude" = "" ]
    then
        longitude='82.92'
fi

read -p 'Minimum seconds between requests to API (default 60): ' timeout
if [ "$timeout" = "" ]
    then
        timeout='60'
fi

if [ "$token" != "" ]
    then
        echo ENV WEATHER_API_TOKEN $token >> Dockerfile
fi

echo CMD python run.py -s $service -lat $latitude -lon $longitude -t $timeout >> Dockerfile

echo building docker with $service service, latitude=$latitude, longitude=$longitude, timeout=$timeout

set -e
docker build -t wpapi .
echo -e -n '\033[32mSuccess buid '
echo $service, with latitude=$latitude, longitude=$longitude, timeout=$timeout
echo 'You can start api with command: docker run -p 80:5000/tcp wpapi'
echo 'API is available in http://<your server ip>/weather/current/'
tput sgr0

read -p 'Run service now? y/n? (default y)' run_now
if [ "$run_now" = "" ]
    then
        run_now="y"
fi

if [ "$run_now" = "y" ]
    then
        docker run -p 80:5000/tcp wpapi
fi
