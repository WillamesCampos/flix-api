from django.core.management.base import BaseCommand

from actors.services.import_service import ActorImportService
from core.utils.file_readers.csv_reader import CSVReader
from core.utils.file_readers.excel_reader import ExcelReader
from core.utils.file_readers.file_reader import FileReader


class Command(BaseCommand):
    help = 'Import actors from a file'

    def __map_file_reader(self, file_path: str) -> FileReader:
        if file_path.endswith('.csv'):
            return CSVReader()
        elif file_path.endswith('.xlsx'):
            return ExcelReader()
        else:
            raise ValueError(f'Invalid file extension: {file_path}')

    def add_arguments(self, parser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the CSV file with actors.')

        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        file_reader = self.__map_file_reader(file_path)
        service = ActorImportService(file_path=file_path, file_reader=file_reader)
        result = service.import_actors()

        created_count = result['created_count']
        skipped_count = result['skipped_count']
        errors = result['errors']

        self.stdout.write(self.style.SUCCESS(f'\n{"=" * 50}'))
        self.stdout.write(self.style.SUCCESS('IMPORTATION SUMMARY'))
        self.stdout.write(self.style.SUCCESS(f'{"=" * 50}'))
        self.stdout.write(self.style.SUCCESS(f'Actors created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Actors skipped: {skipped_count}'))

        if errors:
            self.stdout.write(self.style.ERROR('\nERRORS FOUND:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))

        if created_count > 0:
            self.stdout.write(self.style.SUCCESS('\nACTORS IMPORTED SUCCESSFULLY!'))
