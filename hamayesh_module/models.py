from django.db import models


class Hamayesh_prices(models.Model):
    name = models.CharField(max_length=100,verbose_name='عنوان')
    price = models.IntegerField(verbose_name='هزینه')

    class Meta:
        verbose_name_plural = 'تعرفه های همایش'
        verbose_name = 'تعرفه همایش'

    def __str__(self):
        return self.name

class Hamayesh_topics(models.Model):
    name = models.CharField(max_length=100, verbose_name='عنوان محور')
    details = models.TextField(verbose_name='جزئیات محور')

    class Meta:
        verbose_name_plural = 'محور های همایش'
        verbose_name = 'محور همایش'

    def __str__(self):
        return self.name



class Hamayesh_signup_categories(models.Model):
    name = models.CharField(max_length=100, verbose_name='عنوان')
    price = models.IntegerField(verbose_name='هزینه')

    class Meta:
        verbose_name_plural = 'انواع ثبت نام همایش'
        verbose_name = 'نوع ثبت نام همایش'

    def __str__(self):
        return self.name