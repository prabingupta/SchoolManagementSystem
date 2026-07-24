from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'

    def ready(self):
        import apps.accounts.models  # noqa: F401 — registers the post_save signal
