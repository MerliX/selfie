import os
import random
import string
from datetime import datetime
from PIL import Image
from bottle import get, post, run, view, response, redirect, request
from models import User, Perk, Selfie
from settings import HOST, PORT, DEBUG

MODERATOR_ACCESS_CODE = os.environ['SELFIE_MODERATOR_CODE']
ALLOWED_CODE_SYMBOLS = string.lowercase + string.digits


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
        selfie = Selfie.get(Selfie.is_uploaded == True, Selfie.is_approved == False)
    except Selfie.DoesNotExist:
        selfie = None

    return {
        'created_perk': request.query.created_perk,
        'created_level': request.query.created_level,
        'selfie': selfie
    }


@post('/moderator/approve_selfie')
@check_moderator
def do_approve_selfie():
    try:
        selfie = Selfie.get(
            Selfie.id == request.forms.get('selfie_id'),
            Selfie.is_uploaded == True,
            Selfie.is_approved == False
        )
    except Selfie.DoesNotExist:
        pass
    else:
        if request.forms.get('decision') == 'approve':
            selfie.is_approved = True
            selfie.approved_time = datetime.utcnow()
            selfie.save()

            if selfie.author.approved_ratio >= 2./3:
                next_level = selfie.author.next_level
                for i in range(2):
                    new_perk = Perk.get_least_used(next_level)
                    new_victim = selfie.author.get_random_victim()
                    Selfie(author=selfie.author, victim=new_victim, perk=new_perk).save()

        elif request.forms.get('decision') == 'reject':
            selfie.delete_photo()
            selfie.is_uploaded = False
            selfie.save()
    redirect('/')


@get('/moderator/users')
@view('moderator_users')
@check_moderator
def moderator_users():
    return {
        'created_name': request.query.created_name,
        'created_access_code': request.query.created_access_code,
        'user_perk': request.query.user_perk,
        'users': User.get_moderator_summary()
    }


@post('/moderator/add_user')
@check_moderator
def do_add_user():
    user_name = request.forms.get('add_user_name')
    if user_name:
        try:
            user = User.get(User.name == user_name)
        except User.DoesNotExist:
            user_access_code = ''.join(random.sample(ALLOWED_CODE_SYMBOLS, 6))
            perk = Perk.get_least_used(0)
            user = User(name=user_name, access_code=user_access_code, perk=perk)
            user.save()
            Selfie(author=user, victim=user, perk=perk).save()
        else:
            user_access_code = user.access_code
        redirect(
            '/moderator/users?created_name=%s&created_access_code=%s&user_perk=%s' % 
            (user_name.decode('utf-8'), user_access_code, user.perk.text)
        )
    else:
        redirect('/moderator/users')


@get('/moderator/perks')
@view('moderator_perks')
@check_moderator
def moderator_perks():
    return {
        'created_perk': request.query.created_perk,
        'created_level': request.query.created_level,
        'perks': Perk.select().order_by(Perk.level)
    }


@post('/moderator/add_perk')
@check_moderator
def do_add_perk():
    perk_text = request.forms.get('add_perk_text')
    perk_level = request.forms.get('add_perk_level')
    if perk_level and perk_text:
        Perk(text=perk_text, level=perk_level).save()
        redirect('/moderator/perks?created_perk=%s&created_level=%s' % (perk_text.decode('utf-8'), perk_level))
    else:
        redirect('/moderator/perks')


# user actions

@view('user_feed')
def user_feed(user):
    return {'user': user}


@post('/user/upload_selfie')
def do_upload_selfie():
    try:
        selfie = Selfie.get(
            Selfie.id == request.forms.get('selfie_id'), 
            Selfie.is_uploaded == False
        )
        if selfie.author.access_code == request.get_cookie('access_code'):
            photo = Image.open(request.files.get('selfie_file').file)
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
            photo.save(selfie.photo_path)
            selfie.is_uploaded = True
            selfie.save()
    except Selfie.DoesNotExist:
        pass
    redirect('/')


# login actions

@view('login')
def login(wrong_code=False):
    return {'wrong_code': wrong_code}


@post('/')
def do_login():
    access_code = request.forms.get('access_code')
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
        'selfies': Selfie.get_latest_approved(10)
    }
    

run(host=HOST, port=PORT, debug=DEBUG)
