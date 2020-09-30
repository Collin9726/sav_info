[![Build Status](https://travis-ci.org/Collin9726/sav_info.svg?branch=master)](https://travis-ci.org/Collin9726/sav_info) [![Coverage Status](https://coveralls.io/repos/github/Collin9726/sav_info/badge.svg)](https://coveralls.io/github/Collin9726/sav_info) [![codebeat badge](https://codebeat.co/badges/b017f4cc-4c1d-4367-868b-77931548bfb5)](https://codebeat.co/projects/github-com-collin9726-sav_info-master)

SAV_INFO
=======

## Description
A Python RESTful API handling customer and order data. It employs JWT authentication, Africa's Talking SMS Gateway, unittesting with coverage, and CI/CD through Travis CI.

---

## API Spec and Endpoints
The preferred JSON objects to be returned by the API endpoints are as in the documentation on [https://sav-info.herokuapp.com/api-docs/swagger/](https://sav-info.herokuapp.com/api-docs/swagger/).

## Technologies used

1. Python v3.6
2. DjangoREST
3. Postgres
4. Africa's Talking Sandbox API
5. Travis CI
6. Coveralls
7. Heroku

## Setup & Run instructions
- Clone the repo to your machine
- Create and activate a virtual environment
- Run `pip3 install -r requirements.txt` on your virtual environment
- Open `psql` shell and create Postgres database
- `touch .env` on your root directory and include all configs in `.env.sample` in your `.env` file
- Set `MODE='dev'` for your development environment.
- `python manage.py migrate`
- `python manage.py runserver`

### Remember to:
- Register for Sandbox credentials on [Africa's Talking](https://africastalking.com/)
- Register for [Travis CI](https://travis-ci.org/) and [Coveralls](https://coveralls.io/) accounts and credentials.

### To contribute to this project on any modules, follow these easy steps:

- Fork the repo
- Create a new branch in your terminal (git checkout -b improve-feature)
- Make appropriate changes in file(s)
- Add the changes and commit them (git commit -am "Improve App")
- Push to the branch (git push origin improve-app)
- Create a Pull request

## Support and contact details
For any queries, issues, ideas or concerns contact [Collin Owino](owino.collin@gmail.com). Your feedback is highly appreciated. 

### [License](LICENSE)
MIT license
Copyright (c) 2020 **Collin Owino**