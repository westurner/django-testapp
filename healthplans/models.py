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
    slug = models.SlugField(max_length=255)
    url = models.CharField('URL', max_length=512, blank=True)
    #state = models.CharField(max_length=255) # TODO: OneToMany/ListField

    category = models.CharField(max_length=12,
                                choices=CATEGORY_CHOICES,
                                blank=False)
    base_rate = models.DecimalField(
                    decimal_places=2,
                    max_digits=7,
                    verbose_name="Estimated Monthly Base Rate",
                    help_text="What is the estimated monthly cost?",
                    )
    accuracy = models.DecimalField(
                    decimal_places=2,
                    max_digits=5,
                    verbose_name="Accuracy Estimate",
                    help_text="What percent of applications received "
                              "surcharged quotes?",
                    null=True,
                    blank=True
                    )
    denial_rate = models.DecimalField(
                    decimal_places=2,
                    max_digits=5,
                    verbose_name="Denial Rate",
                    help_text="What percent of applications are denied?",
                    null=True,
                    blank=True
                    )
    deductible_individual = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Deductible (Individual)",
                    null=True,
                    blank=True)
    deductible_family = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Deductible (Family)",
                    null=True,
                    blank=True)
    oop_limit_individual = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="In-Network Out-of-Pocket Limit (Individual)",
                    null=True,
                    blank=True)
    oop_limit_family = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="In-Network Out-of-Pocket Limit (Family)",
                    null=True,
                    blank=True)
    # TODO
    OOP_INCLUDES_CHOICES = (
        ('DCC', 'Deductible + Coinsurance + Co-pay'),
    )
    oop_includes = models.CharField(
                    max_length=255,
                    choices=OOP_INCLUDES_CHOICES,
                    help_text="What is included in the in-network "
                              "out-of-pocket limit?",
                    blank=True)
    hsa_eligible = models.BooleanField(
                    help_text="Is this plan Health Savings Account (HSA) "
                              "eligible?",
                    blank=True)
    plan_network_url = models.URLField(
                    max_length=512,
                    blank=True)
    # TODO
    PPO = 'PPO'
    DOCTOR_CHOICE_CHOICES = (
        (PPO, 'PPO'),
    )
    doctor_choice = models.CharField(
                    max_length=24,
                    choices=DOCTOR_CHOICE_CHOICES,
                    blank=True)
    annual_maximum_benefit_individual = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Annual Maximum Benefit (Individual)",
                    null=True,
                    blank=True)
    annual_maximum_benefit_family = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Annual Maximum Benefit (Family)",
                    null=True,
                    blank=True)

    # TODO: CharField
    copay_primary_care = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Primary care physician office visit Copay",
                    null=True,
                    blank=True)
    copay_specialist = models.DecimalField(
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Specialist care physician office visit Copay",
                    null=True,
                    blank=True)
    copay_diagnostic = models.DecimalField( # TODO: CharField
                    decimal_places=2,
                    max_digits=10,
                    verbose_name="Diagnostic test (X-ray, blood work)",
                    null=True,
                    blank=True)

    # TODO: either fixed-cost or % coinsurance after deductible
    outpatient_facility_fee = models.CharField(
                    max_length=255,
                    verbose_name="Outpatient Facility Fee",
                    help_text="e.g. for minor surgery",
                    blank=True)
    outpatient_service_fee = models.CharField(
                    max_length=255,
                    verbose_name="Outpatient Physician/Surgeon Fee",
                    help_text="e.g. for minor surgery",
                    blank=True)

    overnight_facility_fee = models.CharField(
                    max_length=255,
                    verbose_name="Overnight Hospital Facility Fee",
                    blank=True)
    overnight_service_fee = models.CharField(
                    max_length=255,
                    verbose_name="Overnight Hospital Physician/Surgeon Fee",
                    blank=True)

    emergency_room = models.CharField(
                    max_length=255,
                    verbose_name="Emergency Room",
                    help_text="e.g. If you have an emergency?",
                    blank=True)

    # TODO: $nn Copay
    pharmacy_generic = models.CharField(
                    max_length=255,
                    verbose_name="Generic drugs",
                    blank=True)
    pharmacy_preferred = models.CharField(
                    max_length=255,
                    verbose_name="Preferred drugs",
                    blank=True)
    pharmacy_specialty = models.CharField(
                    max_length=255,
                    verbose_name="Specialty drugs",
                    blank=True)
    formulary_url = models.URLField(
                    max_length=512,
                    blank=True)
    # TODO: pharmacy / formulary?

    mental_health_outpatient = models.CharField(
                    max_length=255,
                    verbose_name="Mental/behavioral health outpatient services",
                    blank=True)
    mental_health_inpatient = models.CharField(
                    max_length=255,
                    verbose_name="Mental/behavioral health inpatient services",
                    blank=True)
    substance_use_outpatient = models.CharField(
                    max_length=255,
                    verbose_name="Substance use disorder outpatient services",
                    blank=True)
    substance_use_inpatient = models.CharField(
                    max_length=255,
                    verbose_name="Substance use disorder inpatient services",
                    blank=True)

    prenatal_postnal_care = models.CharField(
                    max_length=255,
                    verbose_name="Prenatal/postnatal care",
                    blank=True)
    maternity_inpatient = models.CharField(
                    max_length=255,
                    verbose_name="Delivery and all inpatient services for "
                                 "maternity care",
                    blank=True)

    plan_brochure_url = models.URLField(
                    max_length=512,
                    blank=True)


    INCLUDED = 'I'
    EXCLUDED = 'E'
    LIMITED = 'L' # ... add'l CharField
    ADDITIONAL = 'A'
    BENEFIT_CHOICES = (
        (INCLUDED, 'Included'),
        (EXCLUDED, 'Excluded'),
        (LIMITED, 'Limited'),
        (ADDITIONAL, 'Additional'),
    )
    benefits_acupuncture = models.CharField(
        verbose_name="Acupuncture",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_bariatric_surgery = models.CharField(
        verbose_name="Bariatric surgery",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_chiropractic = models.CharField(
        verbose_name="Chiropractic",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_cosmetic_surgery = models.CharField(
        verbose_name="Cosmetic surgery",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_dental_care_adult = models.CharField(
        verbose_name="Dental care adult",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_dental_check_up_children = models.CharField(
        verbose_name="Dental check up children",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_durable_medical_equipment = models.CharField(
        verbose_name="Durable medical equipment",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_emergency_transportation = models.CharField(
        verbose_name="Emergency Transportation",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_eye_exam_adult = models.CharField(
        verbose_name="Eye exam adult",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_eye_glasses_children = models.CharField(
        verbose_name="Eye glasses children",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_habilitation = models.CharField(
        verbose_name="Habilitation",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_hearing_aid = models.CharField(
        verbose_name="Hearing aid",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_home_health_care = models.CharField(
        verbose_name="Home health care",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_hospice = models.CharField(
        verbose_name="Hospice",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_imaging = models.CharField(
        verbose_name="Imaging (CT/PET scans, MRIs)",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_infertility_treatment = models.CharField(
        verbose_name="Infertility treatment",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_inpatient_rehabilitation = models.CharField(
        verbose_name="Inpatient rehabilitation",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_long_term_care = models.CharField(
        verbose_name="Long-term care",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_non_emergency_care_outside_us = models.CharField(
        verbose_name="Non-emergency care outside U.S.",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_non_preferred_brand_drugs = models.CharField(
        verbose_name="Non-preferred brand drugs",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_other_practitioner_office_visit = models.CharField(
        verbose_name="Other practitioner office visit",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_outpatient_rehabilitation = models.CharField(
        verbose_name="Outpatient rehabilitation",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_preventine_care = models.CharField(
        verbose_name="Preventive care, screening, immunization",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_private_duty_nursing = models.CharField(
        verbose_name="Private duty nursing",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_routine_eye_exam_children = models.CharField(
        verbose_name="Routine eye exam children",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_routine_foot_care = models.CharField(
        verbose_name="Routine foot care",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_routine_hearing_tests = models.CharField(
        verbose_name="Routine hearing tests",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_skilled_nursing_care = models.CharField(
        verbose_name="Skilled nursing care",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_urgent_care = models.CharField(
        verbose_name="Urgent Care",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)
    benefits_weight_loss_program = models.CharField(
        verbose_name="Weight loss program",
        choices=BENEFIT_CHOICES,
        max_length=1,
        blank=True)

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
