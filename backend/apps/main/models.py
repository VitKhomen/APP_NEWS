from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Q, Case, When, Value, BooleanField, DateTimeField
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PostManager(models.Manager):
    '''Менеджер для моделі пост с доп методами'''

    def published(self):
        return self.filter(status='published')

    def pinned_post(self):
        '''Вертає закріплені пости по даті закріплення'''
        return self.filter(
            pin_info__isnull=False,
            pin_info__user__subscription__status='active',
            pin_info__user__subscription__end_date__gt=models.functions.now(),
            status='published'
        ).select_related(
            'pin_info', 'pin_info__user', 'pin_info__user__subcription'
        ).order_by('pin_info__pinned_at')

    def regular_posts(self):
        """Вертає незакріпленні псти"""
        return self.filter(pin_info__isnull=True, status='published')

    def with_subscription_info(self):
        """Додає шнформацію об авторі"""
        return self.select_related(
            'author', 'author__subscription', 'category'
        ).prefetch_related('pin_info')

    def for_feed(self):
        """Главная лента: закреплённые (активные) → сверху → обычные посты"""
        return self.get_queryset().filter(status='published').annotate(
            is_pinned_active=Case(
                When(
                    pin_info__isnull=False,
                    pin_info__user__subscription__status='active',
                    pin_info__user__subscription__end_date__gt=timezone.now(),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            ),
            sort_date=Case(
                When(
                    pin_info__isnull=False,
                    pin_info__user__subscription__status='active',
                    pin_info__user__subscription__end_date__gt=timezone.now(),
                    then='pin_info__pinned_at'
                ),
                default='created_at',
                output_field=DateTimeField()
            )
        ).order_by(
            '-is_pinned_active',   # закреплённые всегда сверху
            '-sort_date',          # новые закреплённые / новые посты выше
            '-created_at'
        ).select_related(
            'author', 'category', 'pin_info__user', 'author__subscription'
        )


class Post(models.Model):
    '''Модель поста блого с можливістю закріплення'''

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='posts'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    objects = PostManager()

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def comments_count(self):
        return self.comments.filter(is_active=True).count()

    @property
    def is_pinned(self):
        '''Перевіряє чи заріплен пост'''
        return hasattr(self, 'pin_info') and self.pin_info is not None

    @property
    def can_be_pinned_by_user(self):
        '''Перевіряє чи можна закріпити пост'''
        # Це свойство не повинно приймати параметри
        # Логіка повинна бути винесена в окремий метод

        # Пост повинен бути опублікован
        if self.status != 'published':
            return False

        return True

    def can_be_pinned_by(self, user):
        """Преревіряє чи може юзер закріпити пост"""
        if not user or not user.is_authenticated:
            return False

        # Пост має належити юзеру
        if self.author != user:
            return False

        # Пост має буди оублікован
        if self.status != 'published':
            return False

        # У користувача повинна бути активна підписка
        if not hasattr(user, 'subscription') or not user.subscription.is_active:
            return False

        return True

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def get_pinned_info(self):
        """Вертає інформацію о закріпленні поста"""
        if self.is_pinned:
            return {
                'is_pinned': True,
                'pinned_at': self.pin_info.pinned_at,
                'pinned_by': {
                    'id': self.pin_info.user.id,
                    'username': self.pin_info.user.username,
                    'has_active_subscription': self.pin_info.user.subscription.is_active
                }
            }
        return {'is_pinned': False}
