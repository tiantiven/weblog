from django.db import models
from common.models import CommonModel
# Create your models here.


class PlatformModel(CommonModel):
    pf_name = models.CharField(max_length=64)
    pf_alias = models.CharField(max_length=64)

    class Meta:
        db_table = 'dca_platforms'


class PlanModel(CommonModel):
    P_CYCLE_CHOICES = {
            'D': 'Daily',
            'W': 'Weekly',
            'M': 'Monthly',
            'Q': 'Quarterly',
            'A': 'Annual',
            'B': 'Biennial'
            }
    P_TYPE_CHOICES = {
            'S': 'Single',
            'I': 'Increment',
            'F': 'Function'
            }
    p_name = models.CharField(max_length=64)
    p_alias = models.CharField(max_length=64)
    p_start_at = models.DateField(null=False)
    p_end_at = models.DateField(null=False)
    p_cycle = models.CharField(max_length=1,
                               choices=P_CYCLE_CHOICES,
                               default='D')
    p_type = models.CharField(max_length=1,
                              choices=P_TYPE_CHOICES,
                              default='S')
    p_variable = models.BigIntegerField(null=False, default=1)
    p_expected_total = models.BigIntegerField()
    p_platform = models.ForeignKey(PlatformModel,
                                   on_delete=models.CASCADE,
                                   related_name='plans'
                                   )

    class Meta:
        db_table = 'dca_plans'


class LogModel(CommonModel):
    LOG_DIRECTION_CHOICES = {
            'D': 'Deposit',
            'W': 'WithDrawal'
            }
    p_uid = models.ForeignKey(PlanModel,
                              on_delete=models.CASCADE,
                              related_name='deposit_logs')
    direction = models.CharField(max_length=1,
                                 null=False,
                                 choices=LOG_DIRECTION_CHOICES,
                                 default='D')
    expected_quantity = models.BigIntegerField()
    actual_quantity = models.BigIntegerField()
    progress = models.IntegerField()

    class Meta:
        db_table = 'dca_logs'
