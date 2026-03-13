package com.senizdegen.ecommerce.notification;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface NotificationRepository extends MongoRepository<Notification, Integer> {
}
