from django.db import models
class User(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    def __unicode__(self):
     return self.username
class Status(models.Model):
    account=models.ForeignKey(User)
    status=models.CharField(max_length=1000)
    pub_date=models.DateTimeField('date published')
    def __unicode__(self):
     return self.status
class Friends(models.Model):
    account=models.ForeignKey(User)
    friend_id=models.IntegerField()
    def __unicode__(self):
     return self.friend_id
class Messages(models.Model):
    account=models.ForeignKey(User)
    message=models.CharField(max_length=1000)
    pub_date=models.DateTimeField('date published')
    friend_id=models.IntegerField()
    def __unicode__(self):
     return self.message
