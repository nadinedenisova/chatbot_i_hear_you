FROM python:3.13-bookworm

WORKDIR /opt/admin

COPY . .

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x /opt/admin/entrypoint.sh

# Команда для запуска приложения
ENTRYPOINT ["/opt/admin/entrypoint.sh"]
