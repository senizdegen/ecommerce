import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from .database import AsyncSessionLocal
from .service import FeedService
from .config import Config
from .schemas import ProductCreateModel, ProductUpdateModel

RABBIT_URL = Config.RABBIT_URL

class ProductConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
        self.feed_service = FeedService()

    async def connect(self):
        self.connection = await aio_pika.connect_robust(RABBIT_URL)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

        self.exchange = await self.channel.declare_exchange(
            "product_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        self.queue = await self.channel.declare_queue(
            "feed_product_queue",
            durable=True
        )

        await self.queue.bind(self.exchange, routing_key="product.created")
        await self.queue.bind(self.exchange, routing_key="product.updated")

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

                if routing_key == "product.created":
                    await self.handle_created(data, session)

                elif routing_key == "product.updated":
                    await self.handle_updated(data, session)

    async def handle_created(self, data, session):
        product_dict = {
            "product_uid": data["product_uid"],
            "name": data["name"],
            "description": data["description"],
            "price": data["price"],
            "available_quantity": data["available_quantity"],
            "image_url": data.get("image_url"),  # может быть None если фото нет
        }

        new_product = ProductCreateModel(**product_dict)

        await self.feed_service.create_product(
            session=session,
            product_data=new_product
        )
        return new_product

    async def handle_updated(self, data, session):
        update_data = ProductUpdateModel(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            image_url=data.get("image_url"),  # может быть None если фото не менялось
        )

        updated_product = await self.feed_service.update_product(
            session=session,
            product_uid=data["product_uid"],
            product_data=update_data
        )

        return updated_product