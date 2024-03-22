FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn","api:app","--host","127.0.0.1","--port","8001"]