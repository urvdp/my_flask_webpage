# my_docker_webpage
python Flask web app running on docker

## Setup virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note: On Windows the activate path is different:
```bash
.\.venv\Scripts\activate

# To deactivate
.\.venv\Scripts\deactivate
```

To upgrade pip:
```bash
python -m pip install --upgrade pip
```

PDM is used for package management. 
```bash
pdm install
```

Note: On windows uwsgi cannot be installed because it is a unix only package. You need to skip the installation process.


# Deployment

## Development Environment

Set the `FLASK_APP` environment variable.
```bash
export FLASK_APP=src/my_flask_webpage/__init__.py
```


## Production Environment