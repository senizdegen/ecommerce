import json
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from .database import AsyncSessionLocal
from .service import InventoryService
from .config import Config
from .schemas import InventoryCreate

RABBIT_URL = Config.RABBIT_URL

class ProductCreatedConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
        self.inventory_service = InventoryService()
    
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
            "inventory_product_created_queue",
            durable=True
        )

        await self.queue.bind(self.exchange, routing_key="product.created")
        await self.queue.bind(self.exchange, routing_key="product.deleted")  # добавить

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
                elif routing_key == "product.deleted":
                    await self.handle_deleted(data, session)

    async def handle_created(self, data, session):
        inventory_dict = {
            "product_uid": data["product_uid"],
            "available_quantity": data["available_quantity"]
        }
        new_inventory = InventoryCreate(**inventory_dict)
        await self.inventory_service.create_inventory(session=session, data=new_inventory)

    async def handle_deleted(self, data, session):
        await self.inventory_service.delete_inventory(session=session, product_uid=data["product_uid"])