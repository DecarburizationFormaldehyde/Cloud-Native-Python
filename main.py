from aggregate import Aggregate
from events import *
from errors import InvalidOpreationError

class userdetail(Aggregate):
    def __init__(self,id=None,name="",password="",email="",username=""):
        super().__init__(self)
        self._apply_changes(userdetail(id,name,password,email,username))

    def userRegister(self,userdetails):
        userdetails={1, "robin99", "xxxxxx", "robinatkevin@gmail.com"}
        self._apply_changes(UserRegisterEvent(userdetails))

    def updatePassword(self, count):
        password = ""
        self._apply_changes(UserPasswordEvent(password))