# Final Project
![Web App CI/CD](https://github.com/software-students-fall2023/5-final-project-off-ah/actions/workflows/python-app.yml/badge.svg)

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

# FiDi: Financial Diary, Your Personal Finance Manager 
Introducing our Personal Finance Manager, a streamlined web application designed to simplify your financial tracking and planning. This user-friendly app features three core components: a welcoming home page, a transactions log, and a comprehensive financial report page. The home page serves as your gateway to efficient finance management, offering an overview and quick access to all functionalities. Navigate into the transaction logs to meticulously record and review every financial activity, from daily expenses to significant investments. The financial report page then collates this data, presenting you with clear, insightful summaries and analyses of your financial health. Ideal for personal use, our web app functions as a financial diary, making it easier than ever to monitor and manage your money effectively. Experience a new level of control over your finances with our intuitive and straightforward personal finance manager. 

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
https://fidi.me/  (Does not work on NYU network use mobile data or another wifi)

http://159.203.147.53:4000/

### Dockerhub images:
https://hub.docker.com/repository/docker/marwanwalid5/financeapp/general
 
