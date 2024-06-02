from django.test import TestCase

from dca.models import PlatformModel, PlanModel, LogModel

import datetime
# Create your tests here.


class TestPlatformModel(TestCase):
    def setUp(self):
        self.platform_instance = PlatformModel.objects.create(pf_name='币安',
                                                              pf_alias='BN')

    def test_can_save_platform(self):
        pf1 = PlatformModel()
        pf1.pf_name = '欧易'
        pf1.pf_alias = 'OKX'
        pf1.save()
        self.assertEqual(2, PlatformModel.objects.count())


class TestPlanModel(TestCase):
    def setUp(self):
        self.platform_instance = PlatformModel.objects.create(pf_name='币安',
                                                              pf_alias='BN')

    def test_can_save_plan(self):
        p1 = PlanModel()
        p1.p_name = 'Inc1'
        p1.p_alias = 'Inc1'
        p1.p_platform = self.platform_instance
        p1.p_start_at = datetime.date.today()
        p1.p_cycle = 'D'
        p1.p_type = 'I'
        p1.p_variable = 1
        p1.p_expected_total = 66
        p1.p_end_at = datetime.date.today() + datetime.timedelta(days=365)
        p1.save()
        self.assertEqual(1, PlanModel.objects.count())


class TestLogModel(TestCase):
    def setUp(self):
        _today = datetime.date.today()
        _day_in_a_year = _today + datetime.timedelta(days=365)
        self.platform_instance = PlatformModel.objects.create(pf_name='币安',
                                                              pf_alias='BN')
        self.plan_instance = PlanModel.objects.create(p_name='BN_Inc1',
                                                      p_alias='BN_INC1',
                                                      p_start_at=_today,
                                                      p_end_at=_day_in_a_year,
                                                      p_type='I',
                                                      p_cycle='D',
                                                      p_variable=1,
                                                      p_expected_total=100,
                                                      p_platform=self.platform_instance
                                                      )

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
