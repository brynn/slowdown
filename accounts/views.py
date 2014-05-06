# django functions
from django.conf import settings
from django.template import RequestContext, Context
from django.template.loader import get_template, render_to_string
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core.urlresolvers import reverse

# datetimes and timezones
import datetime
from datetime import date, timedelta
from django.utils.timezone import utc, get_current_timezone_name
from dateutil import tz

# database models
from django.db import models
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from social.apps.django_app.default.models import UserSocialAuth
from accounts.models import UserProfile, Twitter, Instagram, Item

# api clients
import tweepy
from instagram.client import InstagramAPI

# random python stuff
import random
import logging
import itertools
import os
import subprocess
import sys
import base64
import hashlib
import json
import Image
import urllib
from StringIO import StringIO

# constants
SOCIAL_AUTH_TWITTER_KEY = 'iOPlmeF3uXxJdNvttvYWA'
SOCIAL_AUTH_TWITTER_SECRET = 'RkRkkTImAHaH247fj2s4VTIftdv3odYJ6c5Tu2Y'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TWITTER_COUNT = 10
INSTAGRAM_COUNT = 9

# HELPER FUNCTIONS

# helps process list of twitter friends
def paginate(iterable, pageSize):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, pageSize, None),
            list(itertools.islice(i2, pageSize)))
        if len(page) == 0:
            break
        yield page

# does a word have a number in it (haiku helper function)
def has_number(word):
	for c in word:
		if c.isdigit():
			return True
	return False

# does a work consist of only punctuation (haiku helper function)
def is_only_punc(word):	
	for c in word:
		if c.isalnum():
			return False
	return True

# haiku helper function (I forget what this does)
def split(str, num):
	return [ str[start:start+num] for start in range(0, len(str), num) ]

# unique hash generator
def hash_from_id(id):
	return base64.urlsafe_b64encode(hashlib.md5(str(id)).digest())[:11]

# tests for valid images (for rendering profile pics)
def is_valid_image(url):
	try:
		Image.open(StringIO(urllib.urlopen(url).read()))
		return True
	except:
		return False
		
# LOGGED OUT VIEWS

# home page with sign up/in buttons
def home(request):
    if request.user.is_authenticated():
        return redirect('done')
    return render_to_response('home.html', {}, RequestContext(request))
 
# digest examples page   
def examples(request):
	return render_to_response('examples.html', { 'user' : request.user }, RequestContext(request))
	
# item permalink page
def item_permalink(request, hash_code):
	item = get_object_or_404(Item, hash_code=hash_code)
	return render_to_response('item.html', {
   	 'item' : item,
   	 'request' : request,

	}, RequestContext(request))


# LOGGED IN VIEWS

# logging out
@login_required
def logout(request):
    auth_logout(request)
    return render_to_response('home.html', {}, RequestContext(request))
    	
# unsubscribing
@login_required
def unsubscribe(request):
	deleted = False
	user = get_object_or_404(User, username=request.user.username)
	if request.method == 'POST':
		user.delete()
		deleted = True
	return render_to_response('unsubscribe.html', {
   	 'user' : user,
   	 'deleted' : deleted,
	}, RequestContext(request))

# signing in/up
@login_required
def signup(request):
	
	user = get_object_or_404(User, username=request.user.username)
	user_profile = get_object_or_404(UserProfile, user=user)
	user_twitter = UserSocialAuth.objects.filter(user=user, provider='twitter')
	user_instagram = UserSocialAuth.objects.filter(user=user, provider='instagram') 
	twitter_connected = False  
	instagram_connected = False
	
	# connect to twitter api
	if user_twitter:
		twitter_connected = True
		oauth_access_token=(user_twitter.get().tokens).get('oauth_token')
		oauth_access_secret=(user_twitter.get().tokens).get('oauth_token_secret')
		auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
		auth.set_access_token(oauth_access_token, oauth_access_secret)
		api_twitter = tweepy.API(auth)
	
	# connect to instagram api
	if user_instagram:
		instagram_connected = True
		token_instagram = user_instagram.get().tokens
		api_instagram = InstagramAPI(access_token=token_instagram)
	
	# if the user has already signed up, get profile pics and redirect to logged in home page
	if user.email:
	
		# if the user has signed up and just connected twitter via edit settings, stay on edit settings
		if user_twitter and len(user_profile.twitters.all()) == 0:
			return HttpResponseRedirect('/edit-settings/')
		
		# if the user has signed up and just connected instagram via edit settings, stay on edit settings
		if user_instagram and len(user_profile.instagrams.all()) == 0:
			return HttpResponseRedirect('/edit-settings/')
			
		# get twitter profile pics (and check that they are valid)
		if user_twitter and 'twitter_faces' not in request.session:
			request.session['twitter_faces'] = []
			for t in user_profile.twitters.all():
				if is_valid_image(t.url) and t.uid:
					request.session['twitter_faces'].append([t.username, t.url])
				else:
					try:
						t_user = api_twitter.get_user(screen_name=t.username)
						request.session['twitter_faces'].append([t.username, t_user.profile_image_url])
						t.url = t_user.profile_image_url
						t.uid = t_user.id
						t.save()
					except Exception:
						print >> sys.stderr, user_profile.user.username +': Logging in, Twitter API error, couldn\'t get Twitter object profile pic for ' + t.username
		
		# get instagram profile pics (and check that they are valid)		
		if user_instagram and 'insta_faces' not in request.session:
			request.session['insta_faces'] = []
			for i in user_profile.instagrams.all():
				if is_valid_image(i.url) and i.uid:
					request.session['insta_faces'].append([i.username, i.url])
				else:
					try:
						i_user = api_instagram.user_search(i_username)[0]
						request.session['insta_faces'].append([i.username, i_user.profile_picture])
						i.url = i_user.profile_picture
						i.uid = i_user.id
						i.save()
					except Exception:
						print >> sys.stderr, user_profile.user.username +': Logging, Instagram API error, couldn\'t get Instagram object profile pic for ' + i.username
		
		# convert UTC time to local time for rendering on logged in home page
		local_time = user_profile.next_email_time - timedelta(hours=user_profile.tz_offset)
		
		# redirect to logged in home page
		return render_to_response('done.html', {
			'user_profile' : user_profile,
			'session' : request.session,
			'local_time' : local_time,
		}, RequestContext(request))
    	
	else:
		# get list of twitter friends
		if user_twitter and 'twitter_list' not in request.session:
			request.session['twitter_list'] = [] 
# 			request.session['t_pickforme'] = ''
# 			t_counter = 0
			friends_ids = []
			try:
				friends_cursor = tweepy.Cursor(api_twitter.friends_ids,id=user_twitter.get().uid)
				for id in friends_cursor.items():
					friends_ids.append(id)
				for friends_page in paginate(friends_ids, 100):
					friends_objects = api_twitter.lookup_users(user_ids=friends_page)
					for friend in friends_objects:    				
						request.session['twitter_list'].append(friend.screen_name)
						#TODO: make this async yo
# 						if int(friend.followers_count) > 300 and int(friend.statuses_count) > 1000 and t_counter < 10:
# 							request.session['t_pickforme'] += friend.screen_name + ', '
# 							t_counter += 1
			except Exception:
				print >> sys.stderr, user_profile.user.username +': Signing up, Twitter API error, tried to get friend list'
		
		# get list of instagram friends
		if user_instagram and 'instagram_list' not in request.session:
			request.session['instagram_list'] = []
# 			request.session['i_pickforme'] = ''
# 			i_counter = 0
			try:
				for page in api_instagram.user_follows(user_id=user_instagram.get().uid, as_generator=True, max_pages=15):
					for friend in page[0]:
						request.session['instagram_list'].append(friend.username)
						#TODO: make this async yo
# 						if i_counter < 10:
# 							user_object = api_instagram.user(friend.id)
# 							if int(user_object.counts['followed_by']) > 300 and int(user_object.counts['media']) > 100:
# 								request.session['i_pickforme'] += friend.username + ', '
# 								i_counter += 1
			except Exception:
				print >> sys.stderr, user_profile.user.username +': Signing up, Instagram API error, tried to get friend list'
		
		# render sign up form
		return render_to_response('signup.html', {
		 'user_profile' : user_profile,
		 'instagram_connected' : instagram_connected,
		 'twitter_connected' : twitter_connected,
		 'session' : request.session,
		}, RequestContext(request))

# processing the sign up/edit settings form  
@login_required  
def done(request):

	user_profile = get_object_or_404(UserProfile, user=request.user)
	user = get_object_or_404(User, username=request.user.username)
	user_twitter = UserSocialAuth.objects.filter(user=request.user, provider='twitter')
	user_instagram = UserSocialAuth.objects.filter(user=request.user, provider='instagram')
	instagram_connected = False 
	local_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	
	# connect to twitter api
	if user_twitter:
		oauth_access_token=(user_twitter.get().tokens).get('oauth_token')
		oauth_access_secret=(user_twitter.get().tokens).get('oauth_token_secret')
		auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
		auth.set_access_token(oauth_access_token, oauth_access_secret)
		api_twitter = tweepy.API(auth)
	
	# connect to instagram api
	if user_instagram:
		instagram_connected = True
		token_instagram = user_instagram.get().tokens
		api_instagram = InstagramAPI(access_token=token_instagram)

	if 'twitter_faces' not in request.session:
		request.session['twitter_faces'] = []
	if 'insta_faces' not in request.session:
		request.session['insta_faces'] = []
	
	# form processing						
	if request.method == 'POST':
		request.session['errors'] = {}
		error_exists = False
		UTC_OFFSET = int(request.POST.get('tz-offset'))
		
		#TODO: better email validation?
		if request.POST.get('email') == '':
			request.session['errors']['email'] = True
			error_exists = True
		else:
			request.session['errors']['email'] = False
		if request.POST.get('twitters') == '':
			request.session['errors']['twitter'] = True
			error_exists = True
		else:
			request.session['errors']['twitter'] = False
		if request.POST.get('instagrams') == '':
			request.session['errors']['instagram'] = True
			error_exists = True
		else:
			request.session['errors']['instagram'] = False
		if error_exists:
			if user.email:
				return HttpResponseRedirect('/edit-settings/')
			else:
				return HttpResponseRedirect('/signup/')
				
		user.email = request.POST.get('email')
		user.save()
		user_profile.frequency = int(request.POST.get('frequency'))
    	
    	# default next_email_time to Monday at 9AM
		day_of_week = 0
		time_of_day = 9
		time_of_day_string = '9:00 AM'
		
		# day of week
		if (int(request.POST.get('surprise-day')) == 1):
			user_profile.surprise_day = True
			day_of_week = random.randint(0,6)
		else:
			user_profile.surprise_day = False
			day_of_week = request.POST.get('day-of-week')

		# time of day
		if (int(request.POST.get('surprise-time')) == 1):
			user_profile.surprise_time = True
			time_of_day = random.randint(0, 23)
		else:
			user_profile.surprise_time = False
			time_of_day_string = request.POST.get('time-of-day')
			time_of_day = datetime.datetime.strptime(time_of_day_string[:-3], "%H:00").hour
			if (time_of_day_string[-2:] == 'PM'):
				if (int(time_of_day) != 12):
					time_of_day = int(time_of_day) + 12
			else:
				if int(time_of_day) == 12:
					time_of_day = 0
		
		# figure out next_email_time magic
		today = datetime.datetime.utcnow().replace(tzinfo=utc)
		today_weekday = today.weekday()
		
		days_delta = 1
		utc_hour = int(time_of_day) + UTC_OFFSET
		if (int(request.POST.get('frequency')) == 1):
			days_delta = int(day_of_week) - today_weekday
			if utc_hour > 23:
				utc_hour = utc_hour % 24
			# same day of week, earlier time = send next week
			if today_weekday == int(day_of_week):
				if today.hour >= utc_hour:
					days_delta = (7 - today_weekday) + int(day_of_week)
				else: 
					days_delta = 0
    		# day of week has already passed = send next week		
			if today_weekday > int(day_of_week):
				days_delta = (7 - today_weekday) + int(day_of_week)
		else:
			# if you switch to daily, surprise day doesn't make sense
			user_profile.surprise_day = False
			# if you choose a time later today, send it today
			if today.hour < utc_hour:
				days_delta = 0
		
		# set the next day to send
		next_email_time = today + timedelta(days=days_delta)
		
		# set the next time to send
		next_email_time = next_email_time.replace(hour=int(time_of_day), minute=0, second=0, microsecond=0) + timedelta(hours=UTC_OFFSET)
		user_profile.next_email_time = next_email_time
			
		user_profile.lat = request.POST.get('lat')
		user_profile.lon = request.POST.get('lon')
		user_profile.tz_offset = UTC_OFFSET
		
		# binary logic for including email sections or not
		if request.POST.get('remixing') and int(request.POST.get('remixing')) == -1:
			user_profile.remixing = False
		else:
			user_profile.remixing = True
		if request.POST.get('zen') and int(request.POST.get('zen')) == -1:
			user_profile.zen = False
		else:
			user_profile.zen = True		
		if request.POST.get('podcasts') and int(request.POST.get('podcasts')) == -1:
			user_profile.podcasts = False
		else:
			user_profile.podcasts = True
		if request.POST.get('voyeurism') and int(request.POST.get('voyeurism')) == -1:
			user_profile.voyeurism = False
		else:
			user_profile.voyeurism = True
		if request.POST.get('appendix-t') and int(request.POST.get('appendix-t')) == -1:
			user_profile.appendix_t = False
		else:
			user_profile.appendix_t = True
		if request.POST.get('appendix-i') and int(request.POST.get('appendix-i')) == -1:
			user_profile.appendix_i = False
		else:
			user_profile.appendix_i = True
		
		# get or create Twitter database objects and associate with the user			
		if request.POST.get('twitters'):
			UserProfile.twitters.through.objects.filter(userprofile=user_profile).delete()
			request.session['twitter_faces'] = []
			request.session.modified = True
			twitters_list = request.POST.get('twitters').replace(' ','').replace('@', '').split(',')
			for t_name in twitters_list:
				if len(t_name) > 1:	
					t, created = Twitter.objects.get_or_create(username=t_name)		
					if created:
						try:
							t_user = api_twitter.get_user(screen_name=t_name)
							t.uid = t_user.id
							t.url = t_user.profile_image_url
							t.save()
						except Exception:
							print >> sys.stderr, user_profile.user.username +': Saving settings, Twitter API error, couldn\'t create Twitter object in database for ' + t_name
					if is_valid_image(t.url) and t.uid:
						request.session['twitter_faces'].append([t.username, t.url])	
					else:
						try:
							t_user = api_twitter.get_user(screen_name=t_name)
							request.session['twitter_faces'].append([t.username, t_user.profile_image_url])
							t.url = t_user.profile_image_url
							t.uid = t_user.id
							t.save()
						except Exception:
							print >> sys.stderr, user_profile.user.username +': Saving settings, Twitter API error, couldn\'t get Twitter object profile pic for ' + t_name
					request.session.modified = True
					user_profile.twitters.add(t)		
 											
			#include my own tweets
			if int(request.POST.get('my-tweets')) == 1:
				try:
					t_user = api_twitter.get_user(id=user_twitter.get().uid)
					t_self, created = Twitter.objects.get_or_create(username=t_user.screen_name)
					if created:
						t_self.uid = t_user.id
						t_self.url = t_user.profile_image_url
						t_self.save()
					if is_valid_image(t_self.url) and t_self.uid:
						request.session['twitter_faces'].append([t_self.username, t_self.url])
					else:
						request.session['twitter_faces'].append([t_self.username, t_user.profile_image_url])
						t_self.url = t_user.profile_image_url
						t_self.uid = t_user.id
						t_self.save()
					request.session.modified = True
					user_profile.twitters.add(t_self)
				except Exception:
					print >> sys.stderr, user_profile.user.username +': Saving settings, Twitter API error, couldn\'t create Twitter object in database (adding yourself)'
				
		# get or create Instagram database objects and associate with the user	
		if request.POST.get('instagrams'):	
			UserProfile.instagrams.through.objects.filter(userprofile=user_profile).delete()
			request.session['insta_faces'] = []
			request.session.modified = True
			instagrams_list = request.POST.get('instagrams').replace(' ','').split(',')
			for i_name in instagrams_list:
				if len(i_name) > 1:
					i, created = Instagram.objects.get_or_create(username=i_name)
					if created:
						try:
							i_user = api_instagram.user_search(i_name)[0]
							i.uid = i_user.id
							i.url = i_user.profile_picture
							i.save()
						except Exception:
							print >> sys.stderr, user_profile.user.username +': Saving settings, Instagram API error, couldn\'t create Instagram object in database for ' + i_name
					if is_valid_image(i.url) and i.uid:
						request.session['insta_faces'].append([i.username, i.url])
					else:
						try:
							i_user = api_instagram.user_search(i_name)[0]
							request.session['insta_faces'].append([i.username, i_user.profile_picture])
							i.url = i_user.profile_picture
							i.uid = i_user.id
							i.save()
						except Exception:
							print >> sys.stderr, user_profile.user.username +': Saving settings, Instagram API error, couldn\'t get Instagram object profile pic for ' + i_name
					request.session.modified = True
					user_profile.instagrams.add(i)	
					
			#include my own photos
			if int(request.POST.get('my-photos')) == 1:
				try:
					i_user = api_instagram.user(id=user_instagram.get().uid)
					i_self, created = Instagram.objects.get_or_create(username=i_user.username)
					if created:
						i_self.uid = i_user.id
						i_self.url = i_user.profile_picture
						i_self.save()
					if is_valid_image(i_self.url) and i_self.uid:
						request.session['insta_faces'].append([i_self.username, i_self.url])
					else:
						request.session['insta_faces'].append([i_self.username, i_user.profile_picture])
						i.url = i_user.profile_picture
						i.uid = i_user.id
						i.save()
					request.session.modified = True
					user_profile.instagrams.add(i_self)
				except Exception:
					print >> sys.stderr, user_profile.user.username +': Saving settings, Instagram API error, couldn\'t create Instagram object in database (adding yourself)'
						
		user_profile.save()
		local_time = user_profile.next_email_time - timedelta(hours=UTC_OFFSET)
	
	if user_profile.tz_offset:
		local_time = user_profile.next_email_time - timedelta(hours=user_profile.tz_offset)
	return render_to_response('done.html', {
        'user_profile' : user_profile,
        'session' : request.session,
        'local_time' : local_time,
    }, RequestContext(request))

