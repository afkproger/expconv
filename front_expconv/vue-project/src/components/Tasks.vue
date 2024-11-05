<template>
  <div>
    <header>
      <span class="username-container" @click="fetchUserInfo">
        {{ username || 'Профиль' }}
      </span>
    </header>

    <h1>Опросники пользователя</h1>

    <!-- Кнопка для перехода к настройкам задачи -->
    <button @click="goToTaskSettings" class="settings-button">
      Создать новый опросник
    </button>

    <!-- Список задач -->
    <div v-if="tasks.length" class="tasks-list">
      <ul>
        <li v-for="task in tasks" :key="task.id">
          <h3>{{ task.name }}</h3>
          <p>{{ task.description }}</p>

          <!-- Кнопки для действий с задачей -->
          <button @click="viewTaskSettings(task.id)" class="action-button">Посмотреть настройки задачи</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Задачи не найдены.</p>
    </div>

    <!-- Модальное окно для отображения информации о пользователе -->
    <div v-if="showUserModal" class="modal">
      <div class="modal-content">
        <span @click="showUserModal = false" class="close">&times;</span>
        <h2>Профиль пользователя</h2>
        <p><strong>Имя пользователя:</strong> {{ userInfo.username }}</p>
        <p><strong>Имя:</strong> {{ userInfo.first_name }}</p>
        <p><strong>Фамилия:</strong> {{ userInfo.last_name }}</p>
        <p><strong>Телефон:</strong> {{ userInfo.tel }}</p>
        <p><strong>Email:</strong> {{ userInfo.email }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      tasks: [],
      showUserModal: false,
      userInfo: {}
    };
  },
  async mounted() {
    this.username = localStorage.getItem('username') || '';
    await this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) {
          console.warn('Токен отсутствует. Пожалуйста, войдите в систему.');
          return;
        }

        const response = await fetch('http://127.0.0.1:8000/api/v1/tasks/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          if (data.length && data[0].tasks) {
            this.tasks = data[0].tasks;
          } else {
            console.warn('Формат данных отличается от ожидаемого.');
          }
        } else {
          console.error('Ошибка при получении задач:', response.statusText);
        }
      } catch (error) {
        console.error('Ошибка при отправке запроса:', error);
      }
    },
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch('http://127.0.0.1:8000/api/v1/userinfo', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          }
        });

        if (response.ok) {
          this.userInfo = await response.json();
          this.showUserModal = true;
        } else {
          console.error('Ошибка при получении информации о пользователе:', response.statusText);
        }
      } catch (error) {
        console.error('Ошибка при отправке запроса:', error);
      }
    },
    goToTaskSettings() {
      this.$router.push({ name: 'TaskSettings' });
    },
    viewTaskSettings(taskId) {
      // Переход к настройкам задачи, используя taskId
      this.$router.push({ name: 'TaskSettings', params: { id: taskId } });
    }
  }
};
</script>
  
  <style scoped>

.action-button {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.action-button:hover {
  background-color: #1e88e5;
}
  header {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 10px;
  }
  
  .username-container {
    display: inline-block;
    padding: 10px 15px;
    background-color: #f5f5f5;
    border-radius: 5px;
    cursor: pointer;
    margin-right: 20px;
    font-weight: bold;
  }
  
  .settings-button {
    margin: 20px 0;
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .settings-button:hover {
    background-color: #45a049;
  }
  
  .tasks-list ul {
    padding-left: 0;
    list-style-type: none; /* Убираем маркеры списка */
    margin: 0;
  }
  
  .tasks-list li {
    margin: 10px 0;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
    position: relative;
  }
  
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    font-weight: bold;
    color: red;
    cursor: pointer;
    transition: color 0.3s;
  }
  
  .close:hover {
    color: darkred;
  }
  </style>
  