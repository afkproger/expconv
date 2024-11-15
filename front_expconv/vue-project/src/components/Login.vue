<template>
  <div class="login-container">
    <h1>Вход</h1>
    <form @submit.prevent="loginUser">
      <label for="username">Имя пользователя:</label>
      <input v-model="loginData.username" type="text" id="username" required />

      <label for="password">Пароль:</label>
      <input v-model="loginData.password" type="password" id="password" required />

      <button type="submit">Войти</button>
    </form>

    <p v-if="loginMessage">{{ loginMessage }}</p>

    <p>
      Нет аккаунта? 
      <router-link to="/register">Зарегистрируйтесь</router-link>
    </p>
  </div>
</template>

<script>
import config from '@/config.js';
export default {
  data() {
    return {
      loginData: {
        username: this.$route.query.username || '',  // Получаем username из query
        password: this.$route.query.password || ''   // Получаем password из query
      },
      loginMessage: ''
    };
  },
  methods: {
  async loginUser() {
    try {
      const response = await fetch(`${config.apiBaseUrl}auth/token/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.loginData)
      });

      if (response.ok) {
        const result = await response.json();
        this.loginMessage = 'Успешный вход!';
        console.log('Success:', result);

        // Сохранение токена в localStorage
        if (result.auth_token) {
          localStorage.setItem('auth_token', result.auth_token);
          localStorage.setItem('username' , this.loginData.username)

          // Перенаправление на страницу с задачами
          this.$router.push('/tasks');
        } else {
          console.warn('Токен не получен');
        }
      } else {
        const error = await response.json();
        this.loginMessage = `Ошибка: ${error.detail || 'Проверьте введенные данные.'}`;
      }
    } catch (error) {
      console.error('Ошибка при отправке запроса:', error);
      this.loginMessage = 'Произошла ошибка при соединении с сервером.';
    }
  }
}
};
</script>
  
  <style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  margin: auto;
  padding: 50px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

label {
  margin-top: 10px;
  margin-bottom: 5px; /* Добавлен нижний отступ */
  font-weight: bold; /* Сделать текст меток жирным */
}

input {
  width: 100%; /* Занять всю ширину контейнера */
  padding: 10px; /* Добавить внутренний отступ для удобства */
  border: 1px solid #ccc;
  border-radius: 5px; /* Закруглённые углы */
  margin-bottom: 15px; /* Добавлен нижний отступ для разделения полей */
}

button {
  margin-top: 10px; /* Уменьшение отступа сверху */
  padding: 10px 15px; /* Добавлен внутренний отступ для кнопки */
  border: none;
  border-radius: 5px; /* Закруглённые углы */
  background-color: #007bff; /* Цвет фона кнопки */
  color: white; /* Цвет текста кнопки */
  cursor: pointer; /* Изменение курсора при наведении */
}

button:hover {
  background-color: #0056b3; /* Темнее при наведении */
}

p {
  margin-top: 10px; /* Отступ для параграфов */
}
</style>
