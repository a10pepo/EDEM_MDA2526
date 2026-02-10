# Data Migration: Cloud SQL PostgreSQL to BigQuery via Datastream

This guide provides a concise, step-by-step process to migrate data from Cloud SQL for PostgreSQL to BigQuery using GCP Datastream with IP allowlisting for near real-time Change Data Capture (CDC) replication.

---

## Prerequisites

Before starting, ensure you have:

- ✅ A Cloud SQL for PostgreSQL instance with a **Public IP**
- ✅ **Editor** or **Owner** permissions in the GCP Project
- ✅ BigQuery dataset created in the **same region** as Datastream

---

## Step 1: Prepare Cloud SQL (PostgreSQL)

### 1.1 Configure Database Flags

1. Navigate to **Cloud SQL** > **Instances** > **Edit**
2. Add the flag: `cloudsql.logical_decoding = on`
3. Click **Save** and **Restart** the instance (required for this change)

### 1.2 Create Database User & Replication Slot

Connect to your database via **Cloud Shell** and run:

```sql
-- Create Datastream user
CREATE USER datastream_user WITH REPLICATION LOGIN PASSWORD 'your_secure_password';

-- Grant permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO datastream_user;
GRANT USAGE ON SCHEMA public TO datastream_user;

-- Create Publication (defines what to stream)
CREATE PUBLICATION ds_publication FOR ALL TABLES;

-- Create Replication Slot (keeps track of stream position)
SELECT PG_CREATE_LOGICAL_REPLICATION_SLOT('ds_slot', 'pgoutput');
```

---

## Step 2: Configure Networking (IP Allowlisting)

1. Go to **Datastream** > **Connection profiles** > **Create Profile**
2. Select **PostgreSQL**
3. Under **Connectivity Method**, select **IP Allowlisting**
4. Copy the list of **Public IP addresses** displayed for your region
5. Go to **Cloud SQL** > **Connections** > **Networking**
6. Click **Add Network** and add each Datastream IP individually
7. Click **Save**

---

## Step 3: Create Datastream Components

### 3.1 Create Source Connection Profile (PostgreSQL)

Configure the following settings:

- **Hostname**: Your Cloud SQL Public IP
- **Port**: `5432`
- **Database**: `postgres` (or your specific DB name)
- **Credentials**: `datastream_user` / `your_secure_password`
- **Encryption**: None

**Test Connection**: Ensure it passes before proceeding.

### 3.2 Create Destination Connection Profile (BigQuery)

1. Create a new profile
2. Select **BigQuery** as the destination type
3. Give it a descriptive name

### 3.3 Create and Start the Stream

1. Go to **Datastream** > **Streams** > **Create Stream**
2. **Source Config**:
   - Replication Slot: `ds_slot`
   - Publication: `ds_publication`
   - Select schemas/tables to include
3. **Destination Config**: Select your target BigQuery dataset
4. **Validate & Start**: Run the validation tool
5. If all checks are ✅ green, click **Create and Start**

---

## Appendix: CLI Quick Commands

### Whitelist IPs via gcloud

```bash
gcloud sql instances patch [INSTANCE_NAME] \
    --authorized-networks=[IP1]/32,[IP2]/32,[IP3]/32
```

### Create Source Profile via gcloud

```bash
gcloud datastream connection-profiles create pg-source-profile \
    --location=[REGION] \
    --postgresql-profile-hostname=[SQL_IP] \
    --postgresql-profile-username=datastream_user \
    --postgresql-profile-password=your_password \
    --postgresql-profile-port=5432 \
    --postgresql-profile-database=postgres \
    --static-service-ip-connectivity
```

### Create and Run Stream via gcloud

```bash
gcloud datastream streams create pg-to-bq-stream \
    --location=[REGION] \
    --source-connection-profile=pg-source-profile \
    --destination-connection-profile=bq-dest-profile \
    --display-name="PostgreSQL to BigQuery Stream" \
    --postgresql-source-config=replication-slot=ds_slot,publication=ds_publication \
    --bigquery-destination-config=dataset=[DATASET_NAME]
```

---

## Troubleshooting

### Common Issues

- **Connection Failed**: Verify IP allowlisting and firewall rules
- **Replication Slot Not Found**: Ensure the slot was created successfully
- **Permission Denied**: Check user grants and schema permissions
- **Logical Decoding Error**: Confirm the database flag is set and instance restarted

---

**📝 Note**: Keep your replication slot active or it will be dropped. Monitor Datastream for any errors or lag.
    --postgresql-source-config='{"replication_slot": "ds_slot", "publication": "ds_publication"}' \
    --bigquery-destination-config='{"dataset_config": {"single_dataset": {"dataset_id": "your_dataset"}}}' \
    --state=RUNNING
