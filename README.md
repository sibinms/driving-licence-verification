# Driving Licence verification using ID Analyzer 

- Refer ID Analyzer core API here : https://developer.idanalyzer.com/coreapi_reference.html


# Why combined verification of driving license and user profile verification import ?

- To verify the identify the user who is renting/leasing a vehicle
- To check the authenticity of the documents supplied
- To avoid uploading someone else document for getting authorised access

# Where this is useful ?

- This is useful in any industry where we are using driving licence as a verification document 


# How this works ?
![driving drawio](https://user-images.githubusercontent.com/32489487/195359772-6769adf8-984e-4f91-9a05-f3b00461301b.png)






> Project Setup

- In order to work with the project you need the following environment variables
  - ID_ANALYZER_API_URL --> Can be obtained from the ID Analyzer portal
  - ID_ANALYZER_API_KEY --> Can be obtained from the ID Analyzer portal
  - POSTGRES_ENGINE
  - POSTGRES_DATABASE
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_HOST
  - POSTGRES_PORT


- How to run this project ?
  - Clone the repository using git clone
  - Make sure that you have Docker installed in your computer
  - Get into the project directory
  - docker-compose up 

- If you see this error message `psycopg2.OperationalError: FATAL:  database "db" does not exist`
  - docker-compose exec <db> psql -U postgres
  - CREATE DATABASE <database_name> ;


# API Documentation

> Refer here : https://documenter.getpostman.com/view/17843916/2s83zmM3Bh
