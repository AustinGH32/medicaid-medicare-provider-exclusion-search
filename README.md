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
- Full-text search with GIN indexing

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

You can generate one by running:
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
python manage.py import_exclusions path/to/UPDATED.csv
python manage.py import_georgia path/to/georgia.xlsx
python manage.py import_california path/to/california.csv
python manage.py import_new_york path/to/new_york.xlsx
python manage.py import_ohio path/to/ohio.xlsx
python manage.py import_north_dakota path/to/north_dakota.xlsx
python manage.py import_north_carolina path/to/north_carolina.xlsx
python manage.py import_oregon path/to/oregon.xlsx
python manage.py import_pennsylvania path/to/pennsylvania.csv
python manage.py import_new_jersey path/to/new_jersey.pdf
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
