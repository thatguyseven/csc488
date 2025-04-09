# WARNING: Do not change Name to NAME! Defaults to device name
Name ?= aan1

all: build run push
 
build: 
	docker build -t ${Name}/iss-info-api:1.0 . 
 
run: 
	docker run --name nasa-api -p 5000:5000 ${Name}/iss-info-api:1.0 
push: 
	docker push ${Name}/iss-info-api:1.0