package com.senizdegen.ecommerce.order;

import com.senizdegen.ecommerce.customer.CustomerClient;
import com.senizdegen.ecommerce.exception.BusinessException;
import com.senizdegen.ecommerce.orderline.OrderLineRequest;
import com.senizdegen.ecommerce.orderline.OrderLineService;
import com.senizdegen.ecommerce.product.ProductClient;
import com.senizdegen.ecommerce.product.PurchaseRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository repository;
    private final CustomerClient customerClient;
    private final ProductClient productClient;
    private final OrderMapper mapper;
    private final OrderLineService orderLineService;
    public Integer createOrder(@Valid OrderRequest request) {
        var customer = this.customerClient.findCustomerById(request.customerId())
                .orElseThrow(() -> new BusinessException("Can not create order:: No customer exists with ID:: " + request.customerId()));

        this.productClient.purchaseProducts(request.products());

        var order = this.repository.save(mapper.toOrder(request));

        for (PurchaseRequest purchaseRequest : request.products()){
            orderLineService.saveOrderLine(
                    new OrderLineRequest(
                            null,
                            order.getId(),
                            purchaseRequest.productId(),
                            purchaseRequest.quantity()
                    )
            );
        }

        //todo start payment process

        //send the order confirmation --> notification-ms (kafka)
        return null;
    }
}
