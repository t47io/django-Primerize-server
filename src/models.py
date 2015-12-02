from django.db import models
from django import forms
from django.utils.html import format_html

from src.settings import *

# import os

JOB_TYPE_CHOICES = (
    ('1', 'Simple Assembly'),
    ('2', 'Mutate-and-Map'),
    ('3', 'Mutation/Rescue'),
)

JOB_STATUS_CHOICES = (
    ('0', 'Demo'),
    ('1', 'Underway'),
    ('2', 'Success'),
    ('3', 'Fail'),
    ('4', 'Error'),
)


class Design1D(models.Model):
    date = models.DateField(verbose_name='Submission Date')
    job_id = models.CharField(primary_key=True, blank=False, unique=True, max_length=16, verbose_name='Job ID', help_text='<span class="glyphicon glyphicon-credit-card"></span>&nbsp;Unique 16-digit hexadecimal <span class="label label-violet">JOB_ID</span>.')
    sequence = models.TextField(blank=False)
    tag = models.CharField(blank=True, max_length=31, help_text='<span class="glyphicon glyphicon-tag"></span>&nbsp;Prefix/name for sequence.')
    params = models.TextField(blank=True, verbose_name='Optional Parameters', help_text='<span class="glyphicon glyphicon-file"></span>&nbsp;Serialized JSON of optional parameters.')
    primers = models.TextField(blank=True, verbose_name='Primer Set', help_text='<span class="glyphicon glyphicon-list-alt"></span>&nbsp;Serialized array of result design.')
    time = models.FloatField(blank=True, verbose_name='Time Elapsed', help_text='<span class="glyphicon glyphicon-time"></span>&nbsp;Unit of <span class="label label-inverse">seconds</span>.')
    status = models.CharField(blank=False, max_length=1, choices=JOB_STATUS_CHOICES, verbose_name='Status')

    class Meta():
        verbose_name = 'Simple Assembly Design'
        verbose_name_plural = 'Simple Assembly Designs'

    def __unicode__(self):
        return u'%s' % self.job_id


class Design2D(models.Model):
    date = models.DateField(verbose_name='Submission Date')
    job_id = models.CharField(primary_key=True, blank=False, unique=True, max_length=16, verbose_name='Job ID')
    sequence = models.TextField(blank=False)
    tag = models.CharField(blank=True, max_length=31)
    params = models.TextField(blank=True, verbose_name='Optional Parameters')

    time = models.FloatField(blank=True, verbose_name='Time Elapsed')
    status = models.CharField(blank=False, max_length=15, verbose_name='Status')

    class Meta():
        verbose_name = 'Mutate-and-Map Design'
        verbose_name_plural = 'Mutate-and-Map Designs'

    def __unicode__(self):
        return u'%s' % self.job_id


class Design3D(models.Model):
    date = models.DateField(verbose_name='Submission Date')
    job_id = models.CharField(primary_key=True, blank=False, unique=True, max_length=16, verbose_name='Job ID')
    sequence = models.TextField(blank=False)
    tag = models.CharField(blank=True, max_length=31)
    params = models.TextField(blank=True, verbose_name='Optional Parameters')

    time = models.FloatField(blank=True, verbose_name='Time Elapsed')
    status = models.CharField(blank=False, max_length=15, verbose_name='Status')

    class Meta():
        verbose_name = 'Mutation/Rescue Design'
        verbose_name_plural = 'Mutation/Rescue Designs'

    def __unicode__(self):
        return u'%s' % self.job_id


class JobIDs(models.Model):
    job_id = models.CharField(primary_key=True, blank=False, unique=True, max_length=16, verbose_name='Job ID', help_text='<span class="glyphicon glyphicon-credit-card"></span>&nbsp;Unique 16-digit hexadecimal <span class="label label-violet">JOB_ID</span>.')
    type = models.CharField(blank=False, max_length=1, choices=JOB_TYPE_CHOICES, verbose_name='Job Type')
    date = models.DateField(verbose_name='Submission Date')

    class Meta():
        verbose_name = 'Job ID'
        verbose_name_plural = 'Job IDs'


