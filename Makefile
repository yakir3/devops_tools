PROJECT?=yakir
NAME=${PROJECT}/devops_tools

VERSION?=v1.0
GIT_COMMIT:=$(shell git rev-parse --short HEAD)


.PHONY: clean build all test

all: build docker-image clean

test:
	echo ${GIT_COMMIT}

clean:
	docker image prune -f

build: *.py
	@#echo no need to build

docker-image: docker-build docker-push

.ONESHELL: docker-image docker-tag docker-push docker-run
docker-build:
	docker build -t ${NAME}-${GIT_COMMIT}:${VERSION} -f APP-META/Dockerfile .

docker-tag:
	@docker tag ${NAME}:${VERSION} ${DOCKER_REGISTRY}${PUSH_NAME}:${VERSION}

docker-push:
	docker push ${NAME}-${GIT_COMMIT}:${VERSION}