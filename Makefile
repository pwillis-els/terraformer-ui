
pip: venv
	./venv/bin/pip install --upgrade .

venv:
	python3 -m virtualenv -p python3 ./venv

terraform-init:
	terraform init
