FROM python:3.13-bookworm

WORKDIR /opt/bot

COPY . .

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]
