# Real-Time Clickstream Analytics Pipeline on AWS

This project simulates, ingests, transforms, and analyzes clickstream data using a fully serverless architecture on AWS. It includes real-time ingestion using Kinesis and Lambda, data transformation with AWS Glue, storage in S3, query and repair via Athena, and orchestration using AWS Step Functions.

---

## 📁 Project Structure & Files

| File/Resource | Description |
|---------------|-------------|
| `simulate_lambda.zip` | Lambda deployment package to simulate clickstream events into a Kinesis stream. Also includes `faker`|
| `lambda_function.py` | Python Lambda script to simulate one event/second for 20 seconds using `faker` and send to Kinesis. |
| `glue_etl_script.py` | AWS Glue job script to read raw JSON from S3, flatten geo fields, convert timestamps, and write to the processed zone partitioned by date. |
| `state_machine_definition.json` | Step Function JSON definition that orchestrates the pipeline. |
| `stepfunction-role` | IAM role with permissions for Lambda, Glue, Athena, Kinesis, and SNS actions. |
| `SNS topic` | Notifies success/failure of the Step Function via email. |

---

## 🧪 Pipeline Flow Overview

```
[Lambda (simulate)]
   ↓
[Kinesis Stream]
   ↓
[Lambda (transform & write to S3 bucket)]
   ↓
[Raw data stored in clickstream-raw-data-tanzini bucket]
   ↓
[Step Function → Glue ETL Job → Processed S3 bucket]
   ↓
[Athena Query: MSCK REPAIR TABLE]
   ↓
[SNS NotifySuccess or NotifyFailure]
```

---

## 🧰 AWS Services Used

- **Amazon Kinesis**: Real-time ingestion stream.
- **AWS Lambda**: 2 functions: one for simulating events, another for reading from Kinesis and writing to S3.
- **Amazon S3**: Stores raw and processed clickstream data.
- **AWS Glue**: ETL jobs for data cleaning and partitioning.
- **Amazon Athena**: Queries partitioned data and repairs metadata.
- **AWS Step Functions**: Orchestrates the entire flow.
- **Amazon SNS**: Sends notifications on pipeline success or failure.

---

## 🚀 Step-by-Step Guide to Run the Pipeline

### 1. **Create the Kinesis Stream**
- Go to **Amazon Kinesis** → Create data stream `clickstream-data`.

### 2. **Deploy Lambda for Simulation**
- Create a Lambda function.
- Upload the zipped simulator code.
- Attach an IAM role with `kinesis:PutRecord` permission.
- Add to Step Function later or run manually to simulate data.

### 3. **Create Raw S3 Bucket**
- Create a bucket: `clickstream-raw-data-tanzini`
- Grant write access to Kinesis-consuming Lambda.

### 4. **Deploy Lambda for Ingestion**
- Set up a Lambda with Kinesis as trigger.
- This Lambda writes records to the raw S3 bucket.

### 5. **Create Glue Job**
- Upload `glue_etl_script.py`.
- Use Spark, add S3 input (raw) and output (processed) paths.
- Set IAM role for Glue with S3 read/write and job execution permissions.

### 6. **Create Athena Table**
Use this sample DDL:
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS clickstream_db.raw_clickstream_raw_data_tanzini (
  user_id string,
  session_id string,
  event_time timestamp,
  event_type string,
  page_url string,
  referrer_url string,
  device_type string,
  browser string,
  ip string,
  country string,
  city string
)
PARTITIONED BY (event_date date)
STORED AS PARQUET
LOCATION 's3://clickstream-processed-data-tanzini/'
```

### 7. **Configure Step Function**
- Use the `state_machine_definition.json`.
- Link Lambda, Glue, Athena, and SNS steps.
- Attach IAM role with full permissions.

### 8. **Create SNS Topics**
- Create topics `PipelineSuccess` and `PipelineFailure`.
- Subscribe via email to receive notifications.

### 9. **Run Step Function**
- Trigger the Step Function manually.
- Lambda will simulate → data flows through Kinesis → raw S3 → Glue ETL → Athena repair → SNS success/failure.

---

## 📝 Notes

- Ensure IAM roles have policies for Kinesis, Lambda, Glue, Athena, and SNS.
- Use CloudWatch Logs for debugging if anything fails.
- Adjust simulation duration by changing the loop in `lambda_function.py`.

---

## 📌 Next Steps (Optional Improvements)
- Add monitoring/alerts using CloudWatch Alarms.
- Store Athena results in a database or visualize in QuickSight.
- Add a CDK/Terraform deployment script.

---

## 📧 Contact
Created by **Tanmay Singh** — feel free to reach out for improvements or collaboration!
