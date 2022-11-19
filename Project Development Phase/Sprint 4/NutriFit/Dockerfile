FROM debian:stable
COPY . ./app
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip build-essential libxml2
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3", "main.py"]
