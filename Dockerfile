FROM python:3-alpine

WORKDIR /root/
RUN mkdir -p /root/.aws \
    && echo -e "[default]\nregion = us-east-1\noutput = json" > /root/.aws/config

#
# Download dependencies
#

## Install Terraform (adds about 37MB).
## Probably not necessary if you use the AWS provider download below.
#ARG TERRAFORM_VERSION=0.12.29
#RUN wget -O /usr/local/bin/terraform.zip \
#        "https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" \
#    && unzip /usr/local/bin/terraform.zip -d /usr/local/bin \
#    && rm /usr/local/bin/terraform.zip

# Install Terraformer.
# The AWS version adds about 131MB, and the 'all' version adds 242MB.
ARG TERRAFORMER_PROVIDER=aws
ARG TERRAFORMER_VERSION=0.8.8
RUN wget -O /usr/local/bin/terraformer \
        "https://github.com/GoogleCloudPlatform/terraformer/releases/download/${TERRAFORMER_VERSION}/terraformer-${TERRAFORMER_PROVIDER}-linux-amd64" \
    && chmod 755 /usr/local/bin/terraformer


# Install the Terraform provider manually so we don't have to download Terraform
# just to download this file. The AWS provider adds about 149MB.
ARG TERRAFORM_PROVIDER=aws
ARG TERRAFORM_PROVIDER_VERSION=3.4.0
ARG TERRAFORM_PROVIDER_VERSION_FULL=3.4.0_x5
ARG TERRAFORM_PROVIDER_CHECKSUM=sha256:b8efeae190cedc2acec95c215ce7a401f841d0f3adc4e5ce59847036a801dc95
RUN mkdir -p .terraform/plugins/linux_amd64/ \
    && wget -O .terraform/plugins/linux_amd64/terraform-provider-${TERRAFORM_PROVIDER}_v${TERRAFORM_PROVIDER_VERSION_FULL} \
        "https://releases.hashicorp.com/terraform-provider-${TERRAFORM_PROVIDER}/${TERRAFORM_PROVIDER_VERSION}/terraform-provider-${TERRAFORM_PROVIDER}_${TERRAFORM_PROVIDER_VERSION}_linux_amd64.zip?checksum=${TERRAFORM_PROVIDER_CHECKSUM}" \
    && chmod 755 .terraform/plugins/linux_amd64/terraform-provider-${TERRAFORM_PROVIDER}_v${TERRAFORM_PROVIDER_VERSION_FULL}

#
# Install the app
#

COPY . /app/terraformer-ui

# Sample block if we have to compile pip dependencies in Alpine
#RUN apk add -t pip-deps --update --upgrade --no-cache \
#        gcc \
#        libffi-dev \
#        libgcrypt-dev \
#        musl-dev \
#        openssl-dev \
#    && pip install --no-cache-dir -U /app/terraformer-ui \
#    && apk del pip-deps -r --purge --no-cache \

RUN pip install --no-cache-dir -U /app/terraformer-ui

CMD ["terraformer-ui"]
