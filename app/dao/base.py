from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        """
        Асинхронно создает новый экземпляр модели с указанными значениями.

        Аргументы:
            **values: Именованные параметры для создания нового экземпляра модели.

        Возвращает:
            Созданный экземпляр модели.
        """
        with async_session_maker() as session:
            with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def add_many(cls, instances: list[dict]):
        """
        Асинхронно создает несколько новых экземпляров модели с указанными значениями.

        Аргументы:
            instances: Список словарей, где каждый словарь содержит именованные параметры для создания нового
            экземпляра модели.

        Возвращает:
            Список созданных экземпляров модели.
        """
        with async_session_maker() as session:
            with session.begin():
                new_instances = [cls.model(**values) for values in instances]
                session.add_all(new_instances)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return new_instances

    @classmethod
    async def update(cls, filter_by, **values):
        """
        Асинхронно обновляет экземпляры модели, удовлетворяющие критериям фильтрации, указанным в filter_by,
        новыми значениями, указанными в values.

        Аргументы:
            filter_by: Критерии фильтрации в виде именованных параметров.
            **values: Именованные параметры для обновления значений экземпляров модели.

        Возвращает:
            Количество обновленных экземпляров модели.
        """
        with async_session_maker() as session:
            with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = session.execute(query)
                try:

                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        """
        Асинхронно удаляет экземпляры модели, удовлетворяющие критериям фильтрации, указанным в filter_by.

        Аргументы:
            delete_all: Если True, удаляет все экземпляры модели без фильтрации.
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Количество удаленных экземпляров модели.
        """
        if delete_all is False:
            if not filter_by:
                raise ValueError("Необходимо указать хотя бы один параметр для удаления.")

        with async_session_maker() as session:
            with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = session.execute(query)
                try:
                    session.commit()
                except SQLAlchemyError as e:
                    session.rollback()
                    raise e
                return result.rowcount
