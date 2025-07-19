from django.db import models


class Hamayesh_prices(models.Model):
    name = models.CharField(max_length=100,verbose_name='عنوان')
    price = models.IntegerField(verbose_name='هزینه')
    is_active = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = 'تعرفه های همایش'
        verbose_name = 'تعرفه همایش'

    def __str__(self):
        return self.name

