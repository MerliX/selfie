from src.models import db, User, Requirement, Task

db.connect()

try:
    db.drop_tables([User, Requirement, Task])
except:
    db.rollback()

db.create_tables([User, Requirement, Task])

db.close()
