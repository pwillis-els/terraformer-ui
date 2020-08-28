
pip: venv
	./venv/bin/pip install --upgrade .

venv:
	python3 -m virtualenv -p python3 ./venv

terraform-init:
	terraform init

DOCKER_IMG      := terraformer-ui
DOCKER_IMG_TAG  := latest

docker-build:
	docker build -t $(DOCKER_IMG):$(DOCKER_IMG_TAG) .

docker-run: docker-build
	docker run --rm -it $(DOCKER_IMG):$(DOCKER_IMG_TAG)
