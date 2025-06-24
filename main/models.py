from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length= 60)
    image = models.ImageField(upload_to='media/', blank=True,null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    # add 'admin' in default value  if you add new field 

def __str__(self):
    return self.title

