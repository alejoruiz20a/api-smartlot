#!/bin/bash

echo "========================================="
echo " REQUISITOS:"
echo " - Debes tener la base de datos 'smartlot' creada en tu pgAdmin."
echo " - El script utiliza la dirección local (127.0.0.1) en el puerto 5432."
echo "========================================="

# Credentials
read -p "Ingrese el usuario de PostgreSQL: " DB_USER
read -s -p "Ingrese la contraseña de PostgreSQL: " DB_PASSWORD
echo ""

# Consts
DB_HOST="127.0.0.1"
DB_PORT="5432"
DB_NAME="smartlot"
CONFIG_PATH="app/config.py"

# Replace config.py
echo "Modificando archivo config.py..."

ESCAPED_PASSWORD=$(printf '%s\n' "$DB_PASSWORD" | sed 's/[\/&]/\\&/g')

NEW_URI="    SQLALCHEMY_DATABASE_URI = (\n        f\"postgresql://$DB_USER:$ESCAPED_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME\"\n    )"

sed -i "/SQLALCHEMY_DATABASE_URI = (/{
N
N
s|.*SQLALCHEMY_DATABASE_URI = (.*\n.*\n.*)|$NEW_URI|
}" "$CONFIG_PATH"

# Prepare venv

echo "Preparando entorno virtual..."
rm -rf venv
python -m venv venv
venv/Scripts/activate

pip install -r requirements.txt

# Deploy migrations
echo ""
echo "¿Deseas crear las tablas en la base de datos?"
echo "1. Sí"
echo "2. No"
read -p "Seleccione una opción: " OPCION_TABLAS

if [ "$OPCION_TABLAS" == "1" ]; then
    echo "Ejecutando migraciones..."
    flask db upgrade
fi

# Execute Flask in background
flask run