from django.apps import AppConfig


class UserfollowsConfig(AppConfig):
    name = 'UserFollows'


    def ready(self):
        import UserFollows.signals