# construct and send that email
def email_helper(user):
	error_code = 'OK'

	user_profile = get_object_or_404(UserProfile, user=user)	
	user_twitter= UserSocialAuth.objects.filter(user=user, provider='twitter')
	user_instagram = UserSocialAuth.objects.filter(user=user, provider='instagram')
	
	# initialize those variables
	tweets = {}
	instagrams = {}
	instagram_links = {}
	mashups = None
	mashup_links = {}
	haikus_attributed = []
	haiku_links = {}
	audio_links = {}	
	random_photos = []
	num_haikus = 8
	num_mashups = 9
	
	# TWITTER CONTENT (HAIKUS, PODCAST)
	
	# connect to twitter api
	if user_twitter:
		oauth_access_token=(user_twitter.get().tokens).get('oauth_token')
		oauth_access_secret=(user_twitter.get().tokens).get('oauth_token_secret')
		auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
		auth.set_access_token(oauth_access_token, oauth_access_secret)
		api_twitter = tweepy.API(auth)  	
	
	# haiku input txt file
	f_haikus = open(os.path.join(BASE_DIR, 'tweets_haikus.txt'), 'w')
	# twitter audio input txt file
	f_audio = open(os.path.join(BASE_DIR, 'tweets_audio.txt'), 'w')
	
	# get tweets and write new tweets to haiku and twitter audio input files
	for person in user_profile.twitters.all():		
		person_tweets = []
		try:
			timeline = api_twitter.user_timeline(screen_name=person.username, include_rts=False, exclude_replies=True, count=TWITTER_COUNT)
			f_audio.write('\nSTARTING TWEETS FROM USERNAME, @' + person.username.encode('ascii', 'xmlcharrefreplace') + ':\n,')
			for t in timeline:
				if t.created_at.replace(tzinfo=utc) >= user_profile.last_email_time:
					person_tweets.append(t)			
					
					filtered_tweet = ' '.join([word for word in t.text.split(' ') if not word.startswith('http') and not has_number(word) and not is_only_punc(word)])
					f_haikus.write(filtered_tweet.encode('ascii', 'xmlcharrefreplace') + '{')
					
					no_links = ' '.join([word for word in t.text.split(' ') if not word.startswith('http')])
					f_audio.write(no_links.encode('ascii', 'xmlcharrefreplace') + ' ,STOP, \n')
					
			if len(person_tweets) > 0:
				tweets[person.username] = person_tweets
		except Exception:
			print >> sys.stderr, user_profile.user.username +': Sending email, Twitter API error, couldn\'t fetch timeline'
	f_audio.write('\n END OF ALL TWEETS')
	f_audio.close()
	f_haikus.close()
	
	# run the haiku script
	p_haikus = subprocess.Popen(['python2.7', '/home/bshepherd/webapps/slowdown_django/slowdown/haiku.py', '/home/bshepherd/webapps/slowdown_django/slowdown/tweets_haikus.txt'], stdout=subprocess.PIPE)
	haikus = p_haikus.communicate()[0].split('\n')
	
	# attribute the haikus (this code is the worst code)
	haikus_split = split(haikus, 4)	
	haiku_pool = ['\n'.join(h[:-1]) for h in haikus_split]
	if len(haiku_pool) < num_haikus:
		num_haikus = len(haiku_pool)	
	haikus_result = random.sample(haiku_pool, num_haikus)
	sub_results = []
	
	for h in haikus_result:
		substrings = h.split('{')
		if len(substrings) == 1:	
			for username, t_list in tweets.items():			
				for t in t_list:
					filtered_tweet = ' '.join([word for word in t.text.split(' ') if not word.startswith('http') and not has_number(word) and not is_only_punc(word)])
					
					if h.replace('\n', ' ').strip().encode('ascii', 'xmlcharrefreplace') in filtered_tweet.encode('ascii', 'xmlcharrefreplace'):
						link = '<sup><a href="http://twitter.com/' + username + '/status/' + t.id_str + '" target="_blank">1</a></sup> '
						if h:
							haikus_attributed.append(h + link)
		else:
			counter = 1
			sub_result = []
			for s in substrings:			
				if len(s.replace('\n', ' ').strip()) > 5:
					for username, t_list in tweets.items():
						for t in t_list:
							filtered_tweet = ' '.join([word for word in t.text.split(' ') if not word.startswith('http') and not has_number(word) and not is_only_punc(word)])
							if s.replace('\n', ' ').strip().encode('ascii', 'xmlcharrefreplace') in filtered_tweet.encode('ascii', 'xmlcharrefreplace'):

								link = '<sup><a href="http://twitter.com/' + username + '/status/' + t.id_str + '" target="_blank">' + str(counter) + '</a></sup> '
								if s:
									sub_result.append(s + link)
								counter = counter + 1
			sub_results.append(sub_result)
								
	for result in sub_results:
		haikus_attributed.append(''.join(r for r in result))
 	
 	# save a permalink item for each haiku
 	for h in haikus_attributed:
		i = Item(user=user, item_type=Item.HAIKU, text=h)
		i.save()
		i.hash_code = hash_from_id(i.id)
		i.save()
		haiku_links[h] = i.hash_code
	
	# run the audio script for the tweets
 	p_audio = subprocess.Popen(['python2.7', '/home/bshepherd/webapps/slowdown_django/slowdown/audiotweets.py', '-o', '/home/bshepherd/webapps/slowdown_static/audio/tweets_audio.mp3', '-f', '/home/bshepherd/webapps/slowdown_django/slowdown/tweets_audio.txt'], stdout=subprocess.PIPE)
 	p_audio.communicate()

	# save a permalink item for the twitter podcast
 	i = Item(user=user, item_type=Item.PODCAST)
	i.save()
	i.hash_code = hash_from_id(i.id)
	try:
		os.rename('/home/bshepherd/webapps/slowdown_static/audio/tweets_audio.mp3', '/home/bshepherd/webapps/slowdown_static/audio/tweets_' + i.hash_code + '.mp3')
		i.audio = '/static/audio/tweets_' + i.hash_code + '.mp3'
		i.save()
	except Exception:
		error_code = 'TWEET AUDIO FAILED'
		print >> sys.stderr, user_profile.user.username +': Sending email, couldn\'t save Twitter audio'
		
	audio_links['twitter'] = i.hash_code
 	
 	# INSTAGRAM CONTENT (MASHUPS, PODCAST, RANDOM PHOTOS)
	
	if user_instagram:
		# connect to instagram api
		token_instagram = user_instagram.get().tokens
		api_instagram = InstagramAPI(access_token=token_instagram)

		# instagram audio input txt file
		f_audio_insta = open(os.path.join(BASE_DIR, 'insta_audio.txt'), 'w')
	
		# get photos and write captions to instagram audio input txt file
		for person in user_profile.instagrams.all():
			person_instagrams = []	
			try:
				uid = api_instagram.user_search(person.username)[0].id
				recent_media, next = api_instagram.user_recent_media(user_id=uid, count=INSTAGRAM_COUNT)
				f_audio_insta.write('\nSTARTING INSTAGRAM CAPTIONS FROM USERNAME, @' + person.username.encode('ascii', 'xmlcharrefreplace') + ':\n,')
				for media in recent_media:
					if media.created_time.replace(tzinfo=utc) >= user_profile.last_email_time:
						instagram_links[media.images['standard_resolution'].url] = media.link
						person_instagrams.append(media.images['standard_resolution'].url)
						if media.caption:
							f_audio_insta.write(media.caption.text.encode('ascii', 'xmlcharrefreplace') + ' ,STOP, \n')
				if len(person_instagrams) > 0:
					instagrams[person.username] = person_instagrams
			except Exception:
				print >> sys.stderr, user_profile.user.username +': Sending email, Instagram API error, couldn\'t fetch recent media'

		f_audio_insta.close()

		# get all tweets and photos, select randomly to create mashups
		if tweets.values() and instagrams.values():
			tweet_pool = [item for sublist in tweets.values() for item in sublist]
			instagram_pool = [item for sublist in instagrams.values() for item in sublist]
			if len(tweet_pool) < num_mashups:
				num_mashups = len(tweet_pool)
			if len(instagram_pool) < num_mashups:
				num_mashups = len(instagram_pool)
			tweets_random = random.sample(tweet_pool, num_mashups)
			instagrams_random = random.sample(instagram_pool, num_mashups)
			mashups = zip(tweets_random, instagrams_random)
	
		if mashups:
			# create permalink items for all mashups
			for mashup in mashups:
				image_link = instagram_links[mashup[1]]
				text_link = 'http://www.twitter.com/' + mashup[0].author.screen_name + '/status/' + mashup[0].id_str
				i = Item(user=user, item_type=Item.REMIX, image_url=mashup[1], image_link=image_link, text=mashup[0].text, text_link=text_link)
				i.save()
				i.hash_code = hash_from_id(i.id)
				i.save()
				mashup_links[mashup[1]] = i.hash_code
		
		# get random photos using user's lat and lon
		try:	
			media = api_instagram.media_search(count=9, lat=user_profile.lat, lng=user_profile.lon)
			for m in media:
				random_photos.append((m.images['standard_resolution'].url, m.link))
		except Exception:
			error_code = 'LAT LON SEARCH FAILED'
			print >> sys.stderr, user_profile.user.username +': Sending email, Instagram API error, lat lon search failed'
	 	
	 	# run the audio script for the instagram captions
		p_audio_insta = subprocess.Popen(['python2.7', '/home/bshepherd/webapps/slowdown_django/slowdown/audiotweets.py', '-o', '/home/bshepherd/webapps/slowdown_static/audio/instagramcaptions_audio.mp3', '-f', '/home/bshepherd/webapps/slowdown_django/slowdown/insta_audio.txt'], stdout=subprocess.PIPE)
		p_audio_insta.communicate()

		# create a permalink item for the instagram podcast
		i = Item(user=user, item_type=Item.PODCAST)
		i.save()
		i.hash_code = hash_from_id(i.id)
		try:
			os.rename('/home/bshepherd/webapps/slowdown_static/audio/instagramcaptions_audio.mp3', '/home/bshepherd/webapps/slowdown_static/audio/instagramcaptions_' + i.hash_code + '.mp3')
			i.audio = '/static/audio/instagramcaptions_' + i.hash_code + '.mp3'
			i.save()
		except Exception:
			error_code = 'INSTAGRAM AUDIO FAILED'
			print >> sys.stderr, user_profile.user.username +': Sending email, couldn\'t save Instagram audio'
		audio_links['instagram'] = i.hash_code
		
	# construct email content	
	html_content = render_to_string('email.html', {
		'user_profile' : user_profile,
		'tweets' : tweets,
		'instagrams' : instagrams,
		'instagram_links' : instagram_links,
		'mashups' : mashups,
		'mashup_links' : mashup_links,
		'haikus' : haikus_attributed,
		'haiku_links' : haiku_links,
		'random_photos' : random_photos,
		'audio_links' : audio_links,
	})
	
	all_tweets = [item for sublist in tweets.values() for item in sublist]
	all_photos = [item for sublist in instagrams.values() for item in sublist]

	# hash prevents emails from threading
	email_hash = hash_from_id(random.randint(0,100000))
	
	subject = user.first_name + ', It\'s Time to Slow Down!'
	
	# TODO: remove the BCC!
	msg = EmailMessage(subject, html_content, 'Slow Down Digest<no-reply+'+email_hash+'@slowdown.io>', [user.email], ['schmeenarf@gmail.com'])
	msg.content_subtype = "html"
	
	# attach twitter mp3 if it exists and has content
	if user_twitter and user_profile.podcasts and (len(all_tweets) > 0):
		audio_t = '/home/bshepherd/webapps/slowdown_static/audio/tweets_' + audio_links['twitter'] + '.mp3'
		try:
			msg.attach_file(audio_t)
		except Exception:
			print >> sys.stderr, user_profile.user.username +': Sending email, couldn\'t attach Twitter audio'
		
	# attach instagram mp3 if it exists and has content
	if user_instagram and user_profile.podcasts and (len(all_photos) > 0):
		audio_i = '/home/bshepherd/webapps/slowdown_static/audio/instagramcaptions_' + audio_links['instagram'] + '.mp3'
		try:
			msg.attach_file(audio_i)
		except Exception:
			print >> sys.stderr, user_profile.user.username +': Sending email, couldn\'t attach Instagram audio'
			
	msg.send()
	return error_code
	
