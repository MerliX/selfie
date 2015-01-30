# -*- coding: utf-8 -*-

import os
import logging
import random
from uuid import uuid4
from itertools import chain
from peewee import SqliteDatabase, Model, TextField, IntegerField, BooleanField, CharField, fn, \
                   ForeignKeyField, DateTimeField, JOIN_LEFT_OUTER, CompositeKey
from settings import PHOTO_PATH, DB_PATH, SELFIE_REWARD

db = SqliteDatabase(DB_PATH)
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Requirement(Model):
    description = TextField()
    difficulty = IntegerField()
    is_basic = BooleanField(default=True)

    class Meta(object):
        database = db


class User(Model):
    name = CharField(unique=True)
    access_code = CharField(unique=True)
    score = IntegerField(default=0)

    @property
    def needs_more_selfie_tasks(self):
        # make first selfie before you get any new tasks
        if self.tasks.where(
                (Task.is_selfie_game == True) & (Task.is_approved == True)
                ).count() < 1:
            return False

        # you should always have 3 open tasks
        if self.tasks.where(
                (Task.is_selfie_game == True) & (Task.is_approved == False)
                ).count() < 3:
            return True

        return False

    @property
    def current_difficulty(self):
        return (self
            .tasks
            .select(fn.Max(Task.difficulty))
            .where(Task.is_selfie_game == True)
            .scalar()
        )

    @property
    def photo_url(self):
        try:
            first_selfie = self.tasks.where(
                (Task.is_selfie_game == True)
                & (Task.partner >> None)
                & (Task.is_complete == True)
            ).get()
        except Task.DoesNotExist:
            return '/selfies/unknown.jpg'
        return first_selfie.photo_url    

    def has_active_store_item(self, item):
        return bool(self
            .bought_items
            .where(
                (BoughtStoreItem.item == item)
                & (BoughtStoreItem.is_delivered == False)
            )
            .count()
        )

    def generate_access_code(self):
        self.access_code = ''.join(
            chain(*zip(
                random.sample('bcdfghjklmnpqrstvwxz', 3),
                random.sample('aeiouy', 3)
            ))
        )

    class Meta(object):
        database = db


class Task(Model):
    assignee = ForeignKeyField(User, related_name='tasks', on_delete='CASCADE')
    partner = ForeignKeyField(User, related_name='mentions', null=True, on_delete='CASCADE')
    is_complete = BooleanField(default=False)
    is_photo_required = BooleanField(default=True)
    is_selfie_game = BooleanField(default=True)
    is_approved = BooleanField(default=False)
    is_rejected = BooleanField(default=False)
    approved_time = DateTimeField(null=True)
    description = TextField(null=True)
    reward = IntegerField(default=SELFIE_REWARD)
    difficulty = IntegerField()
    basic_requirement = ForeignKeyField(Requirement, null=True, on_delete='SET NULL')

    @property
    def photo_path(self):
        return os.path.join(PHOTO_PATH, '%s.jpg' % self.id)

    @property
    def photo_url(self):
        return '/selfies/%s.jpg' % self.id

    def find_partner(self):
        try:
            self.partner = (User
                .select(User.id)
                .join(Task, JOIN_LEFT_OUTER, Task.partner)
                .where(
                    ~(User.id << self.assignee
                                     .tasks
                                     .select(Task.partner)
                                     .where(
                                        ~(Task.partner >> None) 
                                        & (Task.is_selfie_game == True)
                                     )
                    )
                    & (User.id != self.assignee.id)
                )
                .group_by(User.id)
                .order_by(fn.Count(Task.id), fn.Random())
                .get()
            )
        except User.DoesNotExist:
            pass

    def generate_description(self):
        difficulty_left = self.difficulty
        basic_requirement = None
        used_requirements = []
        exclude_requirements = [
            r.basic_requirement 
            for r in self.assignee.tasks.where(~(Task.basic_requirement >> None))
        ] + [
            r.basic_requirement
            for r in self.assignee.mentions.where(~(Task.basic_requirement >> None))
        ]

        try:
            while difficulty_left > 0:
                requirement = (Requirement
                    .select()
                    .where(
                        (Requirement.is_basic == (basic_requirement is None))
                        & (Requirement.difficulty <= difficulty_left)
                        & ~(Requirement.id << exclude_requirements)
                        & ~(Requirement.id << used_requirements)
                    )
                    .order_by(fn.Random())
                    .get()
                )

                difficulty_left -= requirement.difficulty
                used_requirements.append(requirement)
                if basic_requirement is None:
                    basic_requirement = requirement
        except Requirement.DoesNotExist:
            pass

        if used_requirements:
            self.description = ' '.join([r.description for r in used_requirements])
            self.basic_requirement = basic_requirement


    def delete_photo(self):
        os.remove(self.photo_path)

    class Meta(object):
        database = db


class Coupon(Model):
    activated_by = ForeignKeyField(User, related_name='coupons', null=True, on_delete='SET NULL')
    reward = IntegerField()
    code = CharField(unique=True)
    description = TextField()
    limit = IntegerField()
    kind = CharField()
    activated_time = DateTimeField(null=True)

    def generate_code(self):
        self.code = ''.join(
            chain(*(
                zip(
                    random.sample('bcdfghjklmnpqrstvwxz', 3),
                    random.sample('aeiouy', 3)
                ) 
                + random.sample('1234567890', 2)
            ))
        )

    @staticmethod
    def generate_kind():
        return uuid4().hex

    class Meta(object):
        database = db


class StoreItem(Model):
    description = TextField()
    price = IntegerField()

    class Meta(object):
        database = db


class BoughtStoreItem(Model):
    user = ForeignKeyField(User, related_name='bought_items', on_delete='CASCADE')
    item = ForeignKeyField(StoreItem, related_name='bought_users', on_delete='CASCADE')
    is_delivered = BooleanField(default=False)

    class Meta(object):
        database = db
        primary_key = CompositeKey('user', 'item')