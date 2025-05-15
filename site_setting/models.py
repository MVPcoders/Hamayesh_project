from django.db import models

# Create your models here.
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200,verbose_name='اسم سایت')
    site_url = models.CharField(max_length=200,verbose_name="ادرس سایت")
    address = models.CharField(max_length=200,verbose_name="آدرس")
    phone_number = models.CharField(max_length=200,verbose_name="تلفن",null=True,blank=True)
    email = models.CharField(max_length=200,verbose_name="ایمیل",null=True,blank=True)
    copyright = models.TextField(verbose_name="متن کپی رایت")
    logo = models.ImageField(upload_to="upload/images/site_module/logo/",verbose_name="لوگو سایت",null=True,blank=True)
    about_us_text = models.TextField(verbose_name="متن درباره ما")
    #بخش مربوط به همایش
    poster = models.ImageField(upload_to='upload/images/site_module/poster/',verbose_name="پوستر همایش",null=True,blank=True)
    hamayesh_title = models.CharField(max_length=200,verbose_name='عنوان همایش',null=True,blank=True)
    hamayesh_detail = models.CharField(max_length=200,verbose_name='جزئیات همایش',null=True,blank=True)

    is_main_setting = models.BooleanField(default=False,verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name
