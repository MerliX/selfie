import os
from collections import defaultdict
from peewee import *
from settings import PHOTO_PATH, DB_PATH

db = SqliteDatabase(DB_PATH)


class Perk(Model):
    text = TextField()
    level = IntegerField()

    @staticmethod
    def get_least_used(level):
        if level == 0:
            return (Perk
                .select(Perk, fn.Count(User.id))
                .join(User, JOIN_LEFT_OUTER)
                .where(Perk.level == 0)
                .group_by(Perk)
                .order_by(fn.Count(User.id))
                .get()
            )
        else:
            return (Perk
                .select(Perk, fn.Count(Selfie.id))
                .join(Selfie, JOIN_LEFT_OUTER)
                .where(Perk.level == level)
                .group_by(Perk)
                .order_by(fn.Count(Selfie.id))
                .get()
            )

    class Meta:
        database = db


class User(Model):
    name = CharField(unique=True)
    access_code = CharField(unique=True)
    perk = ForeignKeyField(Perk, related_name='users')

    @staticmethod
    def get_moderator_summary():
        return (User
            .select(User, fn.Max(Perk.level).alias('level'))
            .join(Selfie)
            .join(Perk)
            .group_by(User.id)
            .order_by(Perk.level.desc())
        )

    def get_ordered_selfies(self):
        selfies = defaultdict(list)
        for selfie in self.selfies.select(Selfie, Perk).join(Perk):
            selfies[selfie.perk.level].append(selfie)
        return selfies

    def get_random_victim(self):
        previous_victims = [
            s.victim.id 
            for s in self.selfies.select(Selfie.victim).join(User, on=Selfie.victim)
        ]
        return (User
            .select()
            .where(~(User.id << previous_victims))
            .order_by(fn.Random())
            .get()
        )

    @property
    def approved_ratio(self):
        approved = self.selfies.where(Selfie.is_approved == True).count()
        total = self.selfies.count() or 1
        return float(approved) / total

    @property
    def next_level(self):
        return (self
            .selfies
            .select(fn.Max(Perk.level))
            .join(Perk)
            .scalar() + 1
        )

    class Meta:
        database = db


class Selfie(Model):
    author = ForeignKeyField(User, related_name='selfies')
    victim = ForeignKeyField(User, related_name='mentions')
    is_uploaded = BooleanField(default=False)
    is_approved = BooleanField(default=False)
    approved_time = DateTimeField(null=True)
    perk = ForeignKeyField(Perk, related_name='selfies')

    @staticmethod
    def get_latest_approved(limit):
        return (Selfie
            .select()
            .where(Selfie.is_approved == True)
            .order_by(Selfie.approved_time.desc())
            .limit(limit)
        )

    @property
    def photo_path(self):
        return os.path.join(PHOTO_PATH, '%s.jpg' % self.id)

    @property
    def photo_url(self):
        return '/selfies/%s.jpg' % self.id    

    def combined_perks(self):
        perks = set()
        perks.add(self.perk.text)
        perks.add(self.author.perk.text)
        perks.add(self.victim.perk.text)
        return list(perks)

    def delete_photo(self):
        os.remove(self.photo_path)

    class Meta:
        database = db
