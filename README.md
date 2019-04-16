# Street-Watch - ALPHA
In order to use the evaluate the code in this repo for the alpha release, please follow the following instructions
1. Clone the repo:
   - `mkdir ~/Street-Watch`
   - `git clone https://github.com/PavementPrometheus/Street-Watch.git ~/Street-Watch`
2. Follow the below sections for each portion of the release
## Web API
1. Download docker compose (desktop/toolbox)
   - Windows: https://docs.docker.com/docker-for-windows/install/
   - Mac    : https://docs.docker.com/docker-for-mac/install/
   - Linux  : https://docs.docker.com/install/linux/docker-ce/ubuntu/ 
   
2. a. Run the docker container (assuming from linux)
   - `sudo dockerd &`
   - `cd ~/Street-Watch`
   - `sudo docker-compose up --build`

2. b. Run the test docker container
   - `sudo dockerd &`
   - `cd ~/Street-Watch`
   - `sudo docker-compose -f ~/Street-Watch/docker-compose.yml -f ~/Street-Watch/docker-compose.test.yml up --build`

3. b. Test the API
   - `sudo docker exec flask python -m unittest`

## Object Detection and Database Population
1. Download yolov3.weights from google drive
   - https://drive.google.com/drive/u/1/folders/0ACU5WrVTgGFqUk9PVA/
2. Place yolov3.weights into Object_Detection
   - `cd ~/Downloads`
   - `mv yolov3.weights ~/Street-Watch/Object_Detection`
3. Follow Web API instructions above
4. While Web API service is running, run video_demo
   - `cd ~/Street-Watch/Object_Detection`
   - `video_demo.py --video JacksonWYTownSquare.avi`
5. Look in output folder to play video post obfuscation
   - `cd ~/Street-Watch/Object_Detection/output`
   - `<video player name> result_JacksonWYTownSquare.avi`
6. Run HTTP GET request for stored data from Web API
   - `curl -i -H "Accept: application/json" -H "Content-Type: application/json" http://192.168.99.100:4000/pavement`

## Troubleshooting
**Cannot access localhost:4000**  
After building the container through the ```docker-compose up --build``` command, if no url is showing to access the Web API (ex: localhost:4000):
- If using the Docker Toolbox, open the Kinematic Docker API 
- Find the Access URL on the righthand side (ex: 192.168.99.100:4000)
- Use the Acess URL within your browser to access the Web API
