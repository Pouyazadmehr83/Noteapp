# Create your models here.


from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notes')
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title,self.content}"

