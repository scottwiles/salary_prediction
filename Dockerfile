# python version used during development
FROM python:3.7.6

WORKDIR /usr/salary_prediction

# Install requirements before copying files, so it's in an earlier image layer
COPY deployment_requirements.txt ./
RUN pip install --no-cache-dir -r deployment_requirements.txt

# Copy app files
COPY ./api/ ./api/
COPY ./front-end/build/ ./front-end/build/
COPY ./models/salary_prediction_xgboost_v1.pkl ./models/

# set workdir that the flask app is expecting
WORKDIR /usr/salary_prediction/api

EXPOSE 5000

CMD ["python", "./app.py"]