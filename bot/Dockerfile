FROM python:3.11

WORKDIR /bot/

COPY ./requirements.txt /bot/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python3 run.py