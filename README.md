## Setup

Assuming you have conda installed, first step is to setup a conda environment:

```bash
conda create --name <your_env_name> --file requirements.txt
```

After that, activate the environment:

```bash
conda activate <your_env_name>
```

Next, download the ClinicalTrials dataset as specified in the take home prompt. Save the file as `ctg-studies.json` in the root directory of this project.

Lastly, you need to have a PostgreSQL database running. Save the database credentials in the following environment variables:

- `DBNAME`: The name of the database (default: `argon_db`)
- `DBUSER`: The username of the database (default: `argon_user`)
- `DBPASSWORD`: The password of the database (default: `somepassword`)
- `DBHOST`: The host of the database (default: `localhost`)
- `DBPORT`: The port of the database (default: `5432`)

After setting up the environment variables, you can run the following command:

```bash
python main.py
```

## Overview

This project is a simple ETL pipeline that takes a JSON file containing clinical trial studies and inserts them into a PostgreSQL database.
I setup the project to be simple, performant, and easily to maintain and extend. I separated the application roughly into 3 layers:

- `models.py`: Contains the pydantic models for the clinical trial studies and the database models. This layer is responsible for parsing, validating and cleaning the JSON data.
- `main.py`: Contains the main ETL pipeline. This layer is responsible for orchestrating the ETL process (you'd plug something like Airflow or Prefect here).
- `dbutils`: Contains the database utils and most importantly the logic that transforms the pydantic models into database rows.


## Final Thoughts

There's still plenty of room to make this run faster. A few examples:
- Parallelize the database insertions via asyncio and connection pooling
- Increasing the batch size of the database insertions
- Leveraging SQL COPY instead of INSERT statements
- Creating indexes after the data is inserted

Whether or not to implement these is dependent on the details of the use case. I've left them out for simplicity.
