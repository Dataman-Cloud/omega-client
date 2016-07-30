FROM index.shurenyun.com/zqdou/python:3.4

MAINTAINER Zheng Liu zliu@dataman-inc.com

RUN mkdir /code
ADD . /code/

RUN pip3 install -r /code/python-omegaclient/requirements.txt

WORKDIR /code/python-omegaclient

RUN python setup.py install

ENTRYPOINT ["python3", "sryapi_cli.py", "-v"]
