# -*- coding: utf-8 -*-

import os
from datetime import datetime
from PIL import Image
from bottle import get, post, run, view, response, redirect, request, hook
from models import User, Task, Requirement, Coupon, StoreItem, BoughtStoreItem, db
from settings import HOST, PORT, DEBUG

MODERATOR_ACCESS_CODE = os.environ['SELFIE_MODERATOR_CODE']


@hook('before_request')
def _connect_db():
    db.connect()
    db.execute_sql('PRAGMA foreign_keys=1')


@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()


@get('/')
def main():
    access_code = request.get_cookie('access_code')
    
    if access_code is None:
        return login()
    if access_code == MODERATOR_ACCESS_CODE:
        redirect('/moderator/feed')
    
    try:
        User.get(User.access_code == access_code)
    except User.DoesNotExist:
        return login(True)
    else:
        redirect('/user/feed')


# moderator actions

def check_moderator(func):
    def wrapper():
        if request.get_cookie('access_code') != MODERATOR_ACCESS_CODE:
            redirect('/')
        else:
            return func()
    return wrapper


@get('/moderator/feed')
@view('moderator_feed')
@check_moderator
def moderator_feed():
    try:
        task = Task.get(Task.is_complete == True, Task.is_approved == False)
    except Task.DoesNotExist:
        task = None

    return {
        'task': task
    }


@post('/moderator/approve_task')
@check_moderator
def do_approve_task():
    try:
        task = Task.get(
            Task.id == request.forms.get('task_id'),
            Task.is_complete == True,
            Task.is_approved == False
        )
    except Task.DoesNotExist:
        pass
    else:
        if request.forms.get('decision') == 'approve':
            task.is_approved = True
            task.is_rejected = False
            task.approved_time = datetime.utcnow()
            task.save()
            User.update(score=User.score + task.reward).where(User.id == task.assignee).execute()
            if task.partner:
                (User
                    .update(score=User.score + task.reward / 2)
                    .where(User.id == task.partner)
                    .execute()
                )
        elif request.forms.get('decision') == 'reject':
            if task.is_photo_required:
                task.delete_photo()
            task.is_complete = False
            task.is_rejected = True
            task.save()
    redirect('/')


@get('/moderator/users')
@view('moderator_users')
@check_moderator
def moderator_users():
    return {
        'created_name': request.query.created_name,
        'created_access_code': request.query.created_access_code,
        'users': User.select().order_by(User.score.desc())
    }


@post('/moderator/add_user')
@check_moderator
def do_add_user():
    user_name = request.forms.get('add_user_name')
    if user_name:
        try:
            user = User.get(User.name == user_name)
        except User.DoesNotExist:
            user = User(
                name=user_name
            )
            user.generate_access_code()
            user.save()
            task = Task(
                assignee=user,
                description=u'Сделай селфи с любимым предметом, чтобы хорошо было видно лицо.',
                difficulty=0
            )
            task.save()
        redirect(
            '/moderator/users?created_name=%s&created_access_code=%s' % 
            (user_name.decode('utf-8'), user.access_code)
        )
    else:
        redirect('/moderator/users')


@get('/moderator/requirements')
@view('moderator_requirements')
@check_moderator
def moderator_requirements():
    return {
        'created_requirement': request.query.created_requirement,
        'created_difficulty': request.query.created_difficulty,
        'created_is_basic': request.query.created_is_basic,
        'requirements': Requirement
                        .select()
                        .order_by(Requirement.is_basic.desc(), Requirement.difficulty)
    }


@post('/moderator/add_requirement')
@check_moderator
def do_add_requirement():
    requirement_description = request.forms.get('add_requirement_description')
    requirement_difficulty = request.forms.get('add_requirement_difficulty')
    requirement_is_basic = bool(request.forms.get('add_requirement_is_basic'))
    if requirement_description and requirement_difficulty:
        Requirement(
            description=requirement_description, 
            difficulty=requirement_difficulty,
            is_basic=requirement_is_basic
        ).save()
        redirect('/moderator/requirements?created_requirement=%s&created_difficulty=%s&created_is_basic=%s' % (
            requirement_description.decode('utf-8'), 
            requirement_difficulty,
            requirement_is_basic
        ))
    else:
        redirect('/moderator/requirements')


@post('/moderator/edit_requirement')
@check_moderator
def do_edit_requirement():
    try:
        requirement = Requirement.get(Requirement.id == request.forms.get('edit_requirement_id'))
    except Requirement.DoesNotExist:
        pass
    else:
        if request.forms.get('action') == 'delete':
            requirement.delete_instance()
        elif request.forms.get('action') == 'save':
            requirement_description = request.forms.get('edit_requirement_description')
            requirement_difficulty = request.forms.get('edit_requirement_difficulty')
            requirement_is_basic = bool(request.forms.get('edit_requirement_is_basic'))
            if requirement_description and requirement_difficulty:
                requirement.description = requirement_description
                requirement.difficulty = requirement_difficulty
                requirement.is_basic = requirement_is_basic
                requirement.save()
    redirect('/moderator/requirements#requirement-%s' % requirement.id)


