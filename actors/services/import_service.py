from datetime import datetime
from typing import Dict, List, Optional

from actors.models import NATIONALITY_CHOICES, Actor
from app.settings import logger
from core.utils.file_readers.file_reader import FileReader


class ActorImportService:
    def __init__(self, file_path: str, file_reader: FileReader) -> None:
        self.file_path = file_path
        self.file_reader = file_reader
        self.created_count = 0
        self.skipped_count = 0
        self.errors: List[str] = []

    def __validate_name(self, name: str, row_num: int) -> bool:
        if not name:
            self.errors.append(f'Line {row_num + 1}: Name is required')
            self.skipped_count += 1
            return False
        return True

    def __validate_birthday(self, birthday: str, row_num: int) -> bool:
        try:
            birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
            if birthday_date > datetime.now().date():
                self.errors.append(f'Line {row_num + 1}: Birthday cannot be in the future')
                self.skipped_count += 1
                return False
        except ValueError:
            self.errors.append(f'Line {row_num + 1}: Invalid birthday. Must be in the format YYYY-MM-DD')
            self.skipped_count += 1
            return False
        return True

    def __validate_nationality(self, nationality: str, row_num: int) -> bool:
        if nationality:
            nationalities = [choice[0] for choice in NATIONALITY_CHOICES]
            if nationality not in nationalities:
                self.errors.append(f'Line {row_num + 1}: Invalid nationality. Must be one of: {", ".join(nationalities)}')
                self.skipped_count += 1
                return False
        return True

    def __process_row(self, row: Dict[str, str], row_num: int) -> Optional[Actor]:
        try:
            name = row.get('name', '').strip()
            if not self.__validate_name(name, row_num):
                return None

            birthday = row.get('birthday', '').strip()
            if not self.__validate_birthday(birthday, row_num):
                return None

            nationality = row.get('nationality', '').strip()
            if not self.__validate_nationality(nationality, row_num):
                return None

            actor = Actor.objects.create(name=name, birthday=birthday, nationality=nationality)
            self.created_count += 1
            logger.info(f'Actor created: {actor.name}')
            return actor
        except Exception as e:
            self.errors.append(f'Row {row_num + 1}: Unexpected error - {str(e)}')
            self.skipped_count += 1
            logger.error(f'Error processing row {row_num + 1}: {str(e)}')
            return None

    def import_actors(self) -> Dict:
        logger_data = {
            'service': 'ActorImportService',
            'method': 'import_actors',
            'file_path': self.file_path,
            'file_reader': self.file_reader.__class__.__name__,
        }
        logger.info(logger_data)

        rows = self.file_reader.read(self.file_path)
        for row_num, row in enumerate(rows):
            self.__process_row(row, row_num)

        return {
            'created_count': self.created_count,
            'skipped_count': self.skipped_count,
            'errors': self.errors,
        }
