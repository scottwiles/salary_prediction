# What's my worth?
***Salary prediction project***

![project techonologies](./img/project-technologies.png)

[**`View live app here`**](https://swiles-salary-prediction.herokuapp.com/)

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

Here I will highlight some key insights from data analysis. For a more thorough analysis, I recommend checking out the notebook.

**Link to notebook:** [github](./notebooks/1.0-data-exploration.ipynb) | [nbviewer](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/1.0-data-exploration.ipynb)

### 3.1 Target - Salary

![salary distribution](./img/salary-distribution.jpg)

The distribution of salaries looks pretty normal, but a little right-skewed. We can also see that there are some values of 0.

Further analysis of the extreme `salary` values:
- Entries with 0 salary:
    - There were `5` total instances here, there was no obvious pattern and so these rows were marked for removal during preprocessing.
- Highly paid `JUNIOR` roles:
    - I found some jobs marked as `JUNIOR` that were among the top 0.5% of all salaries. However, these jobs had an average `yearsExperience` of `21`. It was decided that these are not outliers or data errors.

### 3.2 Key insights

**Salary vs Job Type and Industry**  

![salary vs job and industry](./img/salary-vs-jobtype-and-industry.jpg)

There are some findings from analysis that seem pretty intuitive. The above chart of `salary` vs. `jobType` and `industry` is an example. We can see that as the rank or position of a job increases (i.e. junior vs senior vs manager), the average salary also increases; and that education or service industry jobs pay less on average than finance or oil. 

**Salary vs Major**

![salary vs major](./img/salary-vs-major.jpg)

When looking at the average salary per major, we can see that just having a degree, and therefore having a major listed, is associated with a big increase in average salary. In fact the major value of `LITERATURE`, which has the lowest average salary other than `NONE`, is well above the overall median salary while having `NONE` major is well below the overall median salary.

![salary vs major distribution](./img/salary-vs-major-distribution.jpg)

It is also apparent here that the dataset contains far more examples of `degree` being `NONE`, than any of the other levels.

**Salary vs Industry and Major**

*Differences across industries*

![salary vs industry and major](./img/salary-vs-industry-and-major.jpg)

This is one outcome of the analysis that I found to be genuinely insightful and not so intuitive.

When looking at average salaries vs. industry and major we can see that:
- In the `SERVICE` industry, it pays more to have a `BUSINESS` major. 
- In the `AUTO` industry, it pays more to have an `ENGINEERING` major.
- In the `HEALTH` industry, it pays more to have `CHEMISTRY` or `BIOLOGY` majors.
- In the `WEB` industry, it pays more to have `ENGINEERING`, `MATH`, or `PHYSICS` majors.
- In the `FINANCE` and `OIL` industries, it pays more to have `BUSINESS` or `ENGINEERING` majors. 

*****

# 4. Model development

The modeling process started with a simple baseline using a couple of heuristics to make predictions without machine learning. This ended up giving a decent benchmark performance for more advanced methods to measure up against.

Moving to more advanced methods, multiple machine learning algorithms were tested and evaluated. `XGBoost` ultimately provided the best performance, and was selected to use for deployment.

## 4.1 Baseline model

**Link to notebook:** [github](./notebooks/2.0-baseline-model.ipynb) | [nbviewer](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/2.0-baseline-model.ipynb)

The baseline model uses a couple of simple rules to estimate salaries. It feels appropriate to take grouped averages of categorical variables such as `jobType` or `industry` and use these averages to make predictions on new data. Addtionally what I saw in the analysis of the numeric variables `milesFromMetropolis` and `yearsExperience` is that the averages across each value follow a gradual and predictable change. Refer to the [nbviewer link here](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/1.0-data-exploration.ipynb#Miles-from-metropolis) for an illustration. These findings gave me the inspiration to use the relative difference between the grouped averages in these values and the overall average salary. 

*Calculating the relative differnce:*
- Overall average salary in the data set is $\$116k$
- Average salary for `0` `yearsExperience` is $\$92k$
- The relative differnce is therefore: $\$92k - \$116k = -\$24k$

To illustrate this in more detail. Here is what the prediction behavior looks like for all values of `yearsExperience`.

![yearsExperience prediction impact](./img/prediction-behavior-yearsExperience.jpg)

We can see that values around `12` `yearsExperience` are close to the overall average and will not change the overall prediction by much. Values close to `0` or close to `24` will decrease or increase the predicted amount by the most, respectively.


Let's run through a full example by predicting the salary of a `MANAGER` with `0` `yearsExperience`.

*Baseline prediction steps:*
1. $\$115k$ starting point - the overall average `MANAGER` salary.
2. Add $-\$24k$ - the relative difference of `0` `yearsExperience` vs overall.
3. The final predicted salary in this case is then: $\$91k$


But which categorical variables do we use as our starting grouped average? And what about if we are using both of the numeric variables in our prediction? Do we combine both relative differences? It could be problematic to combine both of these relative differences, if they both lie on the extreme ends. For example if both numeric variables say to add $\$20k$ to the salary this means that the numeric variables could influence the overall salary by $\$40k$ or more.

These questions influenced my design of the baseline model tests. I chose to try two methods of combining the relative differences in the numeric variables: add them together, or take the mean. In this way those extreme cases might be more mitigated. And as for the categorical variables, I tested all `15` combinations.

**Baseline model test results:**


For each combo of categorical groupings I tested: only using the grouped average, using one or the other numeric variable, and using both combining them by either adding them or averaging them

![baseline test results](./img/baseline-model-variations-test.jpg)

#### The best performing baseline model scored `371.22` MSE.

**Insights from testing 75 variations**

- **Both numeric variables:**
    - Using `sum` to combine the numeric diffs gives lower MSE than using `mean` - *in every instance*
- **1 numeric variable:**
    - Using `yearsExperience` gives a lower MSE than `milesFromMetropolis` - *in every instance*
- **2 or 3 categorical variables:**
    - When `jobType` is __not__ a part of the categorical variables, the MSE is much higher than when it is included


## 4.2 Machine learning

**Link to notebook:** [github](./notebooks/3.0-ML-model-development.ipynb) | [nbviewer](https://nbviewer.org/github/scottwiles/salary_prediction/blob/main/notebooks/3.0-ML-model-development.ipynb)


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