@get('/moderator/tasks')
@view('moderator_tasks')
@check_moderator
def moderator_tasks():
    return {
        'selfies': Task
                   .select()
                   .where(
                        (Task.is_approved == False) 
                        & (Task.is_selfie_game == True)
                        & (Task.difficulty > 0)
                    )
                   .order_by(Task.is_complete, Task.difficulty.desc())
    }


@post('/moderator/regenerate_selfie')
@check_moderator
def do_regenerate_selfie():
    try:
        selfie = Task.get(
            Task.id == request.forms.get('selfie_id'),
            Task.is_approved == False,
            Task.is_selfie_game == True,
            Task.difficulty > 0
        )
    except Task.DoesNotExist:
        pass
    else:
        selfie.find_partner()
        if selfie.partner is not None:
            selfie.generate_description()
            if selfie.description is not None:
                selfie.is_rejected = False
                if selfie.is_complete:
                    selfie.is_complete = False
                    selfie.delete_photo()
                selfie.save()
    redirect('/moderator/tasks')


@get('/moderator/coupons')
@view('moderator_coupons')
@check_moderator
def moderator_coupons():
    coupons = {}
    for coupon in Coupon.select().order_by(Coupon.activated_by):
        if coupon.kind not in coupons:
            coupons[coupon.kind] = {
                'description': coupon.description,
                'reward': coupon.reward,
                'limit': coupon.limit,
                'codes': [(coupon.code, coupon.activated_by is None)]
            }
        else:
            coupons[coupon.kind]['codes'].append((coupon.code, coupon.activated_by is None))
    return {
        'created_coupon': request.query.created_coupon,
        'created_reward': request.query.created_reward,
        'created_limit': request.query.created_limit,
        'created_count': request.query.created_count,
        'coupons': coupons
    }


@post('/moderator/add_coupon')
@check_moderator
def do_add_coupon():
    coupon_description = request.forms.get('add_coupon_description')
    coupon_reward = request.forms.get('add_coupon_reward')
    coupon_limit = request.forms.get('add_coupon_limit')
    coupon_count = int(request.forms.get('add_coupon_count'))
    if coupon_description and coupon_reward and coupon_limit and coupon_count:
        kind = Coupon.generate_kind()
        for i in xrange(coupon_count):
            coupon = Coupon(
                description=coupon_description, 
                reward=coupon_reward,
                limit=coupon_limit,
                kind=kind
            )
            coupon.generate_code()
            coupon.save()
        redirect('/moderator/coupons?created_coupon=%s&created_reward=%s&created_limit=%s&created_count=%s' % (
            coupon_description.decode('utf-8'), 
            coupon_reward,
            coupon_limit,
            coupon_count
        ))
    else:
        redirect('/moderator/coupons')


@post('/moderator/delete_coupon')
@check_moderator
def do_delete_coupon():
    Coupon.delete().where(
        (Coupon.kind == request.forms.get('coupon_kind'))
        & (Coupon.activated_by >> None)
    ).execute()
    redirect('/moderator/coupons')


@get('/moderator/store')
@view('moderator_store')
@check_moderator
def moderator_store():
    return {
        'created_item': request.query.created_item,
        'created_price': request.query.created_price,
        'items': StoreItem
                 .select()
                 .order_by(StoreItem.price)
    }


@post('/moderator/add_store_item')
@check_moderator
def do_add_store_item():
    store_item_description = request.forms.get('add_store_item_description')
    store_item_price = request.forms.get('add_store_item_price')
    if store_item_description and store_item_price:
        StoreItem(
            description=store_item_description, 
            price=store_item_price
        ).save()
        redirect('/moderator/store?created_item=%s&created_price=%s' % (
            store_item_description.decode('utf-8'), 
            store_item_price
        ))
    else:
        redirect('/moderator/store')


@post('/moderator/delete_store_item')
@check_moderator
def do_delete_store_item():
    try:
        item = StoreItem.get(StoreItem.id == request.forms.get('store_item_id'))
    except StoreItem.DoesNotExist:
        pass
    else:
        for user in item.bought_users:
            User.update(score=User.score + item.price).where(User.id == user.user).execute()
        item.delete_instance()
    redirect('/moderator/store')


@get('/moderator/bought')
@view('moderator_bought')
@check_moderator
def moderator_bought():
    return {
        'items': BoughtStoreItem.select().where(BoughtStoreItem.is_delivered == False)
    }


