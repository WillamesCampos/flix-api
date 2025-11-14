import csv
from datetime import datetime
from typing import Dict, List

from actors.models import Actor
from app.settings import logger
from core.constants import CSV_LINE_LIMIT
from genres.models import Genre
from movies.models import Movie


class MovieImportService:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.created_count = 0
        self.skipped_count = 0
        self.errors: List[str] = []

    def __validate_title(self, title: str, row_num: int) -> bool:
        """Valida se o título foi fornecido."""
        if not title:
            self.errors.append(f'Linha {row_num}: Título é obrigatório')
            self.skipped_count += 1
            return False
        return True

    def __validate_genre(self, genre_name: str, row_num: int) -> Genre | None:
        """Valida e retorna o gênero se existir."""
        if not genre_name:
            self.errors.append(f'Linha {row_num}: Gênero é obrigatório')
            self.skipped_count += 1
            return None

        try:
            return Genre.objects.get(name=genre_name)
        except Genre.DoesNotExist:
            self.errors.append(f'Linha {row_num}: Gênero "{genre_name}" não encontrado. Crie o gênero primeiro.')
            self.skipped_count += 1
            return None

    def __parse_release_date(self, date_str: str, row_num: int) -> datetime.date | None:
        """Parse da data de lançamento."""
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
        except ValueError:
            self.errors.append(f'Linha {row_num}: Data de lançamento inválida. Use o formato YYYY-MM-DD')
            self.skipped_count += 1
            return None

    def __validate_resume(self, resume: str, row_num: int) -> str | None:
        """Valida o resumo do filme."""
        if not resume:
            return None

        resume = resume.strip()
        if len(resume) > CSV_LINE_LIMIT:
            self.errors.append(f'Linha {row_num}: Resumo excede {CSV_LINE_LIMIT} caracteres')
            self.skipped_count += 1
            return None

        return resume

    def __get_actors_by_names(self, actors_names: str, row_num: int) -> List[Actor]:
        """Busca atores pelos nomes fornecidos."""
        if not actors_names:
            return []

        actor_names_list = [name.strip() for name in actors_names.split(',') if name.strip()]
        actors_to_add = []

        for actor_name in actor_names_list:
            try:
                actor = Actor.objects.get(name=actor_name)
                actors_to_add.append(actor)
            except Actor.DoesNotExist:
                logger.warning(f'Linha {row_num}: Ator "{actor_name}" não encontrado. Pulando...')

        return actors_to_add

    def __process_row(self, row: Dict[str, str], row_num: int) -> Movie | None:
        """Processa uma linha do CSV e cria o filme se válido."""
        try:
            # Campos obrigatórios
            title = row.get('title', '').strip()
            if not self.__validate_title(title, row_num):
                return None

            genre_name = row.get('genre', '').strip()
            genre = self.__validate_genre(genre_name, row_num)
            if not genre:
                return None

            # Campos opcionais
            release_date = self.__parse_release_date(row.get('release_date', ''), row_num)
            if release_date is None and row.get('release_date'):
                return None  # Erro no parse da data

            resume = self.__validate_resume(row.get('resume', ''), row_num)
            if resume is None and row.get('resume'):
                return None  # Erro na validação do resumo

            # Criar o filme
            movie = Movie.objects.create(title=title, genre=genre, release_date=release_date, resume=resume)

            # Associar atores (se houver)
            actors_names = row.get('actors', '').strip()
            actors_to_add = self.__get_actors_by_names(actors_names, row_num)
            if actors_to_add:
                movie.actors.set(actors_to_add)

            self.created_count += 1
            logger.info(f'Filme criado: {title}')
            return movie

        except Exception as e:
            self.errors.append(f'Linha {row_num}: Erro inesperado - {str(e)}')
            self.skipped_count += 1
            logger.error(f'Erro ao processar linha {row_num}: {str(e)}')
            return None

    def import_movies(self) -> Dict[str, int | List[str]]:
        """
        Importa filmes do arquivo CSV.

        Returns:
            Dict com created_count, skipped_count e errors
        """
        logger_data = {
            'service': 'MovieImportService',
            'method': 'import_movies',
            'file_path': self.file_path,
        }
        logger.info(logger_data)

        with open(self.file_path, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=2):  # start=2 porque linha 1 é o cabeçalho
                self.__process_row(row, row_num)

        return {
            'created_count': self.created_count,
            'skipped_count': self.skipped_count,
            'errors': self.errors,
        }


import_service = MovieImportService
