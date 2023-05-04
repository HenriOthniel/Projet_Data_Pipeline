# TP - Final - Data Pipelines

### ⚙ Requirements

- The AWS account provided by your teacher
- The AWS CLI tool: [https://aws.amazon.com/cli](https://aws.amazon.com/cli)
- When logged in your AWS account, be sure to switch the language to English with bottom left language link

 

> ⚠️ All the actions you will execute on your account will be billed to your teacher account so follow carefully the instructions to not occur unexpected costs (all the actions of your account are monitored and traceable by your teacher) ⚠️
> 



## 🥅  Goal

We are simulating a scenario, where our customer is the owner of customer support center and want a way to rank the most active clients by the number of message received from them.

During this exercise, we will have to create 4 iterations of the same data pipeline from a pipeline that is manual and simple to an automated one deployed partially in the cloud.

## 🎯 First Iteration

![First Pipeline](./docs/first-pipeline.svg)

The components of this data pipeline iteration are:

- 2 CSV files `messages.csv` and `users.csv` (you can find samples in the `/samples` folder)
- A Python script `aggregate_data.py`:
    - This script handles 3 mandatory arguments:
        - `messages_path`: path to messages data file
        - `users_path`: path to user data file
        - `output_path`:  path to output the result of the script
    - This script must group messages by `user_id` and rank them by messages received in ascending order and produce a new CSV file called `pipeline_result.csv` at the path specified by the `output_path` argument
    - The script must manage errors and exit the program if anything bad happens with an explanatory output
- A Python script `feed_database.py`:
    - This script handles 3 mandatory arguments:
        - database_uri
    - stores `pipeline_result.csv` data into a SQL database in table called `leaderboard`
    - this script must SQLAlchemy to design the table and interact with the database
    - a migration script must be available to setup the database by using Alembic

This data pipeline is pretty manual and will require the user to launch the 2 python scripts on the CSV files to execute it.

### **Bonus**

Create a Streamlit application in a [web-app.py](http://web-app.py) file that will have 2 tabs named:

- `Upload`: the user can upload the `messages.csv` and `users.csv` and the app will save them in a `/samples` directory
- Leaderboard: the user can view the `results.csv` as table

## 🎯 Second iteration


![Second Pipeline](./docs/second-pipeline.svg)


For this iteration, everything stays the same as the first iteration, except for `feed_database.py` that becomes a Flask API in a file called `api.py`

This API will have two endpoints:

- `POST /feed`:
    - this endpoint must accept a JSON payload with a field called `data_path` that is a valid path to the `pipeline_result.csv` generated by the `aggregate_data.py` script
    - this endpoint will open the CSV file and store the data in the previous following the same behavior as the `feed_database.py` script
- `GET /leaderboard`:
    - this endpoint must query the leaderboard table of the database and return the results in a JSON response following this format:
    
    ```json
    {
      "leaderboard": [
    	{
    		"user_id": 1,
    		"messages": 20,
    		"name": "Andre"
    	}, 
    	...
    }
    ```
    

Also to make the setup of pipeline easier, specify a Docker command to create container for our database with any SQL technology you choose fit with a docker volume to persist the data.

- The docker command (update the command below):

```json
docker run --name leaderboard-db -p 5432:5432 -e POSTGRES_PASSWORD=wizkevin -d postgres
```

Our users can now interact with our application through an API instead of using SQL queries but we want to be able to interact with remote data so we are going to store all our CSVs in the cloud with AWS S3.

### **Bonus**

Update the Leaderboard tab of your Streamlit application to call the new `GET /leaderboard` endpoint to display the results of your data pipeline instead of reading the `results.csv` file

## 🎯 Third data pipeline

![First Pipeline](./docs/third-pipeline.svg)

For this iteration, we keep the same behavior as before except that we will store our CSVs in 2 S3 buckets and we will update the `aggregate_bucket_data.py` script and our API to interact with the buckets.

Here are the different components:

- A new S3 bucket called `{unique_name}-raw-data-bucket-md4-api` that will store the `messages.csv` and the `users.csv` as 2 objects at the root of the bucket
- A new S3 bucket called `{unique_name}-result-data-bucket-md4-api` that will store the `pipeline_result.csv` file
- The script `aggregate_bucket_data.py`:
    - must be updated to use gather the data from the `{unique_name}-raw-data-bucket-md4-api` with the boto3 package and a IAM user that has enough permissions to read the bucket
    - must be updated to store the result of the aggregation in `{unique_name}-result-data-bucket-md4-api` in `pipeline_result.csv` object (replance it if it is already present in the bucket) with the boto3 package and a IAM user that has enough permissions to read/write on the bucket
- For the API `api.py:`
    - A new endpoint `POST /feed/s3` must be implemented:
        - this endpoint must accept a JSON payload with a field called `s3_bucket` that is a valid S3 bucket name
        - It will need to fetch the `s3_bucket` and check if a `pipeline_result.csv` object is present at the root and apply the same logic as the existing `POST /feed` to store the data in our database

To continue to improve the project setup, your will create a `Dockerfile` for the API so that we can easily launch it. 
Specify below these commands:

- The docker build command to build an image called `pipeline-flask-api` from the `Dockerfile`:
```
docker build -t pipeline-flask-api .
```
- The docker run command to create a container from the `pipeline-flask-api` image, that map your local post 3000 to the port 3000 of the container

```
docker run --name pipeline_container -p 3000:3000 -d pipeline-flask-api
```

### **Bonus**

- Update the Upload tab of your Streamlit application to upload data directly to your `{unique_name}-raw-data-bucket-md4-api` in the right objects
- Add a new tab called `Datamart` where the user can view the CSV files in your `{unique_name}-raw-data-bucket-md4-api` as 2 tables called `Messages` and `Users`

## 🎯 Fourth data pipeline

![Fourth Pipeline](./docs/fourth-pipeline.svg)

For this last iteration, we want to automate the first part of our data pipeline in the Cloud with AWS Lambda.

You must complete these steps:

- Create a Lambda called `aggregate-lambda-md4-api` in the `eu-west-3` region
- Attach the Lambda to a S3 trigger listening the S3 bucket `{unique_name}-raw-data-bucket-md4-api`
- Update the lambda execution IAM Role permissions to have a policy allowing your Lambda to read/write to the `{unique_name}-result-data-bucket-md4-api` bucket
- Upload the code  `aggregate_bucket_data.py` script to the Lambda
- Test and validate your Lambda behavior by updating the `messages.csv` or the `users.csv` file in the `{unique_name}-raw-data-bucket-md4-api` with new data and check that the `pipeline_result.csv` file is updated accordingly in the `{unique_name}-result-data-bucket-md4-api`

## ⚙️ Delivery

- Create your own Github repository and invite  `@AJRdev` as a maintainer
- Keep your Github repository code clean, I don’t want to see any unnecessary files (.pycache…) or draft files in your repository.
- Document your code as much as possible and fill information in the `Documentation` section below if you feel the need ⬇️

---

## 📖 Documentation



---

## 🌻 Resources

- Different concepts learned through the module: [https://ajrdev.notion.site/MD4-API-Docker-Cloud-2023-3b2becb7c6d54cada22a016f7f8ed84f](https://www.notion.so/MD4-API-Docker-Cloud-2023-3b2becb7c6d54cada22a016f7f8ed84f)
- Understand how to use boto3 with S3: [https://realpython.com/python-boto3-aws-s3/](https://realpython.com/python-boto3-aws-s3/)
- A exhaustive list of IAM permissions for all AWS services: [https://iam.cloudonaut.io/](https://iam.cloudonaut.io/)