import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from actors.models import Actor


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument('file_name', type=str, help='Nome do arquivo CSV com atores.')

        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']

        with open(file_name, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row['name']
                birthday = datetime.strptime(row['birthday'], '%Y-%m-%d').date()
                nationality = row['nationality']

                self.stdout.write(self.style.NOTICE(f'ATOR: {name}'))

                Actor.objects.create(name=name, birthday=birthday, nationality=nationality)

        self.stdout.write(self.style.SUCCESS('ATORES IMPORTADOS COM SUCESSO!'))
