# config.py
SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://@localhost\\SQLEXPRESS/AnimalKingdom"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

