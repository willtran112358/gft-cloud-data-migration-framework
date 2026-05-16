# python official
FROM python:3.9-slim

# setting workdir
RUN pwd
WORKDIR /app

# for cache
COPY backend/dataLoader/requirements.txt dataLoader/

# installing requirements
RUN pip install --no-cache-dir -r dataLoader/requirements.txt

# copying in workdir dataLoader
COPY backend/dataLoader dataLoader/

# executing producer
CMD ["python", "dataLoader/src/account_producer.py"]
