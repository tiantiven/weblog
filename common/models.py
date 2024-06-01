import uuid

from django.db import models


def uuid_to_bin(uid: uuid.UUID = None, swap_flag: bool = False) -> bytes:
    """
    Convert a UUID string to a binary format.

    :param uuid_str: The UUID string to convert.
    :param swap_flag: If True, swap the time level parts of the UUID.
    :return: A binary representation of the UUID.
    """
    if not isinstance(uid, uuid.UUID):
        uid = uuid.UUID(uid)
    if uid is None:
        uid = uuid.uuid1()
    # 转换为二进制格式
    _b_uuid = uid.bytes
    # 如果swap_flag为真，则交换时间低部和时间高部
    if swap_flag:
        _b_uuid = _b_uuid[6:8] + _b_uuid[4:6] + _b_uuid[0:4] + _b_uuid[8:]
    return _b_uuid


def bin_to_uuid(b_uid: bytes, swap_flag: bool = False) -> uuid.UUID:
    """
    Convert a binary to a UUID string

    :param binary_uuid: The UUID binary to convert.
    :param swap_flag: If Ture, swap the time level part of the UUID.
    :return: UUID
    """
    if swap_flag:
        _b_uuid = b_uid[4:8] + b_uid[2:4] + b_uid[:2] + b_uid[8:]
    else:
        _b_uuid = b_uid
    return uuid.UUID(bytes=_b_uuid)


class UuidToBinField(models.Field):
    description = "UUID_TO_BIN()"

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.get('max_length', 16)
        kwargs.update({'max_length': self.max_length})
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return f'BINARY({self.max_length})'

    def rel_db_type(self, connection):
        return f'BINARY({self.max_length})'

    def from_db_value(self, value, expression, connection):
        """将数据库中的值转换为Python数据类型"""
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        else:
            return bin_to_uuid(value, True)

    def to_python(self, value):
        """将输入的数据转换为Python对象"""
        if isinstance(value, uuid.UUID):
            return value
        if value is None:
            return value
        return bin_to_uuid(value, True)

    def get_prep_value(self, value):
        """将Python对象转换为查询值"""
        if isinstance(value, uuid.UUID):
            return uuid_to_bin(value, True)
        else:
            return value


class CommonModel(models.Model):
    STATE_CHOICES = {
        'N': 'Normal',
        'D': 'Deleted',
        'P': 'Paused',
        'F': 'Finished'
        }
    uid = UuidToBinField(primary_key=True, default=uuid.uuid1, editable=False)
    ctime = models.DateTimeField(max_length=6, auto_now_add=True)
    mtime = models.DateTimeField(max_length=6, auto_now=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='N')

    class Meta:
        abstract = True
        ordering = ['-ctime']


# TODO: 自定义用户，需要修改Django自带的用户鉴权中间件，以后再说吧。
