import json
import aio_pika
from aio_pika import Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None
        self.exchange = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        self.exchange = await self.channel.declare_exchange(
            "product_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def _publish(self, payload: dict, routing_key: str):
        if not self.exchange:
            raise RuntimeError("RabbitMQ exchange is not initialized")
        body = json.dumps(payload).encode()
        message = Message(
            body=body,
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT
        )
        await self.exchange.publish(message, routing_key=routing_key)

    async def publish_product_created(self, payload: dict):
        await self._publish(payload, "product.created")

    async def publish_product_updated(self, payload: dict):
        await self._publish(payload, "product.updated")

    async def publish_product_deleted(self, payload: dict):
        await self._publish(payload, "product.deleted")