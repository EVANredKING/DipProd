package org.example.service;

import org.example.model.User;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Сервис для управления пользователями
 */
public class UserService {
    private final Map<Integer, User> users = new HashMap<>();
    private final AtomicInteger idGenerator = new AtomicInteger(1);
    
    /**
     * Конструктор, инициализирующий сервис с тестовыми данными
     */
    public UserService() {
        // Добавляем нескольких тестовых пользователей
        addUser(new User(idGenerator.getAndIncrement(), "user1", "user1@example.com"));
        addUser(new User(idGenerator.getAndIncrement(), "user2", "user2@example.com"));
    }
    
    /**
     * Получает всех пользователей
     * 
     * @return Список всех пользователей
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(users.values());
    }
    
    /**
     * Находит пользователя по ID
     * 
     * @param id ID пользователя
     * @return Пользователь или null, если не найден
     */
    public User getUserById(int id) {
        return users.get(id);
    }
    
    /**
     * Добавляет нового пользователя
     * 
     * @param user Данные пользователя
     * @return Созданный пользователь
     */
    public User addUser(User user) {
        if (user.getId() == 0) {
            user.setId(idGenerator.getAndIncrement());
        }
        users.put(user.getId(), user);
        return user;
    }
    
    /**
     * Обновляет данные пользователя
     * 
     * @param id ID пользователя
     * @param user Новые данные пользователя
     * @return Обновленный пользователь или null, если пользователь не найден
     */
    public User updateUser(int id, User user) {
        if (!users.containsKey(id)) {
            return null;
        }
        
        user.setId(id);
        users.put(id, user);
        return user;
    }
    
    /**
     * Удаляет пользователя
     * 
     * @param id ID пользователя
     * @return true, если пользователь успешно удален
     */
    public boolean deleteUser(int id) {
        return users.remove(id) != null;
    }
} 