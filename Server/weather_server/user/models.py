from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20,verbose_name="用户")
    email = models.EmailField(verbose_name="邮箱")
    password_1 = models.CharField(max_length=20,verbose_name="密码1")
    password_2 = models.CharField(max_length=20, verbose_name="密码2")

    class Meta():
        db_table = 'user'