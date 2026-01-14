class UserRegisterEvent(object):
    def apply_change(self,userdetails):
        id=userdetails.id
        name=userdetails.name
        password=userdetails.password
        emailid=userdetails.emailid

class UserPasswordEvent(object):
    def __init__(self,password):
        self.password=password

    def apply_change(password):
        user.password=password
