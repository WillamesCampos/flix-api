import pandas as pd

from app.settings import logger

from .file_reader import FileReader


class ExcelReader(FileReader):
    def read(self, file_path: str) -> list[dict]:
        logger_data = {
            'service': 'ExcelReader',
            'method': 'read',
            'file_path': file_path,
        }
        logger.info(logger_data)
        try:
            df = pd.read_excel(file_path)
            return df.to_dict(orient='records')
        except Exception as e:
            logger.error(logger_data, exc_info=True)
            raise e
