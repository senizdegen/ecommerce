package com.senizdegen.ecommerce.order;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.jspecify.annotations.Nullable;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class OrderService {
    public Integer createOrder(@Valid OrderRequest request) {
        //check the customer --> OpenFeign

        //purchase the products --> product-ms

        //persist order

        //persist order lines

        //start payment process

        //send the order confirmation --> notification-ms (kafka)
        return null;
    }
}
