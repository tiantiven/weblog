from django.test import TestCase

from dca.models import PlatformModel, PlanModel, LogModel

import datetime
# Create your tests here.


class TestPlatformModel(TestCase):
    def setUp(self):
        self.platform_instance = PlatformModel.objects.create(name='币安',
                                                              alias='BN')

    def test_can_save_platform(self):
        pf1 = PlatformModel()
        pf1.name = '欧易'
        pf1.alias = 'OKX'
        pf1.save()
        self.assertEqual(2, PlatformModel.objects.count())


class TestPlanModel(TestCase):
    def setUp(self):
        self.platform_instance = PlatformModel.objects.create(name='币安',
                                                              alias='BN')

    def test_can_save_plan(self):
        p1 = PlanModel()
        p1.name = 'Inc1'
        p1.alias = 'Inc1'
        p1.platform = self.platform_instance
        p1.start_at = datetime.date.today()
        p1.cycle = 'D'
        p1.p_type = 'I'
        p1.variable = 1
        p1.expected_total = 66
        p1.end_at = datetime.date.today() + datetime.timedelta(days=365)
        p1.save()
        self.assertEqual(1, PlanModel.objects.count())


class TestLogModel(TestCase):
    def setUp(self):
        _today = datetime.date.today()
        _day_in_a_year = _today + datetime.timedelta(days=365)
        self.platform_instance = PlatformModel.objects.create(name='币安',
                                                              alias='BN')
        self.plan_instance = PlanModel.objects.create(
                name='BN_Inc1',
                alias='BN_INC1',
                start_at=_today,
                end_at=_day_in_a_year,
                p_type='I',
                cycle='D',
                variable=1,
                expected_total=100,
                platform=self.platform_instance)

    def test_can_save_log(self):
        l1 = LogModel()
        l1.p_uid = self.plan_instance
        l1.direction = 'D'
        l1.expected_quantity = 1
        l1.actual_quantity = 1
        l1.progress = 1
        l1.save()
        l2 = LogModel()
        l2.p_uid = self.plan_instance
        l2.direction = 'W'
        l2.expected_quantity = 1
        l2.actual_quantity = 1
        l2.progress = 0
        l2.save()
        self.assertEqual(2, LogModel.objects.count())
