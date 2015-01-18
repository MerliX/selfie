# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime
from itertools import chain
from PIL import Image
from bottle import get, post, run, view, response, redirect, request
from models import User, Task, Requirement
from settings import HOST, PORT, DEBUG

MODERATOR_ACCESS_CODE = os.environ['SELFIE_MODERATOR_CODE']


@get('/')
def main():
    access_code = request.get_cookie('access_code')
    
    if access_code is None:
        return login()
    if access_code == MODERATOR_ACCESS_CODE:
        redirect('/moderator/feed')
    
    try:
        user = User.get(User.access_code == access_code)
    except User.DoesNotExist:
        return login(True)
    else:
        return user_feed(user)


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
            user_access_code = ''.join(
                chain(*zip(
                    random.sample('bcdfghjklmnpqrstvwxz', 3),
                    random.sample('aeiouy', 3)
                ))
            )
            user = User(
                name=user_name, 
                access_code=user_access_code
            )
            user.save()
            task = Task(
                assignee=user,
                description=u'Сделай селфи, чтобы хорошо было видно лицо.',
                difficulty=0
            )
            task.save()
        else:
            user_access_code = user.access_code
        redirect(
            '/moderator/users?created_name=%s&created_access_code=%s' % 
            (user_name.decode('utf-8'), user_access_code)
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


@post('/moderator/delete_requirement')
@check_moderator
def do_delete_requirement():
    try:
        requirement = Requirement.get(Requirement.id == request.forms.get('requirement_id'))
    except Requirement.DoesNotExist:
        pass
    else:
        requirement.delete_instance()
    redirect('/moderator/requirements')


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
                if selfie.is_complete:
                    selfie.is_complete = False
                    selfie.delete_photo()
                selfie.save()
    redirect('/moderator/tasks')


# user actions

@view('user_feed')
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
        'tasks': user.tasks.order_by(Task.is_complete, Task.is_approved, Task.approved_time.desc()),
        'no_tasks_available': no_tasks_available
    }


@post('/user/upload_photo')
def do_upload_photo():
    try:
        task = Task.get(
            Task.id == request.forms.get('task_id'),
            Task.is_photo_required == True, 
            Task.is_complete == False
        )
        if task.assignee.access_code == request.get_cookie('access_code'):
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
            task.save()
    except Task.DoesNotExist:
        pass
    redirect('/')


# login actions

@view('login')
def login(wrong_code=False):
    return {'wrong_code': wrong_code}


@post('/')
def do_login():
    access_code = request.forms.get('access_code').lower()
    if access_code:
        response.set_cookie('access_code', access_code)
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
                    & (Task.difficulty > 0)
                 )
                 .order_by(Task.approved_time.desc())
                 .limit(10)
    }
    

run(host=HOST, port=PORT, debug=DEBUG, reloader=DEBUG)
