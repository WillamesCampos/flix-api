from django.core.management.base import BaseCommand

from movies.services.import_service import MovieImportService


class Command(BaseCommand):
    help = 'Importa filmes de um arquivo CSV'

    def add_arguments(self, parser) -> None:
        parser.add_argument('file_name', type=str, help='Nome do arquivo CSV com filmes.')
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        service = MovieImportService(file_name)
        result = service.import_movies()

        created_count = result['created_count']
        skipped_count = result['skipped_count']
        errors = result['errors']

        # Resumo
        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 50}'))
        self.stdout.write(self.style.SUCCESS('RESUMO DA IMPORTAÇÃO'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 50}'))
        self.stdout.write(self.style.SUCCESS(f'Filmes criados: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Filmes ignorados: {skipped_count}'))

        if errors:
            self.stdout.write(self.style.ERROR('\nERROS ENCONTRADOS:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))

        if created_count > 0:
            self.stdout.write(self.style.SUCCESS('\nFILMES IMPORTADOS COM SUCESSO!'))
