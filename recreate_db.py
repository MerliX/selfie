# -*- coding: utf-8 -*-

from peewee import IntegrityError
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
        try:
            user.save()
        except IntegrityError:
            user.name = '%s %s %s' % (username[1], username[2], username[0])
            user.save()

        Task(
            assignee=user,
            description=u'Сделай селфи, на котором хорошо видно лицо.',
            difficulty=0
        ).save()

with open('fixtures/requirements.csv') as f:
    for line in f:
        reqdata = line.rstrip().split(';')
        Requirement(
            description=reqdata[0],
            difficulty=int(reqdata[1]),
            is_basic=reqdata[2] == '1'
        ).save()
