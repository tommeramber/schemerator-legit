FROM python:3

COPY WebExport/ /WebExport/

WORKDIR /WebExport

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]