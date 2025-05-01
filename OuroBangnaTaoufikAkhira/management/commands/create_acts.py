from django.core.management.base import BaseCommand
from OuroBangnaTaoufikAkhira.models import Act


class Command(BaseCommand):
    help = "Create initial medical acts if they do not exist"

    def handle(self, *args, **kwargs):
        acts = [
            {
                "code": "ACT-001",
                "libelle": "Consultation adulte",
                "amount": 10000,
                "act_type_id": 1,
            },
            {
                "code": "ACT-002",
                "libelle": "Consultation enfant",
                "amount": 8000,
                "act_type_id": 1,
            },
            {
                "code": "ACT-003",
                "libelle": "Consultation cardiologique",
                "amount": 15000,
                "act_type_id": 2,
            },
            {
                "code": "ACT-004",
                "libelle": "Consultation dermatologique",
                "amount": 14000,
                "act_type_id": 2,
            },
            {
                "code": "ACT-005",
                "libelle": "Échographie pelvienne",
                "amount": 18000,
                "act_type_id": 3,
            },
            {
                "code": "ACT-006",
                "libelle": "Échographie rénale",
                "amount": 19000,
                "act_type_id": 3,
            },
            {
                "code": "ACT-007",
                "libelle": "Radio thorax face",
                "amount": 10000,
                "act_type_id": 4,
            },
            {
                "code": "ACT-008",
                "libelle": "Radio thorax profil",
                "amount": 10000,
                "act_type_id": 4,
            },
            {
                "code": "ACT-009",
                "libelle": "Hémogramme complet",
                "amount": 9000,
                "act_type_id": 5,
            },
            {
                "code": "ACT-010",
                "libelle": "Bilan hépatique",
                "amount": 11000,
                "act_type_id": 5,
            },
            {
                "code": "ACT-011",
                "libelle": "Pose de voie veineuse périphérique",
                "amount": 7000,
                "act_type_id": 6,
            },
            {
                "code": "ACT-012",
                "libelle": "Perfusion avec médicament",
                "amount": 12000,
                "act_type_id": 6,
            },
            {
                "code": "ACT-013",
                "libelle": "Suture simple",
                "amount": 10000,
                "act_type_id": 7,
            },
            {
                "code": "ACT-014",
                "libelle": "Suture profonde",
                "amount": 13000,
                "act_type_id": 7,
            },
            {
                "code": "ACT-015",
                "libelle": "Pansement simple",
                "amount": 6000,
                "act_type_id": 8,
            },
            {
                "code": "ACT-016",
                "libelle": "Ablation de fils",
                "amount": 5000,
                "act_type_id": 8,
            },
            {
                "code": "ACT-017",
                "libelle": "ECG au repos",
                "amount": 8000,
                "act_type_id": 9,
            },
            {
                "code": "ACT-018",
                "libelle": "ECG d’effort",
                "amount": 12000,
                "act_type_id": 9,
            },
            {
                "code": "ACT-019",
                "libelle": "Vaccin contre la grippe",
                "amount": 6000,
                "act_type_id": 10,
            },
            {
                "code": "ACT-020",
                "libelle": "Vaccin contre le tétanos",
                "amount": 7000,
                "act_type_id": 10,
            },
        ]

        for act_data in acts:
            act, created = Act.objects.get_or_create(
                libelle=act_data["libelle"],
                defaults={
                    "code": act_data["code"],
                    "amount": act_data["amount"],
                    "act_type_id": act_data["act_type_id"],
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'L\'acte "{act.libelle}" a été créé avec succès'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'L\'acte "{act.libelle}" existe déjà')
                )
