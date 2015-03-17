from src.models import db, User, Requirement, Task, Coupon

try:
    db.drop_tables([User, Requirement, Task, Coupon])
except:
    pass

db.create_tables([User, Requirement, Task, Coupon])