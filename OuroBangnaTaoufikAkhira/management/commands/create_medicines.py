from django.core.management.base import BaseCommand
from OuroBangnaTaoufikAkhira.models import Medicine


class Command(BaseCommand):
    help = "Créer des médicaments"

    def handle(self, *args, **kwargs):
        medicines = [
            {"code": "MDCN-001", "libelle": "Paracétamol"},
            {"code": "MDCN-002", "libelle": "Ibuprofène"},
            {"code": "MDCN-003", "libelle": "Aspirine"},
            {"code": "MDCN-004", "libelle": "Amoxicilline"},
            {"code": "MDCN-005", "libelle": "Ciprofloxacine"},
            {"code": "MDCN-006", "libelle": "Metformine"},
            {"code": "MDCN-007", "libelle": "Salbutamol"},
            {"code": "MDCN-008", "libelle": "Oméprazole"},
            {"code": "MDCN-009", "libelle": "Loratadine"},
            {"code": "MDCN-010", "libelle": "Simvastatine"},
            {"code": "MDCN-011", "libelle": "Losartan"},
            {"code": "MDCN-012", "libelle": "Prednisone"},
            {"code": "MDCN-013", "libelle": "Furosemide"},
            {"code": "MDCN-014", "libelle": "Tramadol"},
            {"code": "MDCN-015", "libelle": "Clarithromycine"},
        ]

        for med_data in medicines:
            medicine, created = Medicine.objects.get_or_create(
                libelle=med_data["libelle"],
                defaults={
                    "code": med_data["code"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Le médicament "{medicine.libelle}" a été créer avec succès'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Le médicament "{medicine.libelle}" existe déjà'
                    )
                )
