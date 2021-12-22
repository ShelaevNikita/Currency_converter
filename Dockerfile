
FROM ubuntu
RUN apt-get update
RUN apt-get install -y memcached
# Port to expose (default: 11211)
EXPOSE 11211
# Default Memcached run command arguments
CMD ['-u', 'root', '-m', '128']
USER daemon
# Set the entrypoint to memcached binary
ENTRYPOINT memcached

FROM python:3.7-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.7-slim AS build-
WORKDIR currency_converter
COPY --from=compile-image /opt/venv /opt/venv
COPY currency_converter.py .

# Make sure we use the virtualenv
ENV PATH="/opt/venv/bin:$PATH"
CMD ['python3', '-u', 'currency_converter.py']

# Commands to run the image:
# sudo docker build -t <image_name> .
# sudo docker run -d -it -p 11211:11211 <image_name>