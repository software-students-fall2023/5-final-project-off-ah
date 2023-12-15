
FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

ENV MONGO_URI=mongodb://localhost:27018/
ENV DB_NAME=bank
ENV KEY=secret

CMD ["python", "-m", "webapp.app"]
