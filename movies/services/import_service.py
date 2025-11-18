from datetime import datetime
from typing import Dict, List, Optional

from actors.models import Actor
from app.settings import logger
from core.constants import CSV_LINE_LIMIT
from core.utils.file_readers.file_reader import FileReader
from genres.models import Genre
from movies.models import Movie


class MovieImportService:
    def __init__(self, file_path: str, file_reader: FileReader) -> None:
        self.file_path = file_path
        self.file_reader = file_reader
        self.created_count = 0
        self.skipped_count = 0
        self.errors: List[str] = []

    def __validate_title(self, title: str, row_num: int) -> bool:
        if not title:
            self.errors.append(f'Line {row_num + 1}: Title is required')
            self.skipped_count += 1
            return False
        return True

    def __validate_genre(self, genre_name: str, row_num: int) -> Optional[Genre]:
        if not genre_name:
            self.errors.append(f'Line {row_num + 1}: Genre is required')
            self.skipped_count += 1
            return None

        try:
            return Genre.objects.get(name=genre_name)
        except Genre.DoesNotExist:
            self.errors.append(f'Line {row_num + 1}: Genre "{genre_name}" not found. Create the genre first.')
            self.skipped_count += 1
            return None

    def __parse_release_date(self, date_str: str, row_num: int) -> Optional[datetime.date]:
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
        except ValueError:
            self.errors.append(f'Line {row_num + 1}: Invalid release date. Use the format YYYY-MM-DD')
            self.skipped_count += 1
            return None

    def __validate_resume(self, resume: str, row_num: int) -> Optional[str]:
        if not resume:
            return None

        resume = resume.strip()
        if len(resume) > CSV_LINE_LIMIT:
            self.errors.append(f'Line {row_num + 1}: Resume exceeds {CSV_LINE_LIMIT} characters')
            self.skipped_count += 1
            return None

        return resume

    def __get_actors_by_names(self, actors_names: str, row_num: int) -> Optional[List[Actor]]:
        if not actors_names:
            return []

        actor_names_list = [name.strip() for name in actors_names.split(',') if name.strip()]
        actors_to_add = []

        for actor_name in actor_names_list:
            try:
                actor = Actor.objects.get(name=actor_name)
                actors_to_add.append(actor)
            except Actor.DoesNotExist:
                logger.warning(f'Line {row_num + 1}: Actor "{actor_name}" not found. Skipping...')

        return actors_to_add

    def __process_row(self, row: Dict[str, str], row_num: int) -> Optional[Movie]:
        try:
            title = row.get('title', '').strip()
            if not self.__validate_title(title, row_num):
                return None

            genre_name = row.get('genre', '').strip()
            genre = self.__validate_genre(genre_name, row_num)
            if not genre:
                return None

            release_date = self.__parse_release_date(row.get('release_date', ''), row_num)
            if release_date is None and row.get('release_date'):
                return None

            resume = self.__validate_resume(row.get('resume', ''), row_num)
            if resume is None and row.get('resume'):
                return None

            movie = Movie.objects.create(title=title, genre=genre, release_date=release_date, resume=resume)

            actors_names = row.get('actors', '').strip()
            actors_to_add = self.__get_actors_by_names(actors_names, row_num)
            if actors_to_add:
                movie.actors.set(actors_to_add)

            self.created_count += 1
            logger.info(f'Movie created: {title}')
            return movie

        except Exception as e:
            self.errors.append(f'Row {row_num + 1}: Unexpected error - {str(e)}')
            self.skipped_count += 1
            logger.error(f'Error processing row {row_num + 1}: {str(e)}')
            return None

    def import_movies(self) -> Dict:
        logger_data = {
            'service': 'MovieImportService',
            'method': 'import_movies',
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


import_service = MovieImportService