def check_and_send_email(request):	
	if request.GET.get('secret') != 'vQbJbBwjQLkB':
		return HttpResponseForbidden()

	# get everyone whose next_email_time is less than the current time	
	all_users = UserProfile.objects.filter(next_email_time__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
	report = []
	for user_profile in all_users:
		print >> sys.stderr, user_profile.user.username +': TRYING TO SEND TO DIGEST'
		try:
			response = email_helper(user_profile.user)
			if response:
				print >> sys.stderr, user_profile.user.username +': SUCCESS'
				user_profile.last_email_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	
				# RECALCULATE NEXT TIME TO SEND EMAIL
				
				# weekly
				if user_profile.frequency == 1:
					days_delta = 7
					if user_profile.surprise_day:
						days_delta = random.randint(1,7)
					next_email_time = user_profile.next_email_time + timedelta(days=days_delta)
				# daily
				else:
					next_email_time = user_profile.next_email_time + timedelta(days=1)				
				if user_profile.surprise_time:
					# ADD UTC OFFSET
					next_email_time = next_email_time.replace(hour=random.randint(0,23), minute=0, second=0, microsecond=0) + timedelta(hours=user_profile.tz_offset)
				user_profile.next_email_time = next_email_time
				user_profile.save()
				
				report.append((user_profile.user.username, response))	
		except Exception as e:
			print >> sys.stderr, user_profile.user.username +': '+str(e)
				
	return HttpResponse(json.dumps(report),content_type='application/json')

@login_required
def edit_settings(request):
	user = get_object_or_404(User, username=request.user.username)
	user_profile = get_object_or_404(UserProfile, user=user)
	user_twitter = UserSocialAuth.objects.filter(user=user, provider='twitter')
	user_instagram = UserSocialAuth.objects.filter(user=user, provider='instagram')

	twitter_connected = False
	instagram_connected = False
	t_selected = ''
	i_selected = ''
	my_tweets = False
	my_photos = False
	local_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	
	if user_twitter:
		twitter_connected = True
		if 'twitter_list' not in request.session:
			# connect to twitter api
			oauth_access_token=(user_twitter.get().tokens).get('oauth_token')
			oauth_access_secret=(user_twitter.get().tokens).get('oauth_token_secret')
			auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
			auth.set_access_token(oauth_access_token, oauth_access_secret)
			api_twitter = tweepy.API(auth)	
			
			# get list of twitter friends
			request.session['twitter_list'] = []
			friends_ids = []
			try:
				friends_cursor = tweepy.Cursor(api_twitter.friends_ids,id=user_twitter.get().uid)
				for id in friends_cursor.items():
					friends_ids.append(id)
				for friends_page in paginate(friends_ids, 100):
					friends_objects = api_twitter.lookup_users(user_ids=friends_page)
					for friend in friends_objects:
						request.session['twitter_list'].append(friend.screen_name)
			except Exception:
				print >> sys.stderr, user_profile.user.username +': Editing settings, Twitter API error, tried to get friend list'
			
	if user_instagram:
		instagram_connected = True
		if 'instagram_list' not in request.session:
			# connect to instagram api
			token_instagram = user_instagram.get().tokens
			api_instagram = InstagramAPI(access_token=token_instagram)
			
			# get list of instagram friends
			request.session['instagram_list'] = []
			try:
				for page in api_instagram.user_follows(user_id=user_instagram.get().uid, as_generator=True, max_pages=15):
					for friend in page[0]:
						request.session['instagram_list'].append(friend.username)
			except Exception:
				print >> sys.stderr, user_profile.user.username +': Editing settings, Instagram API error, tried to get friend list'
	
	# construct string of currently subscribed to twitter users
	for t in user_profile.twitters.all():
		if t.uid and int(t.uid) == int(user_twitter.get().uid):
			my_tweets = True
		else:
			t_selected += t.username + ', '
	
	# construct string of currently subscribed to instagram users	
	for i in user_profile.instagrams.all():
		if i.uid and int(i.uid) == int(user_instagram.get().uid):
			my_photos = True
		else:
			i_selected += i.username + ', '

	# convert utc time to local time for rendering
	if user_profile.next_email_time:
		local_time = user_profile.next_email_time - timedelta(hours=user_profile.tz_offset)
		day_of_week = local_time.weekday()
		time_of_day = local_time.hour
	else:
		day_of_week = 0
		time_of_day = 9

	# render edit settings form
	return render_to_response('settings.html', {
   	 'user_profile' : user_profile,
   	 'instagram_connected' : instagram_connected,
   	 'twitter_connected' : twitter_connected,
	 'session' : request.session,
	 't_selected' : str(t_selected),
	 'i_selected' : str(i_selected),
	 'num_twitters_left' : 11 - len(user_profile.twitters.all()),
	 'num_instagrams_left' : 11 - len(user_profile.instagrams.all()),
	 'my_tweets' : my_tweets,
	 'my_photos' : my_photos,
	 'day_of_week' : day_of_week,
	 'time_of_day' : time_of_day,
	 'local_time' : local_time

	}, RequestContext(request))

# script to go through all twitter and instagram database objects and get their profile pics, saving in case I need it again 	
# def add_urls(request):
# 	user_twitter = UserSocialAuth.objects.filter(user=request.user, provider='twitter')
# 	user_instagram = UserSocialAuth.objects.filter(user=request.user, provider='instagram')
# 	
# 	oauth_access_token=(user_twitter.get().tokens).get('oauth_token')
# 	oauth_access_secret=(user_twitter.get().tokens).get('oauth_token_secret')
# 	auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
# 	auth.set_access_token(oauth_access_token, oauth_access_secret)
# 	api_twitter = tweepy.API(auth)
# 	
# 	token_instagram = user_instagram.get().tokens
# 	api_instagram = InstagramAPI(access_token=token_instagram)
# 	
# 	twitters = Twitter.objects.all()
# 	for t in twitters:
# 		t_user = api_twitter.get_user(screen_name=t.username)
# 		t.url = t_user.profile_image_url
# 		t.save()
# 	
# 	instagrams = Instagram.objects.all()
# 	for i in instagrams:
# 		i_user = api_instagram.user_search(i.username)[0]
# 		i.url = i_user.profile_picture
# 		i.save()
# 	return HttpResponseRedirect('/')