class UserRegisterEvent(object):
    def __init__(self, user_id, user_name, password, emailid):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.emailid = emailid

    def apply_changes(self, user):
        user.id = self.user_id
        user.name = self.user_name
        user.password = self.password
        user.emailid = self.emailid

class UpdatePasswordEvent(object):
    def __init__(self, user_id, new_password):
        self.user_id = user_id
        self.new_password = new_password

    def apply_changes(self, user):
        user.password = self.new_password