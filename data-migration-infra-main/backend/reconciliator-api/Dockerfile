# python official
FROM python:3.9-slim

#Setting workdir
RUN pwd
WORKDIR /app

#copying in workdir dataLoader
COPY /dataLoader dataLoader/

#installing requirements
RUN pip install --no-cache-dir -r dataLoader/requirements.txt

#executing producer
CMD ["python", "dataLoader/src/reconciliator.py"]
