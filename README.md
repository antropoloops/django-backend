# Antropoloops backend

This is the _next_ antropoloops backend.

## Development Setup

The simplest way to do the setup is using docker. You'll need to have docker installed.

#### 1. Open a docker container

Open the docker container:

```bash
docker-compose --project-name django-backend_devcontainer run bash

# or

cd .devcontainer && npm run bash
```

#### 2. Install dependencies

Run inside container:

```bash
pip3 install -r requirements.txt
```

And ensure everything went well:

```bash
python -m django --version
```

#### 3. Run server

```bash
python manage.py runserver
```


## License

GPL v3