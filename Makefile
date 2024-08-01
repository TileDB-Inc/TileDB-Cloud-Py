VERSION ?= 3.18.2

dockertest-geospatial-amd64:
	docker run --platform=linux/amd64 -it -v $(shell pwd):/app -v /tmp:/tmp --entrypoint=/bin/bash tiledbenterprise/notebook-python-r-julia-tilevcf-geo:$(VERSION) -c 'cd /app && python -m pip install --editable .[dev,tests] && python -m pytest $(OPTS)'
