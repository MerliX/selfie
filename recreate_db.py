from src.models import db, User, Requirement, Task

try:
    db.drop_tables([User, Requirement, Task])
except:
    pass

db.create_tables([User, Requirement, Task])