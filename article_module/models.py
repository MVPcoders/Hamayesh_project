from django.db import models

from account_module.models import User


# Create your models here.


class Article(models.Model):

    user = models.ForeignKey(to = User, on_delete=models.CASCADE, verbose_name='کاربر',blank=True, null=True)
    authors_numbers = models.CharField(max_length=20, verbose_name='تعداد نویسندگان')
    authors_info = models.JSONField(null=True, blank=True, verbose_name='نویسندگان')
    main_goal = models.CharField(max_length=200, verbose_name='محور اصلی مقاله')
    language = models.CharField(max_length=100, verbose_name='زبان مقاله')
    persian_subject = models.TextField(verbose_name='عنوان فارسی مقاله')
    english_subject = models.TextField(verbose_name='عنوان انگلیسی مقاله')
    article_abstract = models.TextField(max_length=250, verbose_name='چکیده مقاله', blank=True, null=True)
    file = models.FileField(verbose_name='فایل مقاله', upload_to='articles/')
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت مقاله')
    is_visited = models.BooleanField(verbose_name='دیده شده توسط ادمین', default=False)
    is_coached = models.BooleanField(verbose_name='داوری شده', default=False)
    is_accepted = models.BooleanField(verbose_name='پذیرفته شده توسط داور', default=False)
    is_paid = models.BooleanField(verbose_name='هزینه داوری', default=False)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.persian_subject



class ArticleCertificate(models.Model):
    # دسترسی به کاربر از طریق آرتیکل ممکن است
    article = models.ForeignKey(to=Article, on_delete=models.SET_NULL, null=True, verbose_name='مقاله')
    certificate_url = models.CharField(verbose_name='آدرس تقدیر نامه', max_length=300, default="")
    image = models.ImageField(upload_to='certificates/', verbose_name='عکس تقدیر نامه')
    cer_id = models.CharField(max_length=16, verbose_name='شماره گواهی ', unique=True)
    certificate_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ اعطا')

    def __str__(self):
        return self.article.persian_subject

    class Meta:
        verbose_name = 'گواهی مقاله'
        verbose_name_plural = 'گواهی های مقالات'





##  کد های کامنت شده

# class ArticleAuthor(models.Model):
#     article = models.ForeignKey(to='Article', on_delete=models.CASCADE, verbose_name='مقاله')
#     first_name = models.CharField(max_length=200, verbose_name='نام نویسنده')
#     last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی نویسنده')
#     english_first_name = models.CharField(max_length=200, verbose_name='نام انگلیسی نویسنده')
#     english_last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی انگلیسی نویسنده')
#     email = models.EmailField(verbose_name='ایمیل نویسنده')
#     main_author = models.BooleanField(default=False, verbose_name='نویسنده مسئول')
#
#     def __str__(self):
#         if self.main_author:
#             return f'{self.first_name} {self.last_name}'
#
#     class Meta:
#         verbose_name = 'نویسنده'
#         verbose_name_plural = 'نویسندگان'
