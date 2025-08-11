from django.db import models
from django.contrib.auth.models import AbstractUser
from jalali_date import datetime2jalali


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='موبایل')
    land_line = models.CharField(max_length=11, unique=True, verbose_name='تلفن ثابت', blank=True, null=True)
    DEGREE_CHOICES = [
        ('', ' -- مدرک تحصیلی  --'),
        ('دیپلم', 'دیپلم'),
        ('کارشناسی', 'کارشناسی'),
        ('کارشناسی ارشد', 'کارشناسی ارشد'),
        ('دکتری', 'دکتری')
    ]
    degree = models.CharField(max_length=200, choices=DEGREE_CHOICES, verbose_name='مدرک تحصیلی')
    field_of_study = models.CharField(max_length=200, verbose_name='رشته ی تحصیلی', blank=True, null=True)
    company = models.CharField(max_length=200, verbose_name='شرکت / سازمان', blank=True, null=True)
    province = models.CharField(max_length=200, verbose_name='استان')
    city = models.CharField(max_length=200, verbose_name='شهر')
    address = models.CharField(max_length=500, verbose_name='آدرس')
    postal_code = models.CharField(max_length=200, verbose_name='کد پستی')
    is_online = models.BooleanField(default=False)
    code_meli = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')

    ###   تبدیل تاریخ لاگین به شمسی ####
    def last_login_to_jalali(self):
        if self.last_login:
            jalali_last_login = datetime2jalali(self.last_login).strftime('%y/%m/%d _ %H:%M')
            return jalali_last_login
        else:
            return 'تاکنون وارد نشده'

    def paid_count(self):
        return self.article_set.filter(is_paid=True).count()

    def not_paid_count(self):
        return self.article_set.filter(is_paid=False).count()


    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'لیست کاربران'


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('open', 'باز'),
        ('pending', 'در حال بررسی'),
        ('closed', 'بسته شده'),
    )

    PRIORITY_CHOICES = (
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    )

    DEPARTMENT_CHOICES = (
        ('technical', 'پشتیبانی فنی'),
        ('financial', 'مالی و پرداخت‌ها'),
        ('content', 'محتوا و مقالات'),
        ('other', 'سایر موارد'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, verbose_name='دپارتمان',null=True,blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='اولویت',null=True,blank=True)
    message = models.TextField(verbose_name='پیام',null=True,blank=True)
    answer = models.TextField(verbose_name='جواب',null=True,blank=True)
    attachment = models.FileField(upload_to='tickets/attachments/', null=True, blank=True, verbose_name='پیوست')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"
