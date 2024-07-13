# Email Messaging App With Flask, Rabbitmq and Redis

This is a simple application that sends a mail to the specified email address passed in the query parameter.
The applicaion also tags logs and displays it on an endpoint

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environmental-variables](#Environmental variables)
- [Running the Application](#running-the-application)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python.
- You have installed pip.
- You have installed RabbitMQ.
- You have installed Nginx
- You have installed Ngrok.


## Installation

- To install the required packages, use pip:
    '''bash 
    pip install -r requirements.txt

- To install and start Rabbitmq:
    '''bash
    sudo apt-get update
    sudo apt-get install rabbitmq-server@
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server

- To expose your local server to the internet using Ngrok, first download and install Ngrok from [https://ngrok.com/download](https://ngrok.com/download). 

- To install and start Nginx:
    '''bash
    sudo apt install nginx
    sudo systemctl enable nginx
    sudo systemctl start nginx



## Environmental variables
- Create a file named .env and add your variables. You can see an example at .env.example

## Running the application
- Start
- Start Ngrok with the following command:
    '''bash
    ngrok http 80

- Start the celery worker with the command: 
    '''bash
    celery -A app.celery worker --loglevel=info -E

- Start the Flask app with the command:
    '''bash
    flask --app app run 

## Enjoyyyyyy!!!!!!!