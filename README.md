# Machine Learning Service

This is a standalone project to be used with the [SWP WebAssistant](https://github.com/swp-berlin/webassistant). 

It provides a REST API to calculate embeddings for text data. The embeddings are used to compare the similarity of texts.

The service is able to process HTML, Text and PDF files.

See the [docs folder](docs/) for more information. 

## Development Setup

Create a virtual environment and install the requirements:

```bash
git module init
git submodule update
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Download the model data:

```bash
ENVIRONMENT=develop python manage.py download-data
```

To start the service run:

```bash
ENVIRONMENT=develop python manage.py runserver 127.0.0.1:8080
```


