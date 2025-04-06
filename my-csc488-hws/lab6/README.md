# Lab 6

This lab revolves around running Flask servers and the role Docker plays in deploying Flask apps. There are two apps available in this lab: `meteor-data` and `greet`.

| App | Description |
| - | - |
| `meteor-data` | Located in the `flask` folder. Returns a pregenerated JSON file. | 
| `greet` | Located in `web` folder. Returns a greeting. |

## Initial Setup
To run the files, follow the instructions below.

Prerequisites:
- Docker
  Download Docker using this [link](https://docs.docker.com/desktop/). Select your operating system and download the respective distribution.

Steps to run the apps:
1. Navigate to a directory containing app files.
2. Download either the web or flask folder.
3. Build the files docker `build -t aani/app .`
4. Run the image with `docker run --name "give-your-container-a-name" -d -p <your port number>:5000 
aani/app:1.0`

The Flask server should be up at this point! Open up a browser and search `http://localhost:5000/` to verify the server is up.

## Endpoints

Endpoints for `meteor-data`:
| Endpoint | Description |
| - | - |
| `/` | Returns the greeting "Hello, Flask!" | 
| `/Meteorite_Landings.json` | Returns the contents of the `Meteorite_Landings.json` file. | 

Endpoints for `greet`:
| Endpoint | Description |
| - | - |
| `/` | Returns the greeting "Hello, World!" | 
| `/<name>` | Accepts a name parameter and returns a greeting to the name sent. | 

