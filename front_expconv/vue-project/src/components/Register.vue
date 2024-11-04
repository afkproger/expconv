<template>
  <div class="container">
    <h1>Регистрация</h1>
    <form @submit.prevent="registerUser" class="registration-form">
      <label for="username">Логин пользователя:</label>
      <input v-model="formData.username" type="text" id="username" required />

      <label for="password">Пароль:</label>
      <input v-model="formData.password" type="password" id="password" required />

      <label for="re_password">Повторите пароль:</label>
      <input v-model="formData.re_password" type="password" id="re_password" required />

      <label for="first_name">Имя:</label>
      <input v-model="formData.first_name" type="text" id="first_name" required />

      <label for="last_name">Фамилия:</label>
      <input v-model="formData.last_name" type="text" id="last_name" required />

      <label for="tel">Телефон:</label>
      <input v-model="formData.tel" type="tel" id="tel" required />

      <label for="email">Электронная почта:</label>
      <input v-model="formData.email" type="email" id="email" required />

      <button type="submit">Зарегистрироваться</button>
    </form>

    <p v-if="responseMessage">{{ responseMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
        re_password: '',
        first_name: '',
        last_name: '',
        tel: '',
        email: ''
      },
      responseMessage: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/auth/users/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });

        if (response.ok) {
          const result = await response.json();
          this.responseMessage = 'Регистрация прошла успешно!';
          console.log('Success:', result);
        } else {
          const error = await response.json();
          this.responseMessage = `Ошибка: ${error.detail || 'Проверьте введенные данные.'}`;
        }
      } catch (error) {
        console.error('Ошибка при отправке запроса:', error);
        this.responseMessage = 'Произошла ошибка при соединении с сервером.';
      }
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; 
  background-color: #f9f9f9; 
}

.registration-form {
  display: flex;
  flex-direction: column;
  max-width: 400px; 
  width: 100%; 
  padding: 20px; 
  border: 1px solid #ccc; 
  border-radius: 10px; 
  background-color: #fff; 
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); 
}

label {
  margin-top: 10px;
}

input {
  border: 1px solid #ccc; 
  border-radius: 5px; 
  padding: 10px; 
  margin-top: 5px; 
}

button {
  margin-top: 15px;
  padding: 10px;
  border: none; 
  border-radius: 5px; 
  background-color: #007bff; 
  color: white; 
  cursor: pointer; 
}

button:hover {
  background-color: #0056b3; 
}

p {
  margin-top: 15px; 
  color: #d9534f; 
}
</style>
