class UserRegisterCommand(object):
    def __init__(self, user_id, user_name, password, emailid):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.emailid = emailid

class UpdatePasswordCommand(object):
    def __init__(self, user_id, new_password, original_version):
        self.user_id = user_id
        self.new_password = new_password
        self.original_version = original_version