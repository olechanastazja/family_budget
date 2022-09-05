FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    && apt-get install -y netcat
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["sh", "entrypoint.sh"]