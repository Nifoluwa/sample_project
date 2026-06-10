## SAMPLE DATA APPLICATION

### TOOLS:
* Python >= 3.10
* PostgeSQL
* Pandas
* Plotly
* Streamlit


### ENVIRONMENT AND  DEPENDENCIES
    ## Virtual environments
    source venv/bin/activate(Linux/Mac)
    python -m venv venv(Windows)
    
    ## Relevant Packages
    pip install -r requirements.txt
    
    ## Environment Variables
    Create a .env file and fill with the following:
    DB_HOST=...
    DB_PORT=...
    DB_NAME=...
    DB_USER=...
    DB_PASSWORD=...

    # .streamlit
    In the secrets.toml file, fill with Database URL to
    connect application to database

### NOTES:

    [This project runs with a local PostgreSQL database.
    PostgreSQL is available for download and setup here:]
    (https://www.postgresql.org/). SQL can also be used,
    though requirements differ slightly.

    * For MySQL, see load.py file to select relevant URL
      setup.


### STRUCTURE

    ├── app_entry.py
    ├── .streamlit
        ├── config.toml
    │   └── secrets.toml
    ├── datasets
        └── transaction_data.csv
    ├── etl_pipeline
        ├── extract.py
        ├── load.py
    │   └── transform.py
    ├── help.py
    ├── main_page.py
    ├── main.py
    ├── page_2.py
    ├── README.md
    └── requirements.txt

### RUNNING THE APPLICATION
    To carry out ETL process:
    main.py

    Only after executing the above, to run the application,in terminal run:
    DB_CONN=local streamlit run app_entry.py


    

    