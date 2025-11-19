from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    list_filter = ('created_at', )
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', )

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Post Count"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status',
                    'views_count', 'comments_count', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    raw_id_fields = ('author',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Meta', {
            'fields': ('category', 'author', 'status')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
