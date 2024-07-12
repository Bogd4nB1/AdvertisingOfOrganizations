from django.db import models
from django.urls import reverse
from django.template.defaultfilters import truncatechars  # or truncatewords
from pytils.translit import slugify as slugify_pytils

class AdressOrg(models.Model):
    country = models.CharField(max_length=255, verbose_name="Страна")
    region = models.CharField(max_length=255, verbose_name="Регион")
    city = models.CharField(max_length=255, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")

    def __str__(self) -> str:
        return self.country + ', ' + self.region + ', ' + self.city + ', ' + self.street
    
    class Meta:
        db_table = 'AdressOrg'
        verbose_name = 'Адрес организации'
        verbose_name_plural = 'Адреса организаций'

class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название тега')
    slug = models.SlugField(max_length=50, verbose_name='Tag URL', unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": slugify_pytils(self.title)})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_pytils(self.title)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        db_table = 'Tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Account(models.Model):
    username = models.CharField(max_length=255, verbose_name="Логин")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    password2 = models.CharField(max_length=255, verbose_name="Повторите пароль")
    organitathion = models.ForeignKey("Organitathion", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = 'Account'
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

class Organitathion(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название организации")
    content = models.TextField(verbose_name="Описание организации")
    web_site = models.CharField(max_length=255, verbose_name="Сайт организации")
    phone = models.CharField(max_length=20, verbose_name="Телефон организации")
    adress = models.ForeignKey(AdressOrg, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Адрес организации")
    tages = models.ManyToManyField(Tag, blank=True, related_name='tags', verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото')
    email = models.EmailField(max_length=255, verbose_name="Почта")

    @property
    def short_description(self):
        # для короткого описания в админк
        return truncatechars(self.content, 9)
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'Organitathion'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

class Comment(models.Model):
    organitathion = models.ForeignKey(Organitathion, on_delete=models.SET_NULL, related_name='org', verbose_name='Статья', blank=True, null=True)
    author = models.CharField(max_length=80, verbose_name='Имя', blank=True, null=True)
    text = models.TextField(verbose_name='Описание')
    children = models.ManyToManyField('Comment', verbose_name='Дочерние комментарии', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    class Meta:
        ordering = ['-created_at']
        db_table = 'Comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"{self.author}: {self.text}"
    