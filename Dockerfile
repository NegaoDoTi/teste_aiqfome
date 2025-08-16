FROM python:3.12
WORKDIR /api
RUN apt-get update && apt-get install -y netcat*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]