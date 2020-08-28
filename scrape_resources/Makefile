parse_aws_yaml:
	python3 -c 'import sys,yaml; y=yaml.load(sys.stdin); print(y)' < aws_resources.yaml

aws_resources_yaml:
	./convert_txt_to_yaml.sh aws_resources.txt aws > aws_resources.yaml

aws_regions:
	aws --region us-east-1 ec2 describe-regions --all-regions | jq -r .Regions[].RegionName | sort > aws_regions.txt
