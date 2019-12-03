FROM python:3.8.0

WORKDIR /chepy
COPY dev_requirements.txt /chepy
RUN pip install -r /chepy/dev_requirements.txt \
    && virtualenv -p python3 /chepy/venv \
    && /chepy/venv/bin/pip3 install -r dev_requirements.txt

COPY . /chepy/
RUN cd /chepy && venv/bin/pip3 install .

RUN cd /chepy/ && pytest --disable-pytest-warnings --cov=chepy --cov-config=.coveragerc tests/
RUN cd /chepy/ && bandit --recursive chepy/ --ignore-nosec --skip B101,B413,B303,B310,B112,B304,B320,B410,B404
RUN cd /chepy/ && make -C docs/ clean html


FROM python:3.8.0-slim
RUN apt update && apt install exiftool -y
COPY --from=0 /chepy /chepy
COPY --from=0 /root/.chepy /root/.chepy
WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["/chepy/venv/bin/chepy"]
