from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404

from django.db import models
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth


import tweepy
import datetime
from django.utils.timezone import utc

SOCIAL_AUTH_TWITTER_KEY = 'iOPlmeF3uXxJdNvttvYWA'
SOCIAL_AUTH_TWITTER_SECRET = 'RkRkkTImAHaH247fj2s4VTIftdv3odYJ6c5Tu2Y'

class Twitter(models.Model):
	username = models.CharField(max_length=20)
	uid = models.IntegerField(null=True, blank=True)
	url = models.CharField(max_length=300, null=True, blank=True)
	
	def __unicode__(self):
		return self.username
	
class Instagram(models.Model):
	username = models.CharField(max_length=30)
	uid = models.IntegerField(null=True, blank=True)
	url = models.CharField(max_length=300, null=True, blank=True)
	
	def __unicode__(self):
		return self.username
		
class UserProfile(models.Model):
	user = models.OneToOneField(User, blank=True, null=True)
	frequency = models.IntegerField(null=True, blank=True)
	next_email_time = models.DateTimeField(null=True, blank=True)
	last_email_time = models.DateTimeField(null=True, blank=True)
	surprise_day = models.BooleanField(default=False)
	surprise_time = models.BooleanField(default=False)
	lat = models.FloatField(null=True, blank=True)
	lon = models.FloatField(null=True, blank=True)
	tz_offset = models.IntegerField(null=True, blank=True)

	twitters = models.ManyToManyField(Twitter, null=True, blank=True)
	instagrams = models.ManyToManyField(Instagram, null=True, blank=True)
	
	remixing = models.BooleanField(default=True)
	zen = models.BooleanField(default=True)
	podcasts = models.BooleanField(default=True)
	voyeurism = models.BooleanField(default=True)
	appendix_t = models.BooleanField(default=True)
	appendix_i = models.BooleanField(default=True)
	
	def __unicode__(self):
		return self.user.username

class Item(models.Model):
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	
	REMIX = 'RM'
	HAIKU = 'HU'
	PODCAST = 'PD'
	TYPE_CHOICES = (
		(REMIX, 'Remixing the Stream'),
		(HAIKU, 'Zen Twitter'),
		(PODCAST, 'Social Podcasts'),
	)
	item_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=REMIX)
	
	image_url = models.CharField(max_length=300, blank=True, null=True)
	image_link = models.CharField(max_length=300, blank=True, null=True)
	
	text = models.CharField(max_length=1000, blank=True, null=True)
	text_link = models.CharField(max_length=300, blank=True, null=True)
	
	audio = models.FileField(upload_to='audio/%Y/%m/%d', blank=True, null=True)
	
	hash_code = models.CharField(max_length=11, blank=True, null=True)
	
	def __unicode__(self):
		return self.user.username + ': item ' + str(self.id)
		
	@models.permalink
	def get_absolute_url(self):
		return ('accounts.views.item_permalink', [str(self.id)])
	
def social_auth_to_profile(backend, details, response, user=None, is_new=False, *args, **kwargs):
	profile, created = UserProfile.objects.get_or_create(user=user)
	if created:
		profile.last_email_time = datetime.datetime.min.replace(tzinfo=utc)
		profile.save()