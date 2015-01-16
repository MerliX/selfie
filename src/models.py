# -*- coding: utf-8 -*-

import os
from peewee import *
from settings import PHOTO_PATH, DB_PATH

db = SqliteDatabase(DB_PATH)


class Requirement(Model):
    description = TextField()
    difficulty = IntegerField()
    is_basic = BooleanField(default=True)

    class Meta:
        database = db


class User(Model):
    name = CharField(unique=True)
    access_code = CharField(unique=True)
    score = IntegerField(default=0)

    def get_random_victim(self):
        previous_partners = [
            s.partner.id 
            for s in self.tasks.select(Task.partner).join(User, on=Task.partner)
        ]
        previous_partners.append(self.id)
        return (User
            .select()
            .where(~(User.id << previous_partners))
            .order_by(fn.Random())
            .get()
        )

    @property
    def approved_selfie_ratio(self):
        approved = (self.tasks
            .where((Task.is_approved == True) & (Task.is_selfie_game == True))
            .count()
        )
        total = (self.tasks
            .where(Task.is_selfie_game == True)
            .count()
        ) or 1
        return float(approved) / total

    @property
    def current_difficulty(self):
        return (self
            .tasks
            .select(fn.Max(Task.difficulty))
            .scalar()
        )

    class Meta:
        database = db


class Task(Model):
    assignee = ForeignKeyField(User, related_name='tasks')
    partner = ForeignKeyField(User, related_name='mentions', null=True)
    is_complete = BooleanField(default=False)
    is_photo_required = BooleanField(default=True)
    is_selfie_game = BooleanField(default=True)
    is_approved = BooleanField(default=False)
    approved_time = DateTimeField(null=True)
    description = TextField()
    reward = IntegerField()
    difficulty = IntegerField()

    @property
    def photo_path(self):
        return os.path.join(PHOTO_PATH, '%s.jpg' % self.id)

    @property
    def photo_url(self):
        return '/selfies/%s.jpg' % self.id

    def delete_photo(self):
        os.remove(self.photo_path)

    class Meta:
        database = db
