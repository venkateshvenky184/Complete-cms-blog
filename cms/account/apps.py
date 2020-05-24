from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'


    def ready(self):
        import account.signals


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals