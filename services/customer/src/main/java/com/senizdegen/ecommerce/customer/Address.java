package com.senizdegen.ecommerce.customer;

import org.springframework.validation.annotation.Validated;
import lombok.*;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@Getter
@Setter
@Validated
public class Address {
    private String street;
    private String houseNumber;
    private String zipCode;
}
