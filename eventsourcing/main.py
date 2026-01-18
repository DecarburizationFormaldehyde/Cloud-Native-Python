from eventsourcing.aggregate import Aggregate
from eventsourcing.events import *


class UserDetails(Aggregate):
    def __init__(self, id=None, name="", password="", email="", username=""):
        super().__init__()
        # 创建初始事件
        if id is not None:
            # 如果提供ID，则模拟从事件重建状态
            pass
        else:
            # 默认初始化
            self.id = id
            self.name = name
            self.password = password
            self.email = email
            self.username = username

    def user_register(self, user_id, user_name, password, emailid):
        event = UserRegisterEvent(user_id, user_name, password, emailid)
        self._apply_changes(event)
        # 更新当前状态
        event.apply_changes(self)

    def update_password(self, new_password):
        event = UpdatePasswordEvent(self.id, new_password)
        self._apply_changes(event)
        # 更新当前状态
        event.apply_changes(self)