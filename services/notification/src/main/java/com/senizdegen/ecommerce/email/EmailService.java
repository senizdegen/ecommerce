package com.senizdegen.ecommerce.email;

import com.senizdegen.ecommerce.kafka.order.Product;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.thymeleaf.context.Context;
import org.thymeleaf.spring6.SpringTemplateEngine;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.senizdegen.ecommerce.email.EmailTemplates.ORDER_CONFIRMATION;
import static com.senizdegen.ecommerce.email.EmailTemplates.PAYMENT_CONFIRMATION;
import static java.nio.charset.StandardCharsets.UTF_8;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmailService {

    private final JavaMailSender mailSender;
    private final SpringTemplateEngine templateEngine;

    @Async
    public void sendPaymentSuccessEmail(
            String destinationEmail,
            String customerName,
            BigDecimal amount,
            String orderReference
    ) throws MessagingException {
        MimeMessage mimeMessage = mailSender.createMimeMessage();
        MimeMessageHelper helper =
                new MimeMessageHelper(mimeMessage, MimeMessageHelper.MULTIPART_MODE_RELATED, UTF_8.name());
        helper.setFrom("contact@senizdegen.com");
        final String templateName = PAYMENT_CONFIRMATION.getTemplate();

        Map<String, Object> variables = new HashMap<>();
        variables.put("customerName", customerName);
        variables.put("amount", amount);
        variables.put("orderReference", orderReference);
        Context context = new Context();
        context.setVariables(variables);
        helper.setSubject(PAYMENT_CONFIRMATION.getSubject());

        try{
            String htmlTemplate = templateEngine.process(templateName, context);
            helper.setText(htmlTemplate, true);

            helper.setTo(destinationEmail);
            mailSender.send(mimeMessage);
            log.info("Email sent to [{}] successfully with template [{}]", destinationEmail, templateName);
        }catch (Exception e){
            log.warn("WARNING - Can not send email to {}", destinationEmail);
        }

    }

    @Async
    public void sendOrderConfirmationEmail(
            String destinationEmail,
            String customerName,
            BigDecimal amount,
            String orderReference,
            List<Product> products
    ) throws MessagingException {
        MimeMessage mimeMessage = mailSender.createMimeMessage();
        MimeMessageHelper helper =
                new MimeMessageHelper(mimeMessage, MimeMessageHelper.MULTIPART_MODE_RELATED, UTF_8.name());
        helper.setFrom("contact@senizdegen.com");
        final String templateName = ORDER_CONFIRMATION.getTemplate();

        Map<String, Object> variables = new HashMap<>();
        variables.put("customerName", customerName);
        variables.put("totalAmount", amount);
        variables.put("orderReference", orderReference);
        variables.put("products", products);
        Context context = new Context();
        context.setVariables(variables);
        helper.setSubject(ORDER_CONFIRMATION.getSubject());

        try{
            String htmlTemplate = templateEngine.process(templateName, context);
            helper.setText(htmlTemplate, true);

            helper.setTo(destinationEmail);
            mailSender.send(mimeMessage);
            log.info("Email sent to [{}] successfully with template [{}]", destinationEmail, templateName);
        }catch (Exception e){
            log.warn("WARNING - Can not send email to {}", destinationEmail);
        }

    }
}
