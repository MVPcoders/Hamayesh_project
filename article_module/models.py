from django.db import models
from django.urls import reverse

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
    article_abstract = models.TextField( verbose_name='چکیده مقاله', blank=True, null=True)
    file = models.FileField(verbose_name='فایل مقاله', upload_to='articles/')
    certificate_file = models.FileField(verbose_name='لوح تقدیر', upload_to='articles/certificate/', blank=True, null=True)
    paziresh_file= models.FileField(verbose_name='لوح پذیرش', upload_to='articles/paziresh/', blank=True, null=True)
    kargah_file = models.FileField(verbose_name='لوح حضور کارگاه', upload_to='articles/kargah/', blank=True, null=True)
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت مقاله')
    is_visited = models.BooleanField(verbose_name='دیده شده توسط ادمین', default=False)
    is_coached = models.BooleanField(verbose_name='داوری شده', default=False)
    is_accepted = models.BooleanField(verbose_name='پذیرفته شده توسط داور', default=False)
    need_correction = models.BooleanField(verbose_name="نیاز به اصلاح", default=False)
    correction_text = models.TextField(verbose_name="متن اصلاحیه", null=True, blank=True )
    is_corrected = models.BooleanField(verbose_name="اصلاح شده توسط کابر", default=False,editable=False, blank=True, null=True)
    is_paid = models.BooleanField(verbose_name='هزینه داوری', default=False)
    send_to_pay = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(verbose_name='هزینه',max_length=50, blank=True, null=True,default=0)
    qr_code = models.ImageField(upload_to="article_qrcodes/", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("article_detail", args=[str(self.id)])
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.persian_subject

    def save(self, *args, **kwargs):
        if  self.need_correction :
            self.is_corrected=False
        super(Article, self).save(*args, **kwargs)






