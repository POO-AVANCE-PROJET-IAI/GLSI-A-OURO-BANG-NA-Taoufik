from django.core.management.base import BaseCommand
from OuroBangnaTaoufikAkhira.models import ActType


class Command(BaseCommand):
    help = "Créer des types d’actes médicaux"

    def handle(self, *args, **kwargs):
        act_types = [
            {"code": "T-ACT-001", "libelle": "Consultation générale"},
            {"code": "T-ACT-002", "libelle": "Consultation spécialisée"},
            {"code": "T-ACT-003", "libelle": "Échographie abdominale"},
            {"code": "T-ACT-004", "libelle": "Radiographie thoracique"},
            {"code": "T-ACT-005", "libelle": "Analyse de sang complète"},
            {"code": "T-ACT-006", "libelle": "Pose de perfusion"},
            {"code": "T-ACT-007", "libelle": "Suture de plaie"},
            {"code": "T-ACT-008", "libelle": "Soins infirmiers"},
            {"code": "T-ACT-009", "libelle": "Electrocardiogramme (ECG)"},
            {"code": "T-ACT-010", "libelle": "Vaccination"},
        ]

        for act_type_data in act_types:
            act_type, created = ActType.objects.get_or_create(
                libelle=act_type_data["libelle"],
                defaults={
                    "code": act_type_data["code"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Le type d\'acte "{act_type.libelle}" a été créé avec succès'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Le type d\'acte "{act_type.libelle}" existe déjà'
                    )
                )
