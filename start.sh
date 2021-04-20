export FLASK_DEBUG=1

# Раскоментировать при использовании Docker
# docker-compose up -d

# To load env variables
export $(xargs <database.conf)
export FLASK_APP=app.py

cd app && flask run
