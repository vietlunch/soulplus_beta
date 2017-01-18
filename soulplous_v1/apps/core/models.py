from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos

from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe 
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

@python_2_unicode_compatible
class UserProfile(models.Model):
    """UserProfiles extend the default Django User models.
    Info that is custom to our app is added here.  Users are primarily used for
    auth, while everything else uses UserProfiles.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=20,null=True)
    fullname = models.CharField(max_length=50,null=True,blank=True,verbose_name='fullname')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='users/avatars', default='users/avatars/noimage.png', max_length=255)
    avatar_thumbnail = ImageSpecField(source='avatar',processors=[ResizeToFill(60, 60)],format='JPEG',options={'quality': 60})
    createdDate = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    birthday = models.DateTimeField(null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='friends')
    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"
    def __str__(self):
        return self.occupation 

class Like(models.Model):
    userid = models.IntegerField()
    actionid = models.IntegerField()
    mapactionid = models.IntegerField()
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        
class Report(models.Model):
    userid = models.IntegerField()
    actionid = models.IntegerField()
    TYPES = (('I', 'Invalid'), ('T', 'Bad_Title'), ('C', 'Copyright'))
    report_type = models.CharField(max_length=1,choices = TYPES)
    content = models.TextField(max_length=1000,null=True,blank=False,verbose_name='Details')
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        
class ActionImage():
    image = models.ImageField(upload_to='action/imagealbums',null=True, blank=True)
    actionid = models.IntegerField('Action',null=True, blank=True)
    mapactionid = models.IntegerField('Action',null=True, blank=True)
    class Meta:
        verbose_name = "MapAction"
        verbose_name_plural = "MapActions"
        
@python_2_unicode_compatible
class Action(models.Model):
    title = models.CharField(max_length=1024, null=True, blank=False,verbose_name=u'Title')
    firstPicture = models.ImageField(upload_to='action/images', blank=True)
    content = models.TextField(max_length=30000,null=True,blank=False,verbose_name='Details')
    createDate = models.DateTimeField(auto_now_add=True,verbose_name='CreatedDate',null=True)
    startDate = models.DateTimeField(null=True, blank=True,verbose_name='StartDate')
    endDate = models.DateTimeField(null=True, blank=True,verbose_name='EndDate')
    modified =  models.DateTimeField(auto_now=True,verbose_name='timeUpdated',null=True)
    #imageurl = u'<img src="%s" />' % (self.firstPicture.url)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True, related_name='author')
    isverified = models.BooleanField(verbose_name='isverified',default=False)
    isactive = models.BooleanField(verbose_name='isActive',default=True)
    #lat = models.FloatField(null=True, blank=True)
    #long = models.FloatField(null=True, blank=True)
    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"
    def __str__(self):
        return self.title

    def showimage(self):
        if self.firstPicture:
            return mark_safe('<img src="%s" width="480" height="480"/>' % (self.firstPicture.url))
        else:
            return 'no image'
    showimage.short_decription = 'imagedisplay'

@python_2_unicode_compatible
class MapAction(models.Model):
    userid = models.IntegerField(null=True,blank=True)
    title = models.CharField(max_length=1024, null=True, blank=False,verbose_name=u'Title')
    firstPicture = models.ImageField(upload_to='mapaction/images', blank=True, default='users/avatars/noimage.png')
    content = models.TextField(max_length=30000,null=True,blank=False,verbose_name='Details')
    createDate = models.DateTimeField(auto_now_add=True,verbose_name='CreatedDate',null=True)
    timefromuser = models.DateTimeField(null=True, blank=True,verbose_name='StartDate')
    modified =  models.DateTimeField(auto_now=True,verbose_name='timeUpdated',null=True)
    #imageurl = u'<img src="%s" />' % (self.firstPicture.url)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True, related_name='author')
    isverified = models.BooleanField(verbose_name='isverified',default=False)
    isactive = models.BooleanField(verbose_name='isActive',default=True)
    location = gis_models.PointField(u"longitude/latitude",geography=True, blank=True, null=True)
    
    gis = gis_models.GeoManager()
    objects = models.Manager()
    #lat = models.FloatField(null=True, blank=True)
    #long = models.FloatField(null=True, blank=True)
    class Meta:
        verbose_name = "MapAction"
        verbose_name_plural = "MapActions"
    def __str__(self):
        return self.title

    def showimage(self):
        if self.firstPicture:
            return mark_safe('<img src="%s" width="480" height="480"/>' % (self.firstPicture.url))
        else:
            return 'no image'
    showimage.short_decription = 'imagedisplay'

    
class FriendRequest(models.Model):
    friendid = models.IntegerField()
    userid = models.IntegerField()
    class Meta:
        verbose_name = "FriendRequest"
        verbose_name_plural = "FriendRequests"

class Rating(models.Model):
    actionid = models.IntegerField()
    userid = models.IntegerField()
    rating = models.IntegerField(null=True,blank=True)
    class Meta:
        verbose_name = "Friend"
        verbose_name_plural = "Friends"
    

class CalendarAction(models.Model):
    actionid = models.IntegerField()
    userid = models.IntegerField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(null=True,blank=True)
    class Meta:
        verbose_name = "CalendarAction"
        verbose_name_plural = "CalendarActions"

class PrivateGroup(models.Model):
    userid = models.IntegerField(null=True,blank=True)
    actionid = models.IntegerField(null=True,blank=True)
    members = models.ManyToManyField('UserProfile', related_name='members')
    class Meta:
        verbose_name = "PrivateGroup"
        verbose_name_plural = "PrivateGroup"
    

class ActionPicture(models.Model):
    picture =           models.ImageField(upload_to='action/images', blank=True)
    actionid =            models.ForeignKey('Action')
    class Meta:
        verbose_name = "ActionPicture"
        verbose_name_plural = "ActionPictures"

   
@python_2_unicode_compatible
class ActionRefLink(models.Model):
    link = models.TextField(max_length=1000)
    actionid = models.ForeignKey('Action')
    class Meta:
        verbose_name = "ActionRefLink"
        verbose_name_plural = "ActionRefLinks"

    def __str__(self):
        return self.link
    
@python_2_unicode_compatible   
class  Note(models.Model):
    userid =  models.IntegerField(null=False,blank=False)
    actionid =  models.IntegerField(null=False, blank=False)
    content   =  models.TextField(max_length=2000)
    #childcomment = models.ManyToManyField('self')
    createDate = models.DateTimeField(auto_now_add=True,verbose_name='CreatedDate')
    modified =          models.DateTimeField(auto_now=True,verbose_name='timeUdated')
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
    def __str__(self):
        return self.content

@python_2_unicode_compatible
class  Comment(models.Model):
    commentby =  models.ForeignKey('UserProfile')
    commentin =  models.ForeignKey('PrivateGroup')
    content   =  models.TextField(max_length=2000)
    childcomment = models.ManyToManyField('self')
    createDate = models.DateTimeField(auto_now_add=True,verbose_name='CreatedDate')
    modified =          models.DateTimeField(auto_now=True,verbose_name='timeUdated')
    active = models.BooleanField()
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
    def __str__(self):
        return self.content

   # showimage.allow_tags = True
@python_2_unicode_compatible
class Invitation(models.Model):
    fromuser = models.IntegerField(null=True, blank=True)
    touser =  models.IntegerField(null=True, blank=True)
    actionid = models.IntegerField(null=True, blank=True)
    content = models.TextField(max_length=2000)
    isaccept = models.BooleanField()
    createDate = models.DateTimeField(auto_now_add=True,verbose_name='createdate')
    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
    def __str__(self):
        return self.content

@python_2_unicode_compatible
class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
        )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity_type


@python_2_unicode_compatible
class Notification(models.Model):
    LIKED = 'L'
    COMMENTED_IN = 'C'
    FRIEND_REQUESTED = 'F'
    FRIEND_CREATE_MAP_ACTION = 'M'
    ACCEPTED_INVITATION = 'A'
    ACTION_DEADLINE = 'D'
    ACTION_CLOSED = 'F'
    REPLY_COMMENT = 'R'
    RECEIVED_INVITATION = 'I'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED_IN, 'Commented'),
        (FRIEND_REQUESTED, 'FriendRequest'),
        (RECEIVED_INVITATION, 'Invitation'),
        (FRIEND_CREATE_MAP_ACTION , 'FriendCreateMapAction')
        (ACCEPTED_INVITATION, 'Accepted'),
        (ACTION_DEADLINE, 'Deadlined'),
        (ACTION_CLOSED, 'ClosedAction'),
        (REPLY_COMMENT, 'ReplyComment'),
        )
    userid = models.IntegerField(null=True, blank=True)
    friend_like_id = models.IntegerField(null=True, blank=True)
    friend_create_map_id = models.IntegerField(null=True, blank=True)
    actionmapid = models.IntegerField(null=True, blank=True)
    #invitation_from_id = models.IntegerField(null=True, blank=True)
    user_comment_id = models.IntegerField(null=True, blank=True)
    actionlikedid = models.IntegerField(null=True, blank=True)
    calendaractionid = models.IntegerField(null=True, blank=True)
    Invitationid = models.IntegerField(null=True, blank=True)
    privateGroupid = models.IntegerField(null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    notificationtype = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    comment = models.ForeignKey('Comment',null=True, blank=True)
    isread = models.BooleanField(default=False)
    invitation = models.ForeignKey('Invitation',null=True, blank=True)
    friendrequest = models.ForeignKey('FriendRequest',null=True, blank=True)
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-createdDate',)
    def __str__(self):
        return self.notificationtype
"""
    _LIKED_TEMPLATE = '<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _FAVORITED_TEMPLATE = '<a href="/{0}/">{1}</a> favorited your question: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _ANSWERED_TEMPLATE = '<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _ACCEPTED_ANSWER_TEMPLATE = '<a href="/{0}/">{1}</a> accepted your answer: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _EDITED_ARTICLE_TEMPLATE = '<a href="/{0}/">{1}</a> edited your article: <a href="/article/{2}/">{3}</a>'  # noqa: E501
    _ALSO_COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
"""
