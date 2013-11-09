"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from healthplans.models import Provider
from healthplans.models import Plan

class HealtplansModelsTest(TestCase):
    def test_011_provider_create(self):
        provider = Provider.objects.create(
                name="Test Provider")
        self.assertIsNotNone(provider)
        self.assertIsNotNone(provider.created_time)
        self.assertIsNotNone(provider.updated_time)

    def test_012_plan_create(self):
        provider = Provider.objects.create(
                name="Test Provider")
        COST = 1.05
        plan = Plan.objects.create(
                provider=provider,
                name="Test Plan",
                category=Plan.PLATINUM,
                base_rate=COST)
        self.assertIsNotNone(plan)
        self.assertIsNotNone(plan.created_time)
        self.assertIsNotNone(plan.updated_time)
        self.assertEqual(plan.base_rate, COST)

    def test_021_provider_slug(self):
        provider = Provider.objects.create(
                    name="Test Provider")
        self.assertEqual(provider.slug, "Test-Provider")

    def test_022_plan_slug(self):
        provider = Provider.objects.create(
                name="Test Provider")
        COST = 1.05
        plan = Plan.objects.create(
                provider=provider,
                name="Test Plan",
                category=Plan.PLATINUM,
                base_rate=COST)
        self.assertIsNotNone(plan)
        self.assertEqual(plan.slug, "Test-Plan")


from django.test import Client
class HealthplansViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_links(self):
        response = self.client.get('/')
        self.assertContains(response, 'href="/providers/"')
        self.assertContains(response, 'href="/plans/"')

    def test_provider_list(self):
        provider = Provider.objects.create(
                name="Test Provider")  # TODO: fixtures
        response = self.client.get('/providers/')
        self.assertContains(response, provider.name)
        self.assertContains(response, 'href="/providers/%s"' % provider.slug)

    def test_provider_detail(self):
        provider = Provider.objects.create(
                name="Test Provider")  # TODO: fixtures
        response = self.client.get('/providers/%s' % provider.slug)
        self.assertContains(response, provider.name)
        self.assertContains(response, 'href="/providers/%s">' % provider.slug)

    def test_plan_list(self):
        provider = Provider.objects.create(
                name="Test Provider")  # TODO: fixtures
        plan = Plan.objects.create(
                provider=provider,
                name="Test Plan",
                category=Plan.PLATINUM,
                base_rate=1.05)
        response = self.client.get('/plans/')
        self.assertContains(response, plan.name)
        self.assertContains(response, 'href="/plans/%s"' % plan.slug)

    def test_plan_detail(self):
        provider = Provider.objects.create(
                name="Test Provider")  # TODO: fixtures
        plan = Plan.objects.create(
                provider=provider,
                name="Test Plan",
                category=Plan.PLATINUM,
                base_rate=1.05)
        response = self.client.get('/plans/%s' % plan.slug)
        self.assertContains(response, plan.name)
        self.assertContains(response, 'href="/plans/%s"' % plan.slug)


class HealthplansAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self._superuser_login()

    def _superuser_login(self):
        USERNAME = 'test'
        EMAIL = 'test@example.org'
        PASSWORD = 'TODOTODOTODO'
        from django.db import DEFAULT_DB_ALIAS as db
        from django.contrib.auth.models import User
        User.objects.db_manager(db).create_superuser(
            USERNAME, EMAIL, PASSWORD)
        logged_in = self.client.login(
                username=USERNAME,
                password=PASSWORD)
        self.assertEqual(logged_in, True)

    def test_provider_admin(self):
        provider = Provider.objects.create(
                name="Test Provider")  # TODO: fixtures
        response = self.client.get('/admin/healthplans/provider/')
        self.assertContains(response, provider.name)

    def test_plan_admin(self):
        provider = Provider.objects.create(
                name="Test Provider")  # TODO: fixtures
        plan = Plan.objects.create(
                provider=provider,
                name="Test Plan",
                category=Plan.PLATINUM,
                base_rate=1.05)
        response = self.client.get('/admin/healthplans/plan/')
        self.assertContains(response, plan.name)
