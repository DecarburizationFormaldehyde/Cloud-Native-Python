from contextlib import contextmanager

from commands import *
from events import *

class UserCommandsHandler(object):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def handle(self, command):
        if isinstance(command, UserRegisterCommand):
            event = UserRegisterEvent(command.user_id, command.user_name, command.password, command.emailid)
            self.user_repository.save(event)
        elif isinstance(command, UpdatePasswordCommand):
            with self._user_(command.user_id, command.original_version) as user:
                user.update_password(command.new_password)

    @contextmanager
    def _user_(self, user_id, user_version):
        user = self.user_repository.find_by_id(user_id)
        yield user
        self.user_repository.save(user, user_version)