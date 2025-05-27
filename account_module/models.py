from django.db import models
from django.contrib.auth.models import AbstractUser
from jalali_date import datetime2jalali
# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='موبایل')
    land_line = models.CharField(max_length=11,unique=True, verbose_name='تلفن ثابت', blank=True, null=True)
    DEGREE_CHOICES = [
        ('',' -- مدرک تحصیلی  --'),
        ('دیپلم','دیپلم'),
        ('کارشناسی','کارشناسی'),
        ('کارشناسی ارشد','کارشناسی ارشد'),
        ('دکتری','دکتری')
    ]
    degree = models.CharField(max_length=200,choices=DEGREE_CHOICES ,verbose_name='مدرک تحصیلی')
    field_of_study = models.CharField(max_length=200, verbose_name='رشته ی تحصیلی', blank=True, null=True)
    company = models.CharField(max_length=200, verbose_name='شرکت / سازمان', blank=True, null=True)
    province = models.CharField(max_length=200, verbose_name='استان')
    city = models.CharField(max_length=200, verbose_name='شهر')
    address = models.CharField(max_length=500, verbose_name='آدرس')
    postal_code = models.CharField(max_length=200, verbose_name='کد پستی')
    KIND_OF_SIGNUP_CHOICES = [
        ('','--نوع ثبت نام--'),
        ('دانشجویی','دانشجویی'),
        ('استاد دانشگاه','استاد دانشگاه'),
    ]
    kind_of_signup = models.CharField(max_length=300,choices=KIND_OF_SIGNUP_CHOICES, verbose_name='نوع ثبت نام')
    is_online = models.BooleanField(default=False)
    code_meli = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')

    ###   تبدیل تاریخ لاگین به شمسی ####
    def last_login_to_jalali(self):
        if self.last_login:
            jalali_last_login = datetime2jalali(self.last_login).strftime('%y/%m/%d _ %H:%M')
            return jalali_last_login
        else:
            return 'تاکنون وارد نشده'


    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'لیست کاربران'