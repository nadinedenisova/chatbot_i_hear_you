FROM python:latest

WORKDIR /opt/api

COPY . .

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["fastapi", "run", "src/main.py", "--port", "8080", "--reload"]
