from django.db import models

from service.models import Client, Mailing

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name="Контент")
    picture = models.ImageField(upload_to='blog/', **NULLABLE)
    is_active = models.BooleanField(default=True)
    number_of_views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    date_of_publication = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.SET_NULL, **NULLABLE, )
    mailing = models.ForeignKey(Mailing, verbose_name="Рассылки", on_delete=models.SET_NULL, **NULLABLE, )

    def __str__(self):
        return f'{self.title}, {self.number_of_views}, {self.date_of_publication}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'