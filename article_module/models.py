from django.db import models

from account_module.models import User


# Create your models here.


class Article(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    authors_numbers = models.CharField(max_length=20, verbose_name='تعداد نویسندگان')
    authors_info = models.JSONField(null=True, blank=True, verbose_name='نویسندگان')
    main_goal = models.CharField(max_length=200, verbose_name='محور اصلی مقاله')
    language = models.CharField(max_length=100, verbose_name='زبان مقاله')
    persian_subject = models.TextField(verbose_name='عنوان فارسی مقاله')
    english_subject = models.TextField(verbose_name='عنوان انگلیسی مقاله')
    article_abstract = models.TextField(max_length=250, verbose_name='چکیده مقاله', blank=True, null=True)
    file = models.FileField(verbose_name='فایل مقاله', upload_to='articles/')
    certificate_file = models.FileField(verbose_name='فایل گواهی', upload_to='articles/certificate/', blank=True, null=True)
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت مقاله')
    is_visited = models.BooleanField(verbose_name='دیده شده توسط ادمین', default=False)
    is_coached = models.BooleanField(verbose_name='داوری شده', default=False)
    is_accepted = models.BooleanField(verbose_name='پذیرفته شده توسط داور', default=False)
    is_paid = models.BooleanField(verbose_name='هزینه داوری', default=False)
    send_to_pay = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(verbose_name='هزینه',max_length=50, blank=True, null=True,default=0)


    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.persian_subject





