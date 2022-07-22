from decouple import config
from etria_logger import Gladsheim

from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::__get_collection::Error when trying to get collection"
            )
            Gladsheim.error(
                error=ex,
                message=message,
                database=cls.database,
                collection=cls.collection,
            )
            raise ex

    @classmethod
    async def update_user(cls, unique_id: str, new: dict, upsert: bool = False) -> bool:
        user_filter = {"unique_id": unique_id}
        try:
            collection = await cls.__get_collection()
            await collection.update_one(user_filter, {"$set": new}, upsert=upsert)
            return True
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message="UserRepository::update_user::Failed to update user",
                query=user_filter,
            )
            return False
