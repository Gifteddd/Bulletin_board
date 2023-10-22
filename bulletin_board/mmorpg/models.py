from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Advertisements(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    CATEGORY = (
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('gild_masters', 'Гилдмастеры'),
        ('quest_givers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion_makers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний'))
    content = models.FileField(upload_to='accepted/', null=True, blank=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY, verbose_name='Категирия', default='tanks')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200, default='')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)  
    # video = models.FileField(upload_to='videos/', null=True, blank=True)
    # video_url = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    ad = models.ForeignKey(Advertisements, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    accepted = models.BooleanField(default=False) # Флаг для отметки принятых откликов
    created_at = models.DateTimeField(auto_now_add=True)

