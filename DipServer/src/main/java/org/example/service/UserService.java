package org.example.service;

import org.example.model.User;
import org.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

/**
 * Сервис для управления пользователями
 */
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    /**
     * Получает всех пользователей
     * 
     * @return Список всех пользователей
     */
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    /**
     * Находит пользователя по ID
     * 
     * @param id ID пользователя
     * @return Пользователь или null, если не найден
     */
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }
    
    /**
     * Добавляет нового пользователя
     * 
     * @param user Данные пользователя
     * @return Созданный пользователь
     */
    public User addUser(User user) {
        return userRepository.save(user);
    }
    
    /**
     * Обновляет данные пользователя
     * 
     * @param id ID пользователя
     * @param user Новые данные пользователя
     * @return Обновленный пользователь или null, если пользователь не найден
     */
    public Optional<User> updateUser(Long id, User user) {
        return userRepository.findById(id)
            .map(existingUser -> {
                existingUser.setUsername(user.getUsername());
                existingUser.setEmail(user.getEmail());
                if (user.getPassword() != null) {
                    existingUser.setPassword(user.getPassword());
                }
                return userRepository.save(existingUser);
            });
    }
    
    /**
     * Удаляет пользователя
     * 
     * @param id ID пользователя
     * @return true, если пользователь успешно удален
     */
    public boolean deleteUser(Long id) {
        if (userRepository.existsById(id)) {
            userRepository.deleteById(id);
            return true;
        }
        return false;
    }
} 