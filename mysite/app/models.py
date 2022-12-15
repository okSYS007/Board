
from django.db import models
#from django.contrib.auth.models import User
from users.models import MyUser
from django.urls import reverse

class Announcement(models.Model):
    
    Announcement_author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Creation_date = models.DateTimeField(auto_now_add=True)
    Announcement_title = models.CharField(max_length=255)
    Announcement_text = models.TextField(default='content')

    CHOICES = (
        ('Tank', 'Танки'),
        ('Heal', 'Хилы'),
        ('DD', 'ДД'),
        ('Sales', 'Торговецы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('BS', 'Кузнецы'),
        ('PS', 'Кожевники'),
        ('Potions', 'Зельевары'),
        ('Magic', 'Мастера заклинаний'),
    )

    Category = models.CharField(max_length=300, choices = CHOICES)

    def __str__(self):
        return '%s' % (self.Announcement_title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 

    def get_absolute_url(self):
        return reverse('announce', kwargs={'pk': self.pk})

class Files(models.Model):
    
    Announcement = models.ForeignKey(Announcement, on_delete = models.CASCADE)
    Name = models.CharField(default='file-name', max_length=255)
    File = models.FileField(upload_to='', blank = True, null=True)
    File_type = models.TextField(default='jpg')
    
    def save(self, *args, **kwargs):
        img_endding  = {'jpg', 'png', 'img'}
        self.Name = self.File.name
        check_img = {self.Name.split(".")[-1]}
        if check_img.intersection(img_endding):
            self.File_type = 'img'
        else:
            self.File_type = 'video'
        super().save(*args, **kwargs)

    def __str__(self):
        return  '%s' % str(self.Name)

class Comments(models.Model):

    Announcement = models.ForeignKey(Announcement, on_delete = models.CASCADE)
    User = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Comment = models.TextField(default='comment')
    Comment_date = models.DateTimeField(auto_now_add=True)
    Comment_accepted = models.BooleanField(default = False)

    def __str__(self) :
        return '%s' % str(self.Comment)

class OneTimeCode(models.Model):

    User = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Code = models.CharField(default="", max_length = 4)

    def __str__(self):
        return '%s %s' % (self.User, self.Code)

