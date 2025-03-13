package org.example;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import org.example.controller.ApiController;
import org.example.controller.UserController;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.concurrent.Executors;

public class Main {
    public static void main(String[] args) throws IOException {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        
        // Добавляем контексты для обработки запросов
        server.createContext("/", new RootHandler());
        server.createContext("/api", new ApiHandler());
        server.createContext("/api/users", new UserHandler());
        
        // Устанавливаем пул потоков для обработки запросов
        server.setExecutor(Executors.newFixedThreadPool(10));
        
        // Запускаем сервер
        server.start();
        
        System.out.println("Сервер запущен на порту " + port);
    }
    
    // Обработчик для корневого пути
    static class RootHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = "Добро пожаловать на сервер!";
            sendResponse(exchange, response, 200);
        }
    }
    
    // Обработчик для API запросов
    static class ApiHandler implements HttpHandler {
        private final ApiController apiController = new ApiController();
        
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // Обрабатываем CORS preflight запросы
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                handleCors(exchange);
                return;
            }
            
            // Добавляем CORS заголовки
            addCorsHeaders(exchange);
            
            String method = exchange.getRequestMethod();
            String path = exchange.getRequestURI().getPath();
            
            // Пропускаем обработку запросов к /api/users, так как они обрабатываются UserHandler
            if (path.startsWith("/api/users")) {
                return;
            }
            
            String response;
            int statusCode = 200;
            
            try {
                if ("GET".equals(method)) {
                    response = apiController.handleGetRequest(exchange);
                } else if ("POST".equals(method)) {
                    response = apiController.handlePostRequest(exchange);
                } else {
                    response = "Метод не поддерживается: " + method;
                    statusCode = 405;
                }
            } catch (Exception e) {
                response = "Ошибка сервера: " + e.getMessage();
                statusCode = 500;
                e.printStackTrace();
            }
            
            sendJsonResponse(exchange, response, statusCode);
        }
    }
    
    // Обработчик для запросов к API пользователей
    static class UserHandler implements HttpHandler {
        private final UserController userController = new UserController();
        
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // Обрабатываем CORS preflight запросы
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                handleCors(exchange);
                return;
            }
            
            // Добавляем CORS заголовки
            addCorsHeaders(exchange);
            
            String method = exchange.getRequestMethod();
            String response;
            int statusCode = 200;
            
            try {
                if ("GET".equals(method)) {
                    response = userController.handleGetRequest(exchange);
                } else if ("POST".equals(method)) {
                    response = userController.handlePostRequest(exchange);
                    statusCode = 201;
                } else if ("PUT".equals(method)) {
                    response = userController.handlePutRequest(exchange);
                } else if ("DELETE".equals(method)) {
                    response = userController.handleDeleteRequest(exchange);
                } else {
                    response = "Метод не поддерживается: " + method;
                    statusCode = 405;
                }
                
                // Проверяем, был ли установлен статус в заголовках
                String statusHeader = exchange.getResponseHeaders().getFirst("Status");
                if (statusHeader != null) {
                    statusCode = Integer.parseInt(statusHeader);
                    exchange.getResponseHeaders().remove("Status");
                }
            } catch (Exception e) {
                response = "Ошибка сервера: " + e.getMessage();
                statusCode = 500;
                e.printStackTrace();
            }
            
            sendJsonResponse(exchange, response, statusCode);
        }
    }
    
    // Обработчик CORS preflight запросов
    private static void handleCors(HttpExchange exchange) throws IOException {
        addCorsHeaders(exchange);
        exchange.sendResponseHeaders(204, -1);
        exchange.close();
    }
    
    // Добавляет CORS заголовки
    private static void addCorsHeaders(HttpExchange exchange) {
        exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }
    
    // Вспомогательный метод для отправки текстового ответа
    private static void sendResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        byte[] responseBytes = response.getBytes();
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
    
    // Вспомогательный метод для отправки JSON ответа
    private static void sendJsonResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        byte[] responseBytes = response.getBytes();
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(statusCode, responseBytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(responseBytes);
        }
    }
}
