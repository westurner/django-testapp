from django.db import models
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

#from .utils import slugify


def slugify(s):
    return s.replace(' ', '-')  # TODO FIXME

class DateTimeModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Provider(DateTimeModel):
    name = models.CharField(max_length=255)
    website = models.CharField('URL', max_length=512, blank=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('provider-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Provider, self).save(*args, **kwargs)


class Plan(DateTimeModel):
    BRONZE = 'Bronze'
    SILVER = 'Silver'
    GOLD   = 'Gold'
    PLATINUM = 'Platinum'
    CATASTROPHIC = 'Catastrophic'
    CATEGORY_CHOICES = (
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD,   'Gold'),
        (PLATINUM, 'Platinum'),
        (CATASTROPHIC, 'Catastrophic')
    )

    provider = models.ForeignKey(Provider, related_name='plans')
    name = models.CharField(max_length=255)
    url = models.CharField('URL', max_length=512, blank=True)
    #state = models.CharField(max_length=255) # TODO: OneToMany/ListField
    category = models.CharField(max_length=12,
                                choices=CATEGORY_CHOICES,
                                blank=False)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plan-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Plan, self).save(*args, **kwargs)


class ProvidersSitemap(Sitemap):
    changefreq = 'daily'  # 'weekly'

    def items(self):
        return Provider.objects.order_by('name')

    def lastmod(self, obj):
        return obj.updated_time


class PlansSitemap(Sitemap):
    changefreq = 'daily'  # 'weekly'

    def items(self):
        return Plan.objects.order_by('provider', 'name')

    def lastmod(self, obj):
        return obj.updated_time
