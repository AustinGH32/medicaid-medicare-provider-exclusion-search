# Medicaid Provider Exclusion Search

A Django web application for searching federal and state Medicaid/Medicare 
provider exclusion records across multiple data sources.

## Data Sources
- Federal OIG LEIE (List of Excluded Individuals/Entities)
- California exclusion list
- Georgia DCH exclusion list
- New York exclusion list
- North Carolina exclusion list
- North Dakota exclusion list
- Ohio exclusion list

## States/Territories Without Lists (Use Federal List)
- New Mexico
- Oklahoma
- Puerto Rico

## Tech Stack
- Python / Django
- PostgreSQL
- HTML/CSS

## Features
- Search across federal and state exclusion lists simultaneously
- Unified main exclusion table aggregating all sources
- Filter results by source
- Bulk import via CSV/Excel management commands

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/AustinGH32/medicaid-provider-exclusion-search.git
cd medicaid-provider-exclusion-search
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database
Open psql and run:
```sql
CREATE DATABASE oig_exclusions;
```

### 5. Create a .env file

Create a file called `.env` in the root of the project with the following:


SECRET_KEY=any-long-random-string-you-make-up-yourself

DB_NAME=oig_exclusions

DB_USER=postgres

DB_PASSWORD=your_postgres_password

DB_HOST=localhost

DB_PORT=5432

You can generate a secret key by running:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Import the data
Run each import command with the path to your data file:
```bash
python manage.py import_exclusions path/to/Federal_Exclusion_List.csv
python manage.py import_georgia path/to/Georgia_Exclusions_List.xlsx
python manage.py import_california path/to/California_Exclusion_List.csv
python manage.py import_new_york path/to/NYSOMIGExclusionsList.xlsx
python manage.py import_ohio path/to/Ohio_Provider_Exclusions.xlsx
python manage.py import_north_dakota path/to/ND_Provider_Exclusions.xlsx
python manage.py import_north_carolina path/to/NC_Excluded_Providers.xlsx
python manage.py import_oregon path/to/Oregon_Exclusion_List.csv
python manage.py import_pennsylvania path/to/Pennsylvania_exclusion_list.csv
python manage.py import_new_jersey path/to/NJ_Exclusion_List.csv
```

### 8. Populate the main exclusion table
```bash
python manage.py populate_main
```

### 9. Start the server
```bash
python manage.py runserver
```

### 10. Open the app
Open your browser and go to:
http://127.0.0.1:8000

You should see the search page with all records loaded.
