# -*- coding: utf-8 -*-

from src.models import db, User, Requirement, Task

try:
    db.drop_tables([User, Requirement, Task])
except:
    pass

db.create_tables([User, Requirement, Task])

with open('fixtures/users.csv') as f:
    for line in f:
        userdata = line.rstrip().split(';')
        username = userdata[0].split()
        username = '%s %s' % (username[1], username[0])

        user = User(name=username, access_code=userdata[3])
        user.save()

        Task(
            assignee=user,
            description=u'Сделай селфи, на котором хорошо видно лицо.',
            difficulty=0
        ).save()
