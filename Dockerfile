FROM python:3.8.5

ENV HOME /code
WORKDIR $HOME
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["sh", "entrypoint.sh"]
