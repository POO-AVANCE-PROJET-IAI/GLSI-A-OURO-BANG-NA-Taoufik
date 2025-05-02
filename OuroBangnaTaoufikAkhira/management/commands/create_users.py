from django.core.management.base import BaseCommand
from OuroBangnaTaoufikAkhira.models import User


class Command(BaseCommand):
    help = "Créer des utilisateurs"

    def handle(self, *args, **kwargs):
        users = [
            {
                "username": "taoufik",
                "email": "taoufik@gmail.com",
                "password": "taoufik2005",
            },
            {
                "username": "mei",
                "email": "mei@gmail.com",
                "password": "taoufik2005",
            },
            {
                "username": "fifi",
                "email": "fifi@gmail.com",
                "password": "taoufik2005",
            },
        ]
        for user_data in users:
            if not User.objects.filter(username=user_data["username"]).exists():
                User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"L'utilisateur {user_data['username']} a été créé."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"L'utilisateur {user_data['username']} existe déjà."
                    )
                )
