# Lab7
Lab 7 involves database persistence using Redis. The files in 

| File | Description |
| - | - |
| redis_info.py | An import file for returning a Redis database address from the localhost. |
| app.py | A copy of app.py from Lab 6 with an added `/data` endpoint. |

## How to Run
Prerequisites:
- Docker

1. Download the latest Docker Redis image with  `docker pull redis:6`
2. Open a Redis container with the command `docker run -d -p 6379:6379 -v $pwd/data:/data:rw --name=<username>-redis redis:6 --save 1 1`
3. Run `python app.py` 
