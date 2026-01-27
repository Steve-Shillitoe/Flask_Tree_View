
"""
Application configuration module.

This module defines configuration values for the Flask application,
including database connection settings and SQLAlchemy behaviour.
"""

# SQLAlchemy database connection URI.
#
# This configuration uses:
# - Microsoft SQL Server (SQLEXPRESS)
# - Windows authentication (trusted connection)
# - pyodbc as the database driver
#
# The database name is "AnimalKingdom".
SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://@localhost\\SQLEXPRESS/AnimalKingdom"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

# Disable SQLAlchemy event system for object modification tracking.
# This reduces memory overhead and is recommended unless explicitly needed.
SQLALCHEMY_TRACK_MODIFICATIONS = False


