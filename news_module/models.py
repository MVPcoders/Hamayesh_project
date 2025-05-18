from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان خبر')
    content = models.TextField(verbose_name='متن خبر')
    image = models.ImageField(null=True,blank=True,verbose_name='عکس')
    date = models.DateField(verbose_name='تاریخ')

    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'
        ordering = ['-date']

    def __str__(self):
        return self.title
