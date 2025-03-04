# my_docker_webpage
python Flask web app running on docker

## Setup virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

PDM is used for package management. 

# Deployment

## Development Environment

Set the `FLASK_APP` environment variable.
```bash
export FLASK_APP=src/my_flask_webpage/__init__.py
```


## Production Environment