# Tagmatic Python/Flask Backend

This Flask project provides the backend Web service API for the [Tagmatic](https://github.com/ivanaszuber/tagmatic) frontend application. 

To run the `tagmatic` server locally run the following commands:

```
git clone git@github.com:ivanaszuber/tagmatic-backend.git tagmatic-backend/

cd tagmatic/backend/server

pip3 install -U -r requirements.txt  # install Python dependencies

python3 db_create.py #create the database

python3 run.py #run the server on localhost:5005
```