class JobGroups(models.Model):
    sequence = models.TextField(blank=False)
    tag = models.CharField(blank=True, max_length=31, help_text='<span class="glyphicon glyphicon-tag"></span>&nbsp;Prefix/name for sequence.')
    job_1d = models.OneToOneField(Design1D, null=True, blank=True, verbose_name='Job entry of Design1D', help_text='<span class="glyphicon glyphicon-credit-card"></span>&nbsp;Unique 16-digit hexadecimal <span class="label label-violet">JOB_ID</span>.')
    job_2d = models.OneToOneField(Design2D, null=True, blank=True, verbose_name='Job ID of Design2D', help_text='<span class="glyphicon glyphicon-credit-card"></span>&nbsp;Unique 16-digit hexadecimal <span class="label label-violet">JOB_ID</span>.')
    job_3d = models.OneToOneField(Design3D, null=True, blank=True, verbose_name='Job ID of Design3D', help_text='<span class="glyphicon glyphicon-credit-card"></span>&nbsp;Unique 16-digit hexadecimal <span class="label label-violet">JOB_ID</span>.')

    class Meta():
        verbose_name = 'Job Group'
        verbose_name_plural = 'Job Groups'


class HistoryItem(models.Model):
    date = models.DateField(verbose_name='Display Date')
    content_html = models.TextField(blank=False, verbose_name='HTML Content', help_text='<span class="glyphicon glyphicon-edit"></span>&nbsp;HTML supported.')

    class Meta():
        verbose_name = 'History Item'
        verbose_name_plural = 'History Items'


class SourceDownloader(models.Model):
    date = models.DateField(verbose_name='Request Date')
    first_name = models.CharField(blank=False, max_length=31, verbose_name='First Name')
    last_name = models.CharField(blank=False, max_length=31, verbose_name='Last Name')
    institution = models.CharField(blank=False, max_length=31)
    department = models.CharField(blank=False, max_length=31)
    email = models.EmailField(blank=False, max_length=255)
    is_subscribe = models.BooleanField(default=True, verbose_name='Subscription Status', help_text='<span class="glyphicon glyphicon-check"></span>&nbsp; Check for subscription.')

    class Meta():
        verbose_name = 'Source Downloader'
        verbose_name_plural = 'Source Downloaders'

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'

    def affiliation(self):
        return '%s @ %s' % (self.department, self.institution)
    affiliation.admin_order_field = 'institution'


########################################

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    flag = forms.CharField(required=True)

class PasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password_old = forms.CharField(required=True, widget=forms.PasswordInput)
    password_new = forms.CharField(required=True, widget=forms.PasswordInput)
    password_new_rep = forms.CharField(required=True, widget=forms.PasswordInput)


class Design1DForm(forms.Form):
    sequence = forms.CharField(widget=forms.Textarea, required=True)
    tag = forms.CharField(required=False)
    min_Tm = forms.FloatField(required=False, min_value=10.0, max_value=100.0, initial=60.0)
    max_len = forms.IntegerField(required=False, min_value=60, initial=60)
    min_len = forms.IntegerField(required=False, min_value=0, initial=15)
    num_primers = forms.IntegerField(required=False, min_value=0, initial=0)
    is_num_primers = forms.BooleanField(required=False, initial=False)
    is_check_t7 = forms.BooleanField(required=False, initial=True)

class DownloadForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    institution = forms.CharField(required=True)
    department = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    is_subscribe = forms.BooleanField(initial=True, required=False)


########################################


WEEKDAY_CHOICES = (
    ('0', 'Sunday'),
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
)

class BackupForm(forms.Form):
    # is_backup = forms.BooleanField()
    # is_upload = forms.BooleanField()
    time_backup = forms.TimeField(required=True)
    time_upload = forms.TimeField(required=True)
    day_backup = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    day_upload = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    keep_backup = forms.IntegerField()
    keep_job = forms.IntegerField()


def debug_flag(request):
    if DEBUG:
        return {'DEBUG_STR': '', 'DEBUG_DIR': ''}
    else:
        return {'DEBUG_STR': '.min', 'DEBUG_DIR': 'min/'}

def ga_tracker(request):
    return {'TRACKING_ID': GA['TRACKING_ID']}