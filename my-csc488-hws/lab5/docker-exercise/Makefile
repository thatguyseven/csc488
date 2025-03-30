# WARNING: Do not change Name to NAME! Defaults to device name
Name ?= aan1

all: build run push

images:
	docker images | grep ${Name}

# TROUBLESHOOT: Fails because grep without a matching container returns an exit code of 1. Do not remove true conditional.
ps: 
	docker ps -a | grep ${Name} || true

 
build: 
	docker build -t ${Name}/ml_data_analysis:1.0 . 
 
run: 
	docker run --rm -v \${PWD}/data:/data ${Name}/ml_data_analysis:1.0 ml_data_analysis.py /data/Meteorite_Landings.json 
 
push: 
	docker push ${Name}/ml_data_analysis:1.0