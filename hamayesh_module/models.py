from django.db import models


class Hamayesh_prices(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    class Meta:
        verbose_name_plural = 'تعرفه های همایش'
        verbose_name = 'تعرفه همایش'

    def __str__(self):
        return self.name

class Hamayesh_topics(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()

    class Meta:
        verbose_name_plural = 'محور های همایش'
        verbose_name = 'محور همایش'

    def __str__(self):
        return self.name
