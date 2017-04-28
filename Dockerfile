FROM ubuntu:latest

# Update
RUN apt-get update -y
RUN apt-get install -y python3-pip python3 libssl-dev python3-setuptools dnsutils
RUN easy_install3 pip
# Bundle app source
COPY . /src/dig_restful
# Install app dependencies
RUN pip install --upgrade pip
RUN pip install pyopenssl
RUN pip install -r /src/dig_restful/requirements.txt
EXPOSE 8000
CMD ["python3", "/src/dig_restful/netstats_util.py"]
