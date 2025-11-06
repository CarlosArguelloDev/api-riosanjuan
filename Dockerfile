FROM python:3.13.2-alpine3.21
RUN addgroup flask && adduser -S -G flask flask
WORKDIR /app/
COPY  requirements.txt .
RUN pip install -r requirements.txt
USER flask
COPY --chown=flask . .
EXPOSE 5000
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]



