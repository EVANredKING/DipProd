package org.example.controller;

import com.sun.net.httpserver.HttpExchange;
import org.example.model.User;
import org.example.service.UserService;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Контроллер для управления пользователями
 */
public class UserController {
    private final UserService userService = new UserService();
    private final Pattern userIdPattern = Pattern.compile("/api/users/(\\d+)");
    
    /**
     * Обрабатывает GET запросы для пользователей
     * 
     * @param exchange HTTP обмен
     * @return Ответ для клиента
     */
    public String handleGetRequest(HttpExchange exchange) {
        String path = exchange.getRequestURI().getPath();
        
        if ("/api/users".equals(path)) {
            // Получаем всех пользователей
            List<User> users = userService.getAllUsers();
            return formatUserListResponse(users);
        } else {
            // Ищем пользователя по ID
            Matcher matcher = userIdPattern.matcher(path);
            if (matcher.matches()) {
                int userId = Integer.parseInt(matcher.group(1));
                User user = userService.getUserById(userId);
                if (user != null) {
                    return formatUserResponse(user);
                } else {
                    exchange.getResponseHeaders().set("Status", "404");
                    return "Пользователь с ID " + userId + " не найден";
                }
            }
        }
        
        exchange.getResponseHeaders().set("Status", "404");
        return "Эндпоинт не найден: " + path;
    }
    
    /**
     * Обрабатывает POST запросы для пользователей
     * 
     * @param exchange HTTP обмен
     * @return Ответ для клиента
     */
    public String handlePostRequest(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        
        if ("/api/users".equals(path)) {
            // Создаем нового пользователя
            String requestBody = readRequestBody(exchange);
            User user = parseUserFromJson(requestBody);
            User createdUser = userService.addUser(user);
            exchange.getResponseHeaders().set("Status", "201");
            return "Пользователь создан: " + formatUserResponse(createdUser);
        }
        
        exchange.getResponseHeaders().set("Status", "404");
        return "Эндпоинт не найден: " + path;
    }
    
    /**
     * Обрабатывает PUT запросы для пользователей
     * 
     * @param exchange HTTP обмен
     * @return Ответ для клиента
     */
    public String handlePutRequest(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        Matcher matcher = userIdPattern.matcher(path);
        
        if (matcher.matches()) {
            int userId = Integer.parseInt(matcher.group(1));
            String requestBody = readRequestBody(exchange);
            User user = parseUserFromJson(requestBody);
            
            User updatedUser = userService.updateUser(userId, user);
            if (updatedUser != null) {
                return "Пользователь обновлен: " + formatUserResponse(updatedUser);
            } else {
                exchange.getResponseHeaders().set("Status", "404");
                return "Пользователь с ID " + userId + " не найден";
            }
        }
        
        exchange.getResponseHeaders().set("Status", "404");
        return "Эндпоинт не найден: " + path;
    }
    
    /**
     * Обрабатывает DELETE запросы для пользователей
     * 
     * @param exchange HTTP обмен
     * @return Ответ для клиента
     */
    public String handleDeleteRequest(HttpExchange exchange) {
        String path = exchange.getRequestURI().getPath();
        Matcher matcher = userIdPattern.matcher(path);
        
        if (matcher.matches()) {
            int userId = Integer.parseInt(matcher.group(1));
            boolean deleted = userService.deleteUser(userId);
            
            if (deleted) {
                return "Пользователь с ID " + userId + " удален";
            } else {
                exchange.getResponseHeaders().set("Status", "404");
                return "Пользователь с ID " + userId + " не найден";
            }
        }
        
        exchange.getResponseHeaders().set("Status", "404");
        return "Эндпоинт не найден: " + path;
    }
    
    /**
     * Парсит пользователя из JSON
     * 
     * @param json JSON строка
     * @return Объект пользователя
     */
    private User parseUserFromJson(String json) {
        // Простой парсер JSON (в реальном проекте лучше использовать библиотеку)
        User user = new User();
        
        if (json.contains("\"id\":")) {
            Pattern idPattern = Pattern.compile("\"id\"\\s*:\\s*(\\d+)");
            Matcher idMatcher = idPattern.matcher(json);
            if (idMatcher.find()) {
                user.setId(Integer.parseInt(idMatcher.group(1)));
            }
        }
        
        if (json.contains("\"username\":")) {
            Pattern usernamePattern = Pattern.compile("\"username\"\\s*:\\s*\"([^\"]*)\"");
            Matcher usernameMatcher = usernamePattern.matcher(json);
            if (usernameMatcher.find()) {
                user.setUsername(usernameMatcher.group(1));
            }
        }
        
        if (json.contains("\"email\":")) {
            Pattern emailPattern = Pattern.compile("\"email\"\\s*:\\s*\"([^\"]*)\"");
            Matcher emailMatcher = emailPattern.matcher(json);
            if (emailMatcher.find()) {
                user.setEmail(emailMatcher.group(1));
            }
        }
        
        return user;
    }
    
    /**
     * Форматирует ответ для одного пользователя
     * 
     * @param user Пользователь
     * @return Форматированный ответ
     */
    private String formatUserResponse(User user) {
        return String.format("{ \"id\": %d, \"username\": \"%s\", \"email\": \"%s\" }",
                user.getId(), user.getUsername(), user.getEmail());
    }
    
    /**
     * Форматирует ответ для списка пользователей
     * 
     * @param users Список пользователей
     * @return Форматированный ответ
     */
    private String formatUserListResponse(List<User> users) {
        StringBuilder sb = new StringBuilder("[\n");
        for (int i = 0; i < users.size(); i++) {
            sb.append("  ").append(formatUserResponse(users.get(i)));
            if (i < users.size() - 1) {
                sb.append(",");
            }
            sb.append("\n");
        }
        sb.append("]");
        return sb.toString();
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
} 