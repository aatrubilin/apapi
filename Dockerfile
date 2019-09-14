
FROM python:3.7-alpine
WORKDIR /wpapi
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENV WEATHER_API_TOKEN <API TOKEN>
CMD python run.py -s OpenWeatherMapAPI -lat 55.03 -lon 82.92 -t 60.0
