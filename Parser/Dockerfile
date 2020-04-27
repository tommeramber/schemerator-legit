FROM python:3

# the docker build needs to run from the home schemerator directory. i dont know how to fix it
COPY Parser/ /home/Parser/
COPY SharedUtils/ /home/SharedUtils/

WORKDIR /home/Parser/

ENV PYTHONPATH /home/

CMD ["python", "/home/Parser/app.py"]