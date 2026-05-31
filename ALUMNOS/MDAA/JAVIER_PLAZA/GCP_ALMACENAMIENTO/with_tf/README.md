# Complete architecture with Terraform.

For deploy all the architecture and work with it, you have to do everything step by step.

To use the this architecture you need to have [Anaconda](https://www.anaconda.com/download).

Once you have anaconda, you have to create a python environment with Anaconda. To create that run the following command in your terminal: 

````sh 
conda create --name e2e_gcp_storage python=3.11
````

Once you have the environment you have to activate it. To do it run the following command: 

````sh
conda activate e2e_gcp_storage
````

Now you have to stay in the directory `on_premise`. Once you are in that directory, run the following command: 

````sh
pip install -r requirements.txt
````

**Extra commands**

To deactivate the python environment you have to run the following command: 

````sh 
conda deactivate
````

To delete the environment, run the following command: 

````sh
conda env remove -n e2e-gcp-storage
````

##  Deploy the infrastructure (Terraform).

You have to stay into the directory `terraform/`.

Deploy the infrastructure with Terraform by following these steps:

1. Initialize Terraform.

````sh
terraform init
````

2. View the actions that Terraform is going to perform (part of Terraform best practices).

````sh
terraform plan
````

3. Apply the plan.

````sh
terraform apply
````

## Configure the infrastructure (Ansible).

To configure the infrastructure, you need a SSH key. To create it run the following command: 

````sh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
````

You have to install the PostgreSQL collection to ansible running the following command:

````sh
ansible-galaxy collection install community.postgresql
````

## Connect BigQuery to the Cloud Storage.

ow that we have the parquet file created in our bucket, we will create a external table in BigQuery to access its content. You have to run the following command:

````sh
gcloud bigquery tables create raw_additional_products_info \
  --dataset=orders_bronze \
  --external_data_configuration='format=PARQUET,autodetect=true,source_uris=gs://e2e-gcp-storage-<your project id>/raw_data/*.parquet' \
  --project=<your project id>
````

# On-Premise part.

In the On-Premise part, you have three parts, EL, DBT and the BI

## Extract-Load.

To do this part, you have to add your IP to the Cloud SQL instance. You have the instructions in [Run the Orders APP and the Delivery APP](#run-the-orders-app-and-the-delivery-app).

Now you have to deploy the EL pipeline to synchronize the Cloud SQL database with BigQuery. To do that, you have to run the following command (you have to stay in the `on_premise/` directory):

````sh
POSTGRES_IP=<The public IP of the Cloud SQL instance> GCP_PROJECT=<Your project id> POSTGRES_PASSWORD=<The password of the Cloud SQL> python -m el_orders.main
````

## DBT.

For this part you have to create the directory `gcp_storage_project/` into the directory `on_premise/dbt/`. 

Into the new directory you have to copy all the files into the directory `template` and change the file `profiles.yml` with your information. 

To use DBT you have to create a service account to bring permission to dbt. To create it you have to do the following steps:

1. Go to IAM & Admin in GCP Console. 

2. Go to Services accounts.

![Services accounts in GCP console](../.img/image41.png)

3. Click on `Create service account`.

4. Set the following configuration (you can see in the following steps): 

   - **Service account name**: `dbt-storage-project`
   - **Permissions**:
     - **Role**: `BigQuery Data Owner` and `BigQuery Job User`

![Name Service Account](../.img/image42.png)

![Role service account](../.img/image43.png)

5. Click on `Done`.

Now you have the service account. To use it you have to do the following steps:

1. Click on `Manage keys` into the service account.

![Manage keys service account](../.img/image44.png)

2. Click on `Add key`.

3. Click on `Create new key`.

4. Select `JSON` and click on create. 

Now you have a JSON in your computer. Put it in the directory `on_premise/dbt/gcp_storage_project/`.

Run the following commands to use dbt:

````sh
dbt run --select expanded_delivery_events
dbt run --select analytics
````

## Metabase (BI)

Let's now deploy Metabase to visualize the data from BigQuery.

1. Go to the directory `on_premise/bi/`

2. Deploy the docker-compose running the following command (you need to have the Docker Desktop open):

````sh
docker compose up
````

3. Go to the browser and access `http://localhost:3000` to access Metabase.