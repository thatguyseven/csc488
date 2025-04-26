Name ?= aan1

all: build run push
 
build: 
	docker build -f ./Dockerfile -t ${Name}/hw6-app:latest . 
run: 
	docker run -d -p 6379:6379 -v ${pwd}:/data --name=hw6-data redis:6 --save 1 1.
	docker run --rm -p 5000:5000 ${Name}/hw6-app:latest
push: 
	docker push ${Name}/hw6-app:latest 

# deploy