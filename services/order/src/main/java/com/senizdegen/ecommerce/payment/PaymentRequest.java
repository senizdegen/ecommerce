package com.senizdegen.ecommerce.payment;

import com.senizdegen.ecommerce.customer.CustomerResponse;
import com.senizdegen.ecommerce.order.PaymentMethod;

import java.math.BigDecimal;

public record PaymentRequest(
        BigDecimal amount,
        PaymentMethod paymentMethod,
        Integer orderId,
        String orderReference,
        CustomerResponse customer
) {
}
