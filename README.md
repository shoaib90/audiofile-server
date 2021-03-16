"# audiofile-server" 

> Audio Server API using Python Flask, SQL Alchemy and Marshmallow

#After Cloning the repo to your computer

# Quick Start
## Activate the env
> On windows :-  . env/Scripts/activate.bat

# Install Dependencies
pip install

# Create DB
$ python
from app import db
db.create_all()
exit()

# Run Server (http://localhost:5000)
python app.py

## Endpoints

* GET     /audio/:audioFileType
* GET     /audio/:audioFileType/:audioFileID
* POST    /audio/create
* PUT     /audio/:audioFileType/:audioFileID
* DELETE  /product/:audioFileType/:audioFileID
