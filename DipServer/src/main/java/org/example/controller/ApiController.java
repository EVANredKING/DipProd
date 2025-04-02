package org.example.controller;

import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * Контроллер для обработки API запросов
 */
public class ApiController {
    
    /**
     * Обрабатывает GET запросы
     * 
     * @param exchange HTTP обмен
     * @return Ответ для клиента
     */
    public String handleGetRequest(HttpExchange exchange) {
        String path = exchange.getRequestURI().getPath();
        Map<String, String> queryParams = parseQueryParams(exchange.getRequestURI().getQuery());
        
        // Обработка разных эндпоинтов
        if (path.equals("/api/status")) {
            return "Статус сервера: РАБОТАЕТ";
        } else if (path.equals("/api/info")) {
            return "Информация о сервере: Java HTTP Server v1.0";
        } else {
            return "Эндпоинт не найден: " + path;
        }
    }
    
    /**
     * Обрабатывает POST запросы
     * 
     * @param exchange HTTP обмен
     * @return Ответ для клиента
     */
    public String handlePostRequest(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        String requestBody = readRequestBody(exchange);
        
        // Обработка разных эндпоинтов
        if (path.equals("/api/echo")) {
            return "Полученные данные: " + requestBody;
        } else if (path.equals("/api/submit")) {
            return "Данные успешно отправлены: " + requestBody;
        } else {
            return "Эндпоинт не найден: " + path;
        }
    }
    
    /**
     * Считывает тело запроса
     * 
     * @param exchange HTTP обмен
     * @return Содержимое тела запроса
     */
    private String readRequestBody(HttpExchange exchange) throws IOException {
        try (InputStream inputStream = exchange.getRequestBody()) {
            byte[] requestBodyBytes = inputStream.readAllBytes();
            return new String(requestBodyBytes, StandardCharsets.UTF_8);
        }
    }
    
    /**
     * Парсит параметры запроса
     * 
     * @param query Строка запроса
     * @return Карта параметров
     */
    private Map<String, String> parseQueryParams(String query) {
        Map<String, String> params = new HashMap<>();
        if (query == null || query.isEmpty()) {
            return params;
        }
        
        String[] pairs = query.split("&");
        for (String pair : pairs) {
            String[] keyValue = pair.split("=");
            if (keyValue.length == 2) {
                params.put(keyValue[0], keyValue[1]);
            }
        }
        
        return params;
    }
} 