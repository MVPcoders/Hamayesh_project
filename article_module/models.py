from tabnanny import verbose

from django.db import models

# Create your models here.


class Article(models.Model):
    AUTHORS_CHOICES = [
        ('', '-- تعداد نویسندگان --'),
        ('1', 'یک'),
        ('2', 'دو'),
        ('3', 'سه'),
        ('4', 'چهار'),
    ]
    LANGUAGE_CHOICES = [
        ('persian', 'فارسی'),
        ('english', 'انگلیسی'),
    ]
    authors_numbers = models.CharField(max_length=20, choices=AUTHORS_CHOICES,verbose_name='تعداد نویسندگان')
    main_goal = models.CharField(max_length=200,verbose_name='محور اصلی مقاله')
    language = models.CharField(max_length=100,choices=LANGUAGE_CHOICES,verbose_name = 'زبان مقاله')
    persian_subject = models.TextField(verbose_name = 'عنوان فارسی مقاله')
    english_subject = models.TextField(verbose_name = 'عنوان انگلیسی مقاله')
    english_Abstract = models.TextField(max_length=250,verbose_name='چکیده انگلیسی')
    persian_Abstract = models.TextField(max_length=250,verbose_name='چکیده فارسی')
    main_persian_words = models.TextField(verbose_name='کلمات کلیدی فارسی')
    main_english_words = models.TextField(verbose_name='کلمات کلیدی انگلیسی')
    sources = models.TextField(verbose_name='منابع')
    file = models.FileField(verbose_name='فایل مقاله', upload_to='articles/')
    submit_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت مقاله' )
    is_visited = models.BooleanField(verbose_name='دیده شده توسط ادمین', default=False)
    is_coached = models.BooleanField(verbose_name='داوری شده', default=False)
    is_accepted = models.BooleanField(verbose_name='پذیرفته شده توسط داور', default=False)
    is_paid = models.BooleanField(verbose_name='هزینه داوری', default=False)


    def __str__(self):
        return self.persian_subject



    class Meta:
        verbose_name='مقاله'
        verbose_name_plural='مقالات'


class ArticleAuthor(models.Model):
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, verbose_name='مقاله')
    first_name = models.CharField(max_length=200, verbose_name='نام نویسنده')
    last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی نویسنده')
    english_first_name = models.CharField(max_length=200, verbose_name='نام انگلیسی نویسنده')
    english_last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی انگلیسی نویسنده')
    email = models.EmailField( verbose_name='ایمیل نویسنده')
    main_author = models.BooleanField(default=False,verbose_name = 'نویسنده مسئول')


    def __str__(self):
        if self.main_author:
            return f'{self.first_name} {self.last_name}  - {self.article}'

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'


class ArticleCertificate(models.Model):
    article = models.ForeignKey(to = Article, on_delete=models.SET_NULL,null=True,verbose_name='مقاله')
    authors = models.ForeignKey(to = ArticleAuthor, on_delete=models.SET_NULL,null=True, verbose_name = 'نویسندگان')
    certificate_url = models.CharField(verbose_name='آدرس تقدیر نامه', max_length=300, default="")
    image = models.ImageField(upload_to='certificates/', verbose_name='عکس تقدیر نامه')
    cer_id = models.CharField(max_length=16, verbose_name='شماره گواهی ', unique=True)
    certificate_date = models.DateTimeField(auto_now_add=True, editable=False,verbose_name='تاریخ اعطا')


    def __str__(self):
        return self.article.persian_subject


    class Meta:
        verbose_name = 'گواهی مقاله'
        verbose_name_plural = 'گواهی های مقالات'




