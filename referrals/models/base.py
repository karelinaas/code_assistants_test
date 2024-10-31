from django.db import models


class TimeStampAbstract(models.Model):
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        abstract = True


class DeactivateAbstract(models.Model):
    is_deactivated = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deactivated = True
        self.save()

    class Meta:
        abstract = True
