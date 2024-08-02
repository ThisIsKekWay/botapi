FROM python:3.9-slim

RUN mkdir /bot

WORKDIR /bot

COPY reqs.txt .

RUN pip install -r reqs.txt

COPY . .

CMD ["/bin/bash", "-c", "python main.py"]