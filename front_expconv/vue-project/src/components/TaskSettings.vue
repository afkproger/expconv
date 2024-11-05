<template>
  <div>
    <header>
      <span class="username-container" @click="fetchUserInfo">
        {{ userInfo.username || 'Профиль' }}
      </span>
    </header>
    
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

    <div class="task-settings">
      <h2>Создание нового опросника</h2>
      <form @submit.prevent="submitTask">
        <!-- Основная информация о задаче -->
        <label for="taskName">Название опросника:</label>
        <input type="text" v-model="task.name" id="taskName" required />

        <label for="taskDescription">Описание опросника:</label>
        <textarea v-model="task.description" id="taskDescription" required></textarea>

        <!-- Секция для добавления шкалы оценок -->
        <h3>Шкала оценок</h3>
        <div v-for="(scaleItem, index) in task.scale" :key="index" class="scale-item">
          <input type="text" v-model="scaleItem.grade" placeholder="Значение лингвистической шкалы" required />
          <input type="number" v-model="scaleItem.weight" placeholder="Вес" step="0.1" required />
          <button type="button" class="remove-button" @click="removeScaleItem(index)">Удалить</button>
        </div>
        <button type="button" class="add-button" @click="addScaleItem">Добавить значение шкалы</button>

        <!-- Секция для добавления показателей и вопросов -->
        <h3>Показатели и вопросы</h3>
        <div v-for="(valueItem, index) in task.values" :key="index" class="value-item">
          <div class="input-container">
            <input type="text" v-model="valueItem.indicators" placeholder="Наименование индикатора" required />
            <textarea
              v-model="valueItem.question"
              placeholder="Вопрос для определения эффективности"
              required
              class="question-textarea"
            ></textarea>
          </div>
          <button type="button" class="remove-button" @click="removeValueItem(index)">Удалить</button>
        </div>
        <button type="button" class="add-button" @click="addValueItem">Добавить показатель</button>

        <!-- Кнопки для сохранения и перехода на список задач -->
        <div class="button-container">
          <button type="button" class="tasks-list-button" @click="goToTasks">Список задач</button>
          <button type="submit" class="submit-button">Сохранить задачу</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      task: {
        name: '',
        description: '',
        scale: [],
        values: []
      },
      userInfo: {},
      showUserModal: false,
    };
  },
  methods: {
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
    addScaleItem() {
      this.task.scale.push({ grade: '', weight: null });
    },
    removeScaleItem(index) {
      this.task.scale.splice(index, 1);
    },
    addValueItem() {
      this.task.values.push({ indicators: '', question: '' });
    },
    removeValueItem(index) {
      this.task.values.splice(index, 1);
    },
    submitTask() {
      this.$emit('save-task', this.task);
    },
    goToTasks() {
      this.$router.push('/tasks'); 
    },
  }
};
</script>

  <style scoped>

.value-item {
  display: flex;
  align-items: flex-start; /* Выравнивание по верхнему краю */
  margin-bottom: 10px;
}

.input-container {
  flex: 1; /* Занимает оставшееся пространство */
  display: flex;
  flex-direction: column; /* Вводим элементы в столбик */
}

input[type="text"],
textarea {
  width: 100%; /* Задает ширину 100% */
  margin-bottom: 5px; /* Добавляет отступ между полями */
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

.question-textarea {
  resize: vertical; /* Разрешает изменение размера по вертикали */
  height: 80px; /* Начальная высота текстового поля */
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
  z-index: 1000; /* Обеспечьте, чтобы модальное окно было поверх других элементов */
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
  
.task-settings {
    padding: 30px;
    background-color: #f9f9f9;
    border-radius: 8px;
    max-width: 800px;
    margin: auto;
  }
  
h2 {
    text-align: center;
  }
  
label {
    display: block;
    margin-top: 10px;
    font-weight: bold;
  }
  
  input[type="text"],
  input[type="number"],
  textarea {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    box-sizing: border-box;
  }
  
  .scale-item,
  .value-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .scale-item input,
  .value-item input {
    flex: 1;
    margin-right: 10px;
  }
  
  button {
    cursor: pointer;
  }
  
  .add-button,
  .submit-button,
  .tasks-list-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 15px;
    margin-top: 10px;
    transition: background-color 0.3s;
  }
  
  .add-button:hover,
  .submit-button:hover,
  .tasks-list-button:hover {
    background-color: #45a049;
  }
  
  .remove-button {
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    transition: background-color 0.3s;
  }
  
  .remove-button:hover {
    background-color: #e53935;
  }
  
  .button-container {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  pre {
    background-color: #f1f1f1;
    padding: 10px;
    border-radius: 5px;
    margin-top: 20px;
  }
  </style>
  