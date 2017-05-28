
**If virtualenv already not installed install it**   
$ pip install virtualenv

** create new virtual env**   
$ mkdir ~/env  
$ virtualenv ~/env/chat  
$ source ~/env/chat/bin/activate   

**Install dependency**  
$ pip install -r requirements.txt


**To create database run this in your enviorment**  
$ python -c "from app import db; db.create_all()"

**To run chat**   
$ python app.py
