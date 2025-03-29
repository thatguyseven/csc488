NAME ?= ani

all: images ps

images: 
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}