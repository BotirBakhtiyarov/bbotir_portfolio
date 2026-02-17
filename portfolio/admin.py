"""
Admin configuration for portfolio models.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import CaseStudy, CaseStudyImage


class CaseStudyImageInline(admin.TabularInline):
    model = CaseStudyImage
    extra = 0
    fields = ('image', 'alt_text', 'order')


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'order', 'updated_at')
    list_editable = ('is_published', 'order')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'summary', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CaseStudyImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary', 'is_published', 'order')
        }),
        ('Content', {
            'fields': ('problem', 'solution', 'tech_stack', 'key_results')
        }),
        ('Links', {
            'fields': ('github_link', 'demo_link')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CaseStudyImage)
class CaseStudyImageAdmin(admin.ModelAdmin):
    list_display = ('case_study', 'alt_text', 'order')
