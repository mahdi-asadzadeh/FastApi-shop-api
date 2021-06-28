# About The Project
*Hello my friends*
This project is written with [FastAPI](https://fastapi.tiangolo.com/) framework and Rest architecture and has high performance.
[peewee-orm](http://docs.peewee-orm.com/en/latest/) and Python are used in this project.
Use redis as a shopping cart.
 

## Getting Started


#### Prerequisites
  - [Python](https://www.python.org/downloads/) is installed 


#### Run the project
1.create python virtualenv

        python3 -m venv venv

2.active python virtualenv

3.set **JWT_SECRET** and settings send email in .env file

4.install packages

        pip install -r requirements.txt

5.run project

        uvicorn main:app --reload

