from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import models
from common.models import uuid_to_bin, bin_to_uuid, UuidToBinField, CommonModel

import uuid
import binascii
import datetime


class TestUuidConvertion(TestCase):
    def test_uuid_to_bin(self):
        for a, b, expected in [("099a2ec8-0535-11ef-bf80-0242ac110002",
                                True,
                                b'11EF0535099A2EC8BF800242AC110002'),
                               ("099a2ec8-0535-11ef-bf80-0242ac110002",
                                False, b'099A2EC8053511EFBF800242AC110002')]:
            binary_uuid = uuid_to_bin(a, b)
            self.assertEqual(binascii.b2a_hex(binary_uuid).upper(), expected)

    def test_bin_to_uuid(self):
        for a, b, expected in [(b'11EF0535099A2EC8BF800242AC110002',
                                True,
                                uuid.UUID("099a2ec8-0535-11ef-bf80-0242ac110002")),
                               (b'099A2EC8053511EFBF800242AC110002',
                                False,
                                uuid.UUID("099a2ec8-0535-11ef-bf80-0242ac110002"))]:
            binary_uuid = binascii.a2b_hex(a)
            uuid_str = bin_to_uuid(binary_uuid, b)
            self.assertEqual(uuid_str, expected)


class TestUuidToBinField(TestCase):
    def setUp(self):
        self.field = UuidToBinField()

    def test_from_db_value(self):
        t_uuid = uuid.UUID("099a2ec8-0535-11ef-bf80-0242ac110002")
        b_uuid = uuid_to_bin(str(t_uuid), True)
        self.assertEqual(t_uuid, self.field.from_db_value(b_uuid, None, None))

    def test_to_python(self):
        t_uuid = uuid.UUID("099a2ec8-0535-11ef-bf80-0242ac110002")
        b_uuid = uuid_to_bin(str(t_uuid), swap_flag=True)
        restored_uuid = self.field.to_python(b_uuid)
        self.assertEqual(restored_uuid, t_uuid)

    def test_get_prep_value(self):
        t_uuid = uuid.UUID("099a2ec8-0535-11ef-bf80-0242ac110002")
        b_uuid = self.field.get_prep_value(t_uuid)
        self.assertEqual(b_uuid, uuid_to_bin(str(t_uuid), swap_flag=True))


class DemoModel(CommonModel):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'demos'


class TestCommonModel(TestCase):

    def setUp(self):
        self.uid = uuid.UUID("099a2ec8-0535-11ef-bf80-0242ac110002")
        self.demo_model_instance = DemoModel.objects.create(
                uid=self.uid,
                name="demo2"
                )

    def test_model_creation(self):
        self.assertIsInstance(self.demo_model_instance, DemoModel)
        self.assertEqual(DemoModel.objects.count(), 1)

    def test_can_save(self):
        self.demo1 = DemoModel()
        self.demo1.name = "test"
        self.demo1.save()
        self.assertEqual(2, DemoModel.objects.count())

    def test_uuid_to_bin_field(self):
        self.assertIsInstance(self.demo_model_instance.uid, uuid.UUID)
        self.assertEqual(str(self.demo_model_instance.uid), str(self.uid))

    def test_state_field(self):
        self.assertEqual(self.demo_model_instance.state, 'N')
        # TODO: Choices 中没有'X', 但是没有抛异常
        # with self.assertRaises(ValueError):
        #     DemoModel.objects.create(uid=uuid.uuid1(),
        #                              name='wstate',
        #                              state='X')

    def test_state_field_choices_validation(self):
        # 测试 state 字段的 choices 验证
        with self.assertRaises(ValidationError):
            # 尝试创建一个 state 为 'X' 的实例，这应该失败
            invalid_instance = DemoModel(name='st', state='X')
            invalid_instance.full_clean()

    def test_auto_now_add(self):
        """测试 ctime 字段是否自动设置为当前日期"""
        self.assertIsNotNone(self.demo_model_instance.ctime)
        self.assertTrue(isinstance(self.demo_model_instance.ctime,
                        datetime.datetime))

    def test_auto_now(self):
        """测试mtime字段是否在每次修改自动修改为当前时间"""
        original_mtime = self.demo_model_instance.mtime
        self.demo_model_instance.name = 'Updated Data'
        self.demo_model_instance.save()
        self.assertNotEqual(self.demo_model_instance.mtime, original_mtime)
