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

On windows in windows powershell:
```bash
$env:FLASK_APP = "src/my_flask_webpage/__init__.py"
```

## Production Environment

### Build the Docker Image
```bash
docker build -t my_flask_webpage .
```

A note to windows users: You need C++ build tools to build the image. You can download it from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
These are necessary for the `uwsgi` package. After installing the build tools, you need to run the following command:
```bash
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
```

### Run the Docker Container
```bash
docker run -d -p 3031:3031 my_flask_webpage
```

### Initialize the Database

On Windows:

```bash
docker exec -it <container_id> bash
python -m 'src.my_flask_webpage.setup.init_db'
```

On Linux:

```bash
docker exec -it <container_id> bash
python -m src.my_flask_webpage.setup.init_db
```