from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from OuroBangnaTaoufikAkhira.models import User


class Command(BaseCommand):
    help = "Créer des utilisataurs"

    def handle(self, *args, **kwargs):
        users = [
            {
                "username": "taoufik",
                "email": "taoufik@gmail.com",
                "password": "taoufik2005",
            },
            {
                "username": "fifi",
                "email": "fifi@gmail.com",
                "password": "taoufik2005",
            },
        ]
        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "password": make_password(user_data["password"]),
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"L'utilisateur {user.username} a été créé avec succès."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"L'utilisateur {user.username} existe déjà.")
                )
