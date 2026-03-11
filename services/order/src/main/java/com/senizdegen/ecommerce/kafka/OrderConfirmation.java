package com.senizdegen.ecommerce.kafka;

import com.senizdegen.ecommerce.customer.CustomerResponse;
import com.senizdegen.ecommerce.order.PaymentMethod;
import com.senizdegen.ecommerce.product.PurchaseResponse;

import java.math.BigDecimal;
import java.util.List;

public record OrderConfirmation(
        String orderReference,
        BigDecimal totalAmount,
        PaymentMethod paymentMethod,
        CustomerResponse customer,
        List<PurchaseResponse> products
) {
}
