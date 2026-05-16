FROM spark:3.5.1-scala2.12-java17-python3-ubuntu@sha256:3517693dd4f8b0a13f65ec0c49a95c95b3cbc4379909527dcde690531a2bfd37 AS base

LABEL org.opencontainers.image.authors="proteccion"

USER root
RUN set -ex  \
    && apt-get update  \
    && apt-get install -y --no-install-recommends \
       dnsutils \
       iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
RUN mkdir -p /app/output_files \
    && mkdir -p /app/reports \
    && mkdir -p /app/logs

FROM base AS app

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt \
    && chown -R spark:spark /app

ENV PYSPARK_SUBMIT_ARGS="--master local[3] pyspark-shell"
ENV PORT 8080

#USER spark

# Run Orquestador_informes.py when the container launches
CMD ["python3", "src/ci-348-framework-generacion-de-informes/orquestador.py"]
