from src.models import db, User, Requirement, Task

try:
    db.drop_tables([User, Requirement, Task])
except:
    pass

db.create_tables([User, Requirement, Task])

with open('fixtures/users.csv') as f:
    for line in f:
        userdata = line.split(';')
        username = userdata[0].split()
        username = '%s %s' % (username[1], username[0])
        User(name=username, access_code=userdata[3]).save()
