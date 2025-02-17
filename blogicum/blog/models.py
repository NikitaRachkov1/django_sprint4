from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()

MAX_LENGTH = 256


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Снимите галочку, чтобы скрыть публикацию.')
    )
    created_at = models.DateTimeField(_('Добавлено'), auto_now_add=True)

    class Meta:
        abstract = True


class PostManager(models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .select_related('category')
            .filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            )
        )


class Category(PublishedModel):
    title = models.CharField(_('Заголовок'), max_length=MAX_LENGTH)
    description = models.TextField(_('Описание'))
    slug = models.SlugField(
        _('Идентификатор'),
        unique=True,
        help_text=_(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('Категории')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(_('Название места'), max_length=MAX_LENGTH)

    class Meta:
        verbose_name = _('местоположение')
        verbose_name_plural = _('Местоположения')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(PublishedModel):
    objects = PostManager()

    title = models.CharField(_('Заголовок'), max_length=MAX_LENGTH)
    text = models.TextField(
        _('Текст'),
        help_text=_('Введите текст публикации')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор публикации')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Местоположение')
    )
    pub_date = models.DateTimeField(
        _('Дата и время публикации'),
        help_text=_(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        )
    )

    image = models.ImageField(
        upload_to='posts/',
        null=True,
    )

    @property
    def comment_count(self):
        return len(self.comments.all())

    class Meta:
        verbose_name = _('публикация')
        verbose_name_plural = _('Публикации')
        default_related_name = 'posts'
        ordering = ('-pub_date',)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
