import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from sqlmodel.ext.asyncio.session import AsyncSession
from .database import get_session
from .service import UserService
from .config import Config
from .schemas import UserProfileCreateModel

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
            "user_events", aio_pika.ExchangeType.TOPIC, durable=True
        )

        self.queue = await self.channel.declare_queue(
            "user_created_queue",
            durable=True
        )

        await self.queue.bind(self.exchange, routing_key="user.created")

    async def consume(self):
        await self.queue.consume(self.process_message)

    async def close(self):
        if self.connection:
            await self.connection.close()

    import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from .database import AsyncSessionLocal
from .service import UserService
from .config import Config
from .schemas import UserProfileCreateModel

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

    async def consume(self):
        await self.queue.consume(self.process_message)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def process_message(self, message: AbstractIncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())

            user_profile_dict = {
                "uid": data["uid"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
            }

            async with AsyncSessionLocal() as session:
                user_profile_exists = await self.user_service.user_profile_exists(
                    user_profile_dict["email"], session
                )

                if user_profile_exists:
                    return

                new_user_profile = UserProfileCreateModel(**user_profile_dict)

                await self.user_service.create_user(new_user_profile, session)
