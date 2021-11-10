# What's my worth?
***Salary prediction project***

![project techonologies](./img/project-technologies.png)


# Contents
* [1. Why estimate salaries?](#1-why-estimate-salaries)
* [2. Data](#2-data)  
* [3. EDA](#3-eda)
* [4. Model development](#4-model-development)
    * [4.1  Baseline](#41-baseline-model)
    * [4.2 Machine learning](#42-machine-learning)
* [5. Deployment](#5-deployment)
    * [5.1 React front-end](#51-react-front-end)
    * [5.2 Flask API](#52-flask-api)
* [6. Conclusion](#6-conclusion)

---


# 1. Why estimate salaries?

Many job seekers utilize websites such as LinkedIn or Indeed when searching for new opportunities. But the majority of jobs posted do not include salary information. **This makes it difficult to decide whether a job is worth applying to or where to expect salary negotiations to start, especially when looking for jobs in different cities.**

For example, consider evaluating two different jobs. One job is in the middle of a big city, the other in a smaller rural town. You could readily compare the cost of living between the two locations on websites like [bestplaces.net](https://www.bestplaces.net/cost-of-living/). But without having an estimated salary, it is harder to determine what kind of lifestyle you could have in either location. A job that even has a high-end salary would probably not feel as sufficient in Silicon Valley versus Cincinnati, OH.

This project aims to solve this problem by creating a predictive model to estimate salaries given a set of features that describe a job. The steps of the process are outlined below.


# 2. Data

The dataset contains information from 1 million job listings.

Features:
- `jobId`: (primary key) - Unique identifier for each job.
- `companyId`: Company identifier for each job.
- `jobType`: Describes the senority or rank of the job. (i.e. Junior, Senior, Manager, CEO).
- `degree`: Highest degree obtained. (i.e. None, Bachelors, Doctoral).
- `major`: Specific field of study in school. (i.e. Engineering, Business).
- `industry`: Which industry the job is a part of. (i.e. Finance, Service).
- `yearsExperience`: Years of experience, ranging from 0-24.
- `milesFromMetropolis`: Distance from city center, ranging from 0-99.
- `salary`: (target) - Listed in 1000s of dollars, as the unit of measurement.

#### Features not used for modeling:

- `jobId`: This is a unique identifier for each job, and won't provide much value.
- `companyId`: If the goal of this model was to predict salaries for only a certain set of companies, then this feature would be useful. However, we aim to predict salaries for any given company. So we will not use this feature here.


# 3. EDA

Link to notebook: [github](./notebooks/1.0-data-exploration.ipynb) | [nbviewer](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/1.0-data-exploration.ipynb)

### 3.1 Target - Salary

![salary distribution](./img/salary-distribution.jpg)

The distribution of salaries looks pretty normal, but a little right-skewed. We can also see that there are some values of 0.


# 4. Model development

## 4.1 Baseline model

Link to notebook: [github](./notebooks/2.0-baseline-model.ipynb) | [nbviewer](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/2.0-baseline-model.ipynb)

## 4.2 Machine learning

Link to notebook: [github](./notebooks/3.0-ML-model-development.ipynb) | [nbviewer](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/3.0-ML-model-development.ipynb)


# 5. Deployment

The web app is deployed on Heroku linked here: **[`Live app`](https://swiles-salary-prediction.herokuapp.com/)**

This project makes use of Docker, for easy deployment into a cloud environment.

- [View Dockerfile](./Dockerfile)

Once the API and front-end are ready for deployment, the docker image can be built and/or the image can be pushed to Heroku.
- [Deployment details](./references/deployment.md)


## 5.1 React front-end

The main UI framework was created using the MUI React library: [check it out @ mui.com](https://mui.com/)

[![](./img/ui-screenshot.jpg)](https://swiles-salary-prediction.herokuapp.com/)

## 5.2 Flask API

---

# 6. Conclusion
