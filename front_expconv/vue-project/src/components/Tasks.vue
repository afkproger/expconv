<template>
  <div>
    <header class = "header-with-logo">
      <img src="@/assets/fic_ran.png" alt="Логотип" class="logo" />
      <span class="username-container" @click="fetchUserInfo">
        {{ username || 'Профиль' }}
      </span>
    </header>

    <h1>Опросники пользователя</h1>

    <button @click="goToTaskSettings" class="settings-button">
      Создать новый опросник
    </button>

    <div v-if="tasks.length" class="tasks-list">
      <ul>
        <li v-for="task in tasks" :key="task.id">
          <h3>{{ task.name }}</h3>
          <p>{{ task.description }}</p>
          <button @click="fetchTaskDetails(task.id)" class="action-button">Посмотреть настройки задачи</button>
          <!-- Кнопка для перехода к опросу -->
          <button @click="goToQuestionnaire(task.id)" class="action-button">Опрос</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Задачи не найдены.</p>
    </div>

    <div v-if="showUserModal" class="modal">
      <div class="modal-content">
        <span @click="showUserModal = false" class="close">&times;</span>
        <h2>Профиль пользователя</h2>
        <p><strong>Имя пользователя:</strong> {{ userInfo.username }}</p>
        <p><strong>Имя:</strong> {{ userInfo.first_name }}</p>
        <p><strong>Фамилия:</strong> {{ userInfo.last_name }}</p>
        <p><strong>Телефон:</strong> {{ userInfo.tel }}</p>
        <p><strong>Email:</strong> {{ userInfo.email }}</p>
        <button @click="logoutUser" class="logout-button">Выход</button>
      </div>
    </div>

    <div v-if="showTaskModal" class="modal">
      <div class="modal-content">
        <span @click="showTaskModal = false" class="close">&times;</span>
        <h2>Настройки задачи</h2>
        <p><strong>Название:</strong> {{ taskDetails.name }}</p>
        <p><strong>Описание:</strong> {{ taskDetails.description }}</p>

        <h3>Шкала:</h3>
        <table class="scale-table">
            <thead>
              <tr>
                <th class="fixed-width">Лингвистическая шкала</th>
                <th>Вес</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="scale in taskDetails.scale" :key="scale.id">
                <td class="fixed-width">{{ scale.grade }}</td>
                <td>{{ scale.weight }}</td>
              </tr>
            </tbody>
        </table>

        <h3>Индикаторы:</h3>
        <ul>
          <li v-for="indicator in taskDetails.indicators" :key="indicator.indicator">
            {{ indicator.indicator }} — {{ indicator.question }}
          </li>
        </ul>
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
      showTaskModal: false,
      userInfo: {},
      taskDetails: {}
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

    async logoutUser() {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        console.warn('Токен отсутствует.');
        return;
      }

      const response = await fetch('http://127.0.0.1:8000/auth/token/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        }
      });

      if (response.ok) {
        localStorage.removeItem('auth_token');
        this.username = '';
        this.showUserModal = false;
        window.location.href = 'http://localhost:8080/';
      } else {
        console.error('Ошибка при выходе из системы:', response.statusText);
      }
    } catch (error) {
      console.error('Ошибка при отправке запроса на выход:', error);
    }
    },
    async goToQuestionnaire(taskId) {
        this.$router.push({ name: 'Questionnaire', params: { id: taskId } });
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
    async fetchTaskDetails(taskId) {
      try {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`http://127.0.0.1:8000/api/v1/questionnaire/${taskId}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          }
        });

        if (response.ok) {
          this.taskDetails = await response.json();
          this.showTaskModal = true;
        } else {
          console.error('Ошибка при получении настроек задачи:', response.statusText);
        }
      } catch (error) {
        console.error('Ошибка при отправке запроса:', error);
      }
    }
  }
};
</script>
  
  <style scoped>

.action-button {
  margin-top: 10px;
  margin-right: 10px; 
  padding: 8px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.action-button:last-child {
  margin-right: 0; 
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
  .header-with-logo {
    display: flex;
    align-items: center;
    padding: 10px;
  }

  .logo {
    position: absolute;
    top: 0;
    left: 0;
    width: 50px;
    height: 50px;
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

  .logout-button {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #d32f2f;
}
  
  .settings-button:hover {
    background-color: #45a049;
  }
  
  .tasks-list ul {
    padding-left: 0;
    list-style-type: none; 
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
    width: 500px;
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

  .scale-table {
  width: 100%;              
  border-collapse: collapse; 
  margin-top: 10px;
}

.scale-table th,
.scale-table td {
  padding: 10px;               
  border: 1px solid #ddd;      
  text-align: center;          
}

.scale-table th {
  background-color: #f5f5f5;   
  font-weight: bold;           
}

.scale-table tr:nth-child(even) {
  background-color: #f9f9f9;   
}

.scale-table .fixed-width {
  width: 200px; /* Установите нужную ширину */
  text-align: left; /* Выравнивание текста по левому краю для первой колонки */
}

  </style>
  