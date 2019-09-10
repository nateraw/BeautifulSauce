help:
	@cat Makefile

DOCKER_FILE=docker/Dockerfile
PYTHON_VERSION?=3.7
SRC?=$(shell 'pwd')

build:
	docker build -t beautiful-sauce --build-arg python_version=$(PYTHON_VERSION) -f $(DOCKER_FILE) .
bash: build
	docker run --rm -it -v $(SRC):/src/workspace beautiful-sauce bash