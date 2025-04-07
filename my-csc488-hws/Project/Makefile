# WARNING: Do not change Name to NAME! Defaults to device name
Name ?= aan1

all: build run push
 
build: 
	docker build -t ${Name}/NASA_app:1.0 . 
 
run: 
	docker run -it --rm -v \${PWD}:/app ${Name}/NASA_app:1.0 flask run -p 5000
