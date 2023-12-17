# Final Project
![Web App CI/CD](https://github.com/software-students-fall2023/5-final-project-off-ah/actions/workflows/python-app.yml/badge.svg)

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Team Members: 
[Lara Kim](https://github.com/larahynkim) <br> 
[Angela Tao](https://github.com/XinranTaoAngela) <br> 
[Marwan AbdElhameed](https://github.com/MarwanWalid2) <br> 
[Pavly Halim](https://github.com/pavlyhalim) <br> 

## Set Up Instructions 

### To run locally, 
Clone the repository, then in the parent directory, 

1. Ensure you have the necessary dependencies
```
cd webapp
pip install -r requirements.txt
```

2. Run the following command: 
```
python app.py
```

### To run the containerized app with Docker, open Docker Desktop, clone the repo and run: 
```
cd 5-final-project-off-ah
git pull
docker-compose down //optional just to make sure no other docker images are running
docker-compose pull 
docker-compose up -d
```

### To run tests, 
1. Ensure you've downloaded pytest
```
pip install -U pytest
```

2. Run the following command:
```
pytest 
```
3. To check for coverage, 
```
python -m pip install coverage
python -m coverage run -m pytest tests
python -m coverage report
```
![alt text](https://github.com/software-students-fall2023/5-final-project-off-ah/blob/eca4a754cf31badbe8e5eb3146e41a1ac61158c0/test.png)

### Deployed App: 
http://159.203.147.53:4000/

### Dockerhub images:
https://hub.docker.com/repository/docker/marwanwalid5/financeapp/general
 
