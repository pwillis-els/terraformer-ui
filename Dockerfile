FROM python:3-alpine

COPY . /app/terraformer-ui

# Only if we have to compile dependencies in Alpine
#RUN apk add -t pip-deps --update --upgrade --no-cache \
#        gcc \
#        libffi-dev \
#        libgcrypt-dev \
#        musl-dev \
#        openssl-dev \
#    && pip install --no-cache-dir -U /app/terraformer-ui \
#    && apk del pip-deps -r --purge --no-cache \

RUN pip install --no-cache-dir -U /app/terraformer-ui \
    && mkdir -p /root/.aws \
    && echo -e "[default]\nregion = us-east-1\noutput = json" > /root/.aws/config

CMD ["terraformer-ui"]
