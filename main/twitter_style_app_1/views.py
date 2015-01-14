# Python Imports
import json

# Django Imports
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from twitter_style_app_1.models import UserStatus
from twitter_style_app_1.models import UserExtended
from django.core import serializers
from twitter_style_app_1.authentication_wrapper import allow_if_authenticated


def register_new_user(request):
    """
    Registers a new user.
    """
    try:
        # create User object
        user_object = User.objects.create_user(username=request.POST['username'],
                                               first_name=request.POST['first_name'],
                                               last_name=request.POST['last_name'],
                                               email=request.POST['email'],
                                               password=request.POST['password'])
        user_object.save()

        # create UserExtended object and link to User object
        user_extended_object = UserExtended(user=user_object)
        user_extended_object.save()

        # return
        return HttpResponse(json.dumps("user %s successfully created" % user_object.username), 'application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)


def user_login(request):
    """
    Logs a user into this application.
    """
    try:
        # authenticate user
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        # if user and password return a valid user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps("user %s successfully logged in" % user.username), 'application/json')
            else:
                return HttpResponse(json.dumps("FAIL: %s is not a user" % user.username), 'application/json')

        # if user and password does not return a valid user
        else:
            return HttpResponse(json.dumps("FAIL: user login failed"), 'application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)


@allow_if_authenticated
def user_logout(request):
    """
    Logs a user out of this application.
    """
    try:
        # log out user
        logout(request)

        # return
        return HttpResponse(json.dumps("log out successful"), 'application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)


@allow_if_authenticated
def new_status(request):
    """
    Allows a single user to update their status.
    """
    try:
        # create new UserStatus object and link to user object
        user_status_object = UserStatus(status=request.POST['status'])
        user_status_object.user = UserExtended.objects.get(user__id=request.POST['user_id'])
        user_status_object.save()

        # returned
        return HttpResponse(json.dumps("user %s successfully created new status" % user_status_object.user.user.username),
                            'application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)


@allow_if_authenticated
def follow_user(request, this_user_id, user_to_follow_id):
    """
    Allows a single user to follow another user.
    """
    try:
        # get the user object of the user who want to follow another user
        this_user_object = UserExtended.objects.get(user__id=this_user_id)

        # get the user object of the user who is to be followed
        user_to_follow_object = UserExtended.objects.get(user__id=user_to_follow_id)

        # link the records
        this_user_object.users_following = user_to_follow_object
        this_user_object.save()

        # returned
        return HttpResponse(json.dumps("user %s successfully following %s" % (this_user_object.user.username,
                                                                              user_to_follow_object.user.username)),
                            'application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)


@allow_if_authenticated
def view_time_line(request, user_id):
    """
    Allows a user to view a time line of another user. A time line is a list of all users active status posts.
    """
    try:
        # get status/time line objects for a user
        time_line = UserStatus.objects.filter(user__id=user_id, active=True)
        return_data = serializers.serialize('json', time_line,
                                            indent=2,
                                            use_natural_keys=True)

        # return
        return HttpResponse(return_data, 'application/json')
    except Exception as error:
        return HttpResponseBadRequest(error)