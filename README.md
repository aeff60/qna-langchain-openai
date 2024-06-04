# BorntoDev Course Q&A

This is a Flask application that uses OpenAI's GPT-3.5-turbo model to answer questions about the BorntoDev online course.

## Setup

1. Clone the repository.
2. Install python and dependencies:

```sh
pip install -r requirements.txt
```

3. Set the OPENAI_API_KEY environment variable in your .env file.

## Running the Application

You can run the application using Docker or directly from your terminal.

## Docker

Build the Docker image

```
docker build -t borntodev-qa .
```

Run the Docker container

```
docker run -p 5000:5000 borntodev-qa
```
