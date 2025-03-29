NAME ?= ani

all: images ps

target: prerequisite(s)
	recipe

images: 
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}
