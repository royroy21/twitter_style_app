# twitter_style_app

WARNING: This app is not finished.

#########################################################################################################################
DESCRIPTION:
#########################################################################################################################
The twitter style app is the backend framework of a simple messaging app. The app allows users to do the following:

-register
-login
-logout
-follow a user (currently links other users to the following user's database model)
-post a status
-view another user's time line (currently a time line is made up of all active user status posts)


#########################################################################################################################
API BREAKDOWN:
#########################################################################################################################
The following API links are to be used for front-end creation:

register_new_user "^register_new_user/$" (POST)

	post example = {'username': 'roy1',
			'first_name': 'Roy',
			'last_name': 'Hanley',
			'email': 'royhanley8@gmail.com',
			'password': 'small fat gibbon'}

user_login "^user_login/$" (POST)

	post example = {'username': 'roy1',
			'password': 'small fat gibbon'}

user_logout "^user_logout/$" (GET)

new_status "^new_status/$" (POST)

	post example = {'user_id': User.objects.get(username='roy1').id,
			'status': 'my first status post'}

follow_user "^follow_user/(?P<this_user_id>[^/]+)/(?P<user_to_follow_id>[^/]+)/$" (GET, this_user_id, user_to_follow_id)

view_time_line "^view_time_line/(?P<user_id>[^/]+)/$" (GET, user_id)


#########################################################################################################################
INSTALL APPICATION:
#########################################################################################################################
1) If you haven't already done so please install Django for your computer/server.
2) Pull the application from GitHub
3) Using the command line navigate to the manage.py file
4) run the following commands: python manange.py migrate; python manage.py; python manage.py makemigrations twitter_style_app_1; python manage.py migrate

Your application is now installed. The following commands maybe helpfull:
- python manage.py runserver (to start the server)
- python manage.py test (to check unittests run correctly)
