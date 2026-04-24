import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from .database import AsyncSessionLocal
from .service import UserService
from .config import Config
from .schemas import UserProfileCreateModel, UserProfileUpdateModel

RABBIT_URL = Config.RABBIT_URL


class UserCreatedConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
        self.user_service = UserService()

    async def connect(self):
        self.connection = await aio_pika.connect_robust(RABBIT_URL)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        self.exchange = await self.channel.declare_exchange(
            "user_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )
        self.queue = await self.channel.declare_queue(
            "user_created_queue",
            durable=True,
        )
        await self.queue.bind(self.exchange, routing_key="user.created")
        await self.queue.bind(self.exchange, routing_key="user.updated")
        await self.queue.bind(self.exchange, routing_key="user.deleted")

    async def consume(self):
        await self.queue.consume(self.process_message)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def process_message(self, message: AbstractIncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())
            routing_key = message.routing_key

            async with AsyncSessionLocal() as session:
                if routing_key == "user.created":
                    await self.handle_created(data, session)
                elif routing_key == "user.updated":
                    await self.handle_updated(data, session)
                elif routing_key == "user.deleted":
                    await self.handle_deleted(data, session)

    async def handle_created(self, data, session):
        user_profile_exists = await self.user_service.user_profile_exists(data["email"], session)
        if user_profile_exists:
            return
        new_user_profile = UserProfileCreateModel(
            uid=data["uid"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            is_admin=data.get("is_admin", False),
        )
        await self.user_service.create_user(new_user_profile, session)

    async def handle_updated(self, data, session):
        update_data = UserProfileUpdateModel(
            email=data.get("email"),
            is_admin=data.get("is_admin"),
        )
        await self.user_service.update_user(data["uid"], update_data, session)

    async def handle_deleted(self, data, session):
        await self.user_service.delete_user(data["uid"], session)