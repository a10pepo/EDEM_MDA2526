## DYNAMODB

aws dynamodb create-table --table-name garmin_workouts --attribute-definitions AttributeName=workout_id,AttributeType=S --key-schema AttributeName=workout_id,KeyType=HASH --billing-mode PAY_PER_REQUEST --region eu-north-1

aws dynamodb create-table --table-name garmin_sleep --attribute-definitions AttributeName=date,AttributeType=S --key-schema AttributeName=date,KeyType=HASH --billing-mode PAY_PER_REQUEST --region eu-north-1


## S3 + ATHENA

aws s3 mb s3://garmin-data-278057567356 --region eu-north-1

aws s3api put-public-access-block --bucket garmin-data-278057567356 --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

[System.IO.File]::WriteAllText("$PWD\tmp.json", '{"Name": "garmin_db"}')
aws glue create-database --database-input file://tmp.json --region eu-north-1
Remove-Item tmp.json


## VERIFICAR

aws dynamodb list-tables --region eu-north-1

aws s3 ls s3://garmin-data-278057567356

aws glue get-database --name garmin_db --region eu-north-1


## LAYOUT S3

REM s3://garmin-data-278057567356/
REM ├── workouts/          <- Parquet con todos los entrenamientos
REM ├── sleep/             <- Parquet con todas las metricas de sueno
REM └── athena-results/    <- Resultados de queries Athena (auto-generado)


## BORRAR TODO

aws glue delete-database --name garmin_db --region eu-north-1
aws s3 rm s3://garmin-data-278057567356 --recursive
aws s3 rb s3://garmin-data-278057567356
aws dynamodb delete-table --table-name garmin_workouts --region eu-north-1
aws dynamodb delete-table --table-name garmin_sleep --region eu-north-1
