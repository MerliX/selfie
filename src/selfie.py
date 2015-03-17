# -*- coding: utf-8 -*-

import os
from datetime import datetime
from PIL import Image
from bottle import get, post, run, view, response, redirect, request, hook, static_file, route
from models import User, Task, Requirement, db
from settings import HOST, PORT, DEBUG, PHOTO_PATH, USE_POSTGRES, SERVER, WORKERS


MODERATOR_ACCESS_CODE = os.environ['SELFIE_MODERATOR_CODE']


@route('/static/<filepath:path>')
def static_files(filepath):
    return static_file(filepath, root=os.path.dirname(os.path.realpath(__file__)) + '\\..\\static\\')


@route('/selfies/<filepath:path>')
def static_selfies(filepath):
    return static_file(filepath, root=PHOTO_PATH)


@hook('before_request')
def _connect_db():
    db.connect()
    if not USE_POSTGRES:
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
        if is_moderator():
            return func()
        else:
            redirect('/')
    return wrapper


def is_moderator():
    return request.get_cookie('access_code') == MODERATOR_ACCESS_CODE


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

            user = User.select().where(User.id == task.assignee).get()
            user.score = user.score + task.reward
            user.is_active = True
            user.save()

            if task.partner:
                (User
                    .update(score=User.score + task.reward / 2)
                    .where(User.id == task.partner)
                    .execute())
        elif request.forms.get('decision') == 'reject':
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
    user_company = request.forms.get('add_user_company')
    if user_name:
        user = User.add(user_name, user_company)
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
    description = request.forms.get('add_requirement_description')
    difficulty = request.forms.get('add_requirement_difficulty')
    is_basic = bool(request.forms.get('add_requirement_is_basic'))
    if Requirement.add(description, difficulty, is_basic):
        redirect('/moderator/requirements?created_requirement=%s&created_difficulty=%s&created_is_basic=%s' % (
            description.decode('utf-8'),
            difficulty,
            is_basic
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


# user actions

def get_user(func):
    def wrapper():
        try:
            if is_moderator():
                user = User.get(User.id == request.query.get('user'))
            else:
                user = User.get(User.access_code == request.get_cookie('access_code'))
            return func(user)
        except User.DoesNotExist:
            redirect('/')
    return wrapper


@get('/user/allfeeds')
@view('user_allfeeds')
def user_allfeeds():
    return {
        'tasks': Task
                 .select()
                 .where(
                     (Task.is_approved == True)
                 )
                 .order_by(Task.difficulty)
    }


@get('/user/feed')
@view('user_feed')
@get_user
def user_feed(user):
    generated = user.ensure_tasks_generated()
    approved = (Task
        .select()
        .where(((Task.partner == user) | (Task.assignee == user)) & (Task.is_approved == True))
        .order_by(Task.approved_time.desc())
    )
    active = (user.tasks
         .select()
         .where(Task.is_approved == False)
         .order_by(Task.is_complete, Task.difficulty.desc())
    )
    return {
        'user': user,
        'active_tasks': active,
        'approved_tasks': approved,
        'generated': generated
    }


def save_photo(data, path):
    photo = Image.open(data)
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
    photo.save(path)


@post('/user/upload_photo')
def do_upload_photo():
    try:
        task = Task.get(
            Task.id == request.forms.get('task_id'),
            Task.is_complete == False
        )
        if is_moderator() | (task.assignee.access_code == request.get_cookie('access_code')):
            save_photo(request.files.get('photo_file').file, task.photo_path)
            task.is_complete = True
            task.is_rejected = False
            task.save()
    except Task.DoesNotExist:
        pass
    redirect('/')


@get('/user/upload_photo')
def upload_photo_get():
    redirect('/')  # workaround to prevent error when upload is failed

# login actions


@view('login')
def login(wrong_code=False):
    return {'wrong_code': wrong_code}


@post('/')
def do_login():
    access_code = request.forms.get('access_code').lower().strip()
    if access_code:
        response.set_cookie('access_code', access_code, max_age=14 * 24 * 3600)
    redirect('/')


@route('/go/<access_code>')
@view('go')
def go(access_code):
    return {'code': access_code}


@get('/logout')
def do_logout():
    response.set_cookie('access_code', '')
    redirect('/')


# service/test actions

@get('/recreate_db')
def do_recreate_db():
    if DEBUG:
        from recreate_db import recreate_database
        recreate_database()
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
                    & (Task.difficulty > 0)
                 )
                 .order_by(Task.approved_time.desc())
                 .limit(30)
    }


run(
    server=SERVER,
    workers=WORKERS,
    host=HOST,
    port=PORT,
    debug=DEBUG,
    reloader=DEBUG
)
