FROM python:3.7-alpine

# ENV FLASK_ENV development
# # ENV RASA_URL 'http://bot_core_ai_service:5005'
# ENV RASA_URL 'https://hejt.ml/rasa'

WORKDIR /app 
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python3"] 
CMD ["app.py"]