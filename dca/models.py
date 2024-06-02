from django.db import models
from common.models import CommonModel
# Create your models here.


class PlatformModel(CommonModel):
    name = models.CharField(max_length=64)
    alias = models.CharField(max_length=64)

    class Meta:
        db_table = 'dca_platforms'


class PlanModel(CommonModel):
    CYCLE_CHOICES = {
            'D': 'Daily',
            'W': 'Weekly',
            'M': 'Monthly',
            'Q': 'Quarterly',
            'A': 'Annual',
            'B': 'Biennial'
            }
    TYPE_CHOICES = {
            'S': 'Single',
            'I': 'Increment',
            'F': 'Function'
            }
    name = models.CharField(max_length=64)
    alias = models.CharField(max_length=64)
    start_at = models.DateField(null=False)
    end_at = models.DateField(null=False)
    cycle = models.CharField(max_length=1,
                             choices=CYCLE_CHOICES,
                             default='D')
    p_type = models.CharField(max_length=1,
                              choices=TYPE_CHOICES,
                              default='S')
    variable = models.BigIntegerField(null=False, default=1)
    expected_total = models.BigIntegerField()
    platform = models.ForeignKey(PlatformModel,
                                 on_delete=models.CASCADE,
                                 related_name='plans')

    class Meta:
        db_table = 'dca_plans'


class LogModel(CommonModel):
    DIRECTION_CHOICES = {
            'D': 'Deposit',
            'W': 'WithDrawal'
            }
    plan = models.ForeignKey(PlanModel,
                             on_delete=models.CASCADE,
                             related_name='logs')
    direction = models.CharField(max_length=1,
                                 null=False,
                                 choices=DIRECTION_CHOICES,
                                 default='D')
    expected_quantity = models.BigIntegerField()
    actual_quantity = models.BigIntegerField()
    progress = models.IntegerField()

    class Meta:
        db_table = 'dca_logs'