@post('/moderator/deliver_item')
@check_moderator
def do_deliver_item():
    (BoughtStoreItem
        .update(is_delivered=True)
        .where(BoughtStoreItem.id == request.forms.get('item_id'))
        .execute()
    )
    redirect('/moderator/bought')


# user actions

def get_user(func):
    def wrapper():
        try:
            user = User.get(User.access_code == request.get_cookie('access_code'))
        except User.DoesNotExist:
            redirect('/')
        else:
            return func(user)
    return wrapper


@get('/user/allfeeds')
@view('user_allfeeds')
def user_allfeeds():
    return {
        'tasks': Task
                 .select()
                 .where(
                     (Task.is_selfie_game == True)
                     & (Task.is_approved == True)
                 )
                 .order_by(Task.difficulty)
    }


@get('/user/feed')
@view('user_feed')
@get_user
def user_feed(user):
    no_tasks_available = False
    while user.needs_more_selfie_tasks:
        selfie = Task(assignee=user, difficulty=user.current_difficulty + 1)

        selfie.find_partner()
        if selfie.partner is None:
            no_tasks_available = True
            break

        selfie.generate_description()
        if selfie.description is None:
            no_tasks_available = True
            break

        selfie.save()

    return {
        'user': user,
        'tasks': user.tasks.order_by(Task.is_complete, Task.is_approved, Task.approved_time.desc(), Task.difficulty.desc()),
        'no_tasks_available': no_tasks_available
    }


@post('/user/upload_photo')
@get_user
def do_upload_photo(user):
    try:
        task = Task.get(
            Task.id == request.forms.get('task_id'),
            Task.is_photo_required == True, 
            Task.is_complete == False
        )
        if task.assignee == user:
            photo = Image.open(request.files.get('photo_file').file)
            try:
                orientation = photo._getexif()[274]
            except (TypeError, AttributeError, KeyError):
                pass
            else:
                if orientation in [3, 6, 8]:
                    degrees = {
                        3: 180,
                        6: -90,
                        8: -270
                    }[orientation]
                    photo = photo.rotate(degrees)
            photo.thumbnail((1024, 1024))
            photo.save(task.photo_path)
            task.is_complete = True
            task.is_rejected = False
            task.save()
    except Task.DoesNotExist:
        pass
    redirect('/')


@get('/user/achievements')
@view('user_achievements')
@get_user
def user_achievements(user):
    return {
        'user': user,
        'achievements': user.coupons.order_by(Coupon.activated_time.desc()),
        'reject_coupon': request.query.reject_coupon,
        'activate_coupon': request.query.activate_coupon
    }


@post('/user/activate_coupon')
@get_user
def do_activate_coupon(user):
    try:
        coupon = Coupon.get(
            Coupon.code == request.forms.get('coupon_code').lower(),
            Coupon.activated_by >> None
        )
        activated_count = user.coupons.where(Coupon.kind == coupon.kind).count()
        if coupon.limit > activated_count:
            coupon.activated_by = user
            coupon.activated_time = datetime.utcnow()
            coupon.save()
            User.update(score=User.score + coupon.reward).where(User.id == user).execute()
            redirect('/user/achievements?activate_coupon=%s' % coupon.code)
        else:
            redirect('/user/achievements?reject_coupon=limit')
    except Coupon.DoesNotExist:
        redirect('/user/achievements?reject_coupon=doesnotexist')


@get('/user/store')
@view('user_store')
@get_user
def user_store(user):
    return {
        'user': user,
        'items': StoreItem.select().order_by(StoreItem.price)
    }


@post('/user/buy_store_item')
@get_user
def do_buy_store_item(user):
    try:
        item = StoreItem.get(StoreItem.id == request.forms.get('store_item_id'))
    except StoreItem.DoesNotExist:
        pass
    else:
        if not user.has_active_store_item(item) and user.score >= item.price:
            BoughtStoreItem.create(
                user=user,
                item=item
            )
            User.update(score=User.score - item.price).where(User.id == user).execute()
    redirect('/user/store')


# login actions

@view('login')
def login(wrong_code=False):
    return {'wrong_code': wrong_code}


@post('/')
def do_login():
    access_code = request.forms.get('access_code').lower()
    if access_code:
        response.set_cookie('access_code', access_code, max_age=14 * 24 * 3600)
    redirect('/')


@get('/logout')
def do_logout():
    response.set_cookie('access_code', '')
    redirect('/')


# slideshow actions

@get('/slideshow')
@view('slideshow')
def slideshow():
    return {
        'tasks': Task
                 .select()
                 .where(
                    (Task.is_approved == True) 
                    & (Task.is_selfie_game == True)
                 )
    }
    

run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)
