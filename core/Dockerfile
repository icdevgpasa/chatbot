FROM python:3.6.9

RUN mkdir /src
WORKDIR /src

COPY . /src/
# COPY actions/ \
#     data/ \
#     ./config.yml \
#     ./credentials.yml \
#     ./domain.yml \
#     ./endpoints.yml \
#     ./requirements.txt \
#     /src/

# RUN pip3 install -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN rasa train

EXPOSE 5005

CMD rasa run \
    --enable-api \
    -vv \
    --log-file out.log