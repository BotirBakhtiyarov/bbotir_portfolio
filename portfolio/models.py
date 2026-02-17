"""
Portfolio models: case studies (projects) manageable via Django Admin.
"""
from django.db import models
from django.utils.text import slugify


class CaseStudy(models.Model):
    """A project / case study displayed on the portfolio."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    summary = models.CharField(max_length=300, help_text='Short one-line summary')
    problem = models.TextField(help_text='Problem description')
    solution = models.TextField(help_text='Solution approach')
    tech_stack = models.CharField(
        max_length=500,
        help_text='Comma-separated e.g. Django, PostgreSQL, Celery'
    )
    key_results = models.TextField(
        help_text='Key results / impact (one per line or short paragraphs)'
    )
    github_link = models.URLField(blank=True)
    demo_link = models.URLField(blank=True, help_text='Optional live demo URL')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Case studies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


class CaseStudyImage(models.Model):
    """Optional images for a case study."""
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='case_studies/%Y/%m/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
