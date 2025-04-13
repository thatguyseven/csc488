Name ?= aan1

all: build push
 
build: 
	docker build -f ./Dockerfile -t ${Name}/quadrant-landings:latest . 
	docker build -f ./Dockerfile_test -t ${Name}/test-quadrant-landings:latest . 
 
push: 
	docker push ${Name}/quadrant-landings:latest 
	docker push ${Name}/test-quadrant-landings:latest 