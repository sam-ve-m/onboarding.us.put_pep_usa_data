from decouple import config
from etria_logger import Gladsheim

from func.src.domain.exceptions.model import InternalServerError
from func.src.domain.models.user_data.model import UserData
from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


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
    async def update_user(cls, user_data: UserData):
        user_filter = {"unique_id": user_data.unique_id}
        try:
            collection = await cls.__get_collection()
            await collection.update_one(
                user_filter, {"$set": user_data.get_data_representation()}
            )
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message="UserRepository::update_user::Failed to update user",
                query=user_filter,
            )
            raise InternalServerError("Error updating user data")

    @classmethod
    async def verify_if_user_has_suitability(cls, user_data: UserData) -> bool:
        user_filter = {"unique_id": user_data.unique_id}
        try:
            collection = await cls.__get_collection()
            user_suitability = await collection.find_one(
                user_filter, {"suitability": True}
            )
            if user_suitability.get("suitability"):
                return True
            return False

        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message="UserRepository::verify_if_user_has_suitability::Failed to get user risk profile",
                query=user_filter,
            )
            raise InternalServerError("Error updating user data")
