FROM python:3.8.0

COPY . /app/chepy/
RUN pip install /app/chepy/

WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["chepy"]
