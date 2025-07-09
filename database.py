from motor.motor_asyncio import AsyncIOMotorClient
def get_session():

    try:
        return AsyncIOMotorClient("mongodb://dev:dev@172.20.0.2:27017/")

    except Exception as e:
        raise Exception(e)