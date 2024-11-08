<template>
    <div>
      <header class = "header-with-logo">
        <img src="@/assets/fic_ran.png" alt="Логотип" class="logo" />
        <span class="username-container" @click="fetchUserInfo">
          {{ username || 'Профиль' }}
        </span>
      </header>
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
      <div class="questionnaire-container">
        <h1>{{ questionnaireData.name }}</h1>
        <h2>{{ questionnaireData.description }}</h2>
  
        <div v-if="questionnaireData.indicators.length">
          <ul class="questions-list">
            <li v-for="(indicator, index) in questionnaireData.indicators" :key="index" class="question-item">
              <h4>{{ indicator.question }}</h4>
  
              <div class="answers-container">
                <label v-for="(option, i) in questionnaireData.scale" :key="i" class="answer-option">
                  <input
                    type="radio"
                    :name="'question-' + index"
                    :value="option.grade"
                    v-model="responses[index]"
                  />
                  {{ option.grade }}
                </label>
              </div>
            </li>
          </ul>
        </div>
        <div class="buttons-container">
          <button @click="goToTasks" class="button-style">Список задач</button>
          <button @click="submitAnswers" class="button-style">Отправить ответы</button>
        </div>
  
        <!-- Отображение результата после отправки ответов -->
        <div v-if="result">
          <h3>Результат:</h3>
          <p>{{ result }}</p>
        </div>
      </div>
  </template>
  
  
  <script>
  export default {
    data() {
      return {
        questionnaireData: {
          name: '',
          description: '',
          scale: [],
          indicators: []
        },
        showUserModal: false,
        responses: [],
        answersJson: null,
        result: null,
        userInfo: {},
        username: '' // Добавьте переменную username для отображения имени пользователя
      };
    },
    async created() {
      await this.fetchQuestionnaireData();
    },
    methods: {
      async fetchQuestionnaireData() {
        const taskId = this.$route.params.id;
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
            this.questionnaireData = await response.json();
            this.responses = new Array(this.questionnaireData.indicators.length).fill('');
          } else {
            console.error('Ошибка загрузки данных опросника:', response.statusText);
          }
        } catch (error) {
          console.error('Ошибка отправки запроса:', error);
        }
      },
      async submitAnswers() {
        this.generateAnswersJson();
        console.log('Ответы пользователя:', this.answersJson);
  
        try {
          const response = await fetch('http://127.0.0.1:8000/api/v1/convolution/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Token ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify(this.answersJson)
          });
  
          if (response.ok) {
            const data = await response.json();
            this.result = data.conv; // Сохраняем результат
          } else {
            console.error('Ошибка при отправке ответов:', response.statusText);
            this.result = 'Ошибка при отправке ответов';
          }
        } catch (error) {
          console.error('Ошибка отправки запроса:', error);
          this.result = 'Ошибка при отправке ответов';
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
      generateAnswersJson() {
        this.answersJson = {
          answers: this.questionnaireData.indicators.map((indicator, index) => {
            const selectedAnswer = this.responses[index];
            const selectedOption = this.questionnaireData.scale.find(option => option.grade === selectedAnswer);
            return {
              indicators: indicator.indicator,
              ans: selectedAnswer,
              weight: selectedOption ? selectedOption.weight : null,
              index: index
            };
          })
        };
      },
      goToTasks() {
        this.$router.push('/tasks');
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .sidebar {
    width: 250px;
    padding: 20px;
    background-color: #f7f7f7;
    border-right: 1px solid #ddd;
  }
  
  .questionnaire-container {
    flex: 1;
    padding: 20px;
  }
  
  .questions-list {
    list-style-type: none;
    padding: 0;
  }
  
  .question-item {
    margin-bottom: 20px;
  }
  
  .profile-container {
    text-align: right;
  }
  
  .answers-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .answer-option {
    display: flex;
    align-items: center;
  }
  
  .header-with-logo {
    display: flex;
    align-items: center;
    padding: 10px;
    justify-content: flex-end;  
  }
  .logo {
    position: absolute;
    top: 0;
    left: 0;
    width: 50px;
    height: 50px;
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
  .buttons-container {
    display: flex;
    gap: 30px;
    margin-top: 20px;
  }
  
  .button-style {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .button-style:hover {
    background-color: #45a049;
  }
  
  .logout-button {
    background-color: red;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .logout-button:hover {
    background-color: darkred;
  }
  
  </style>
  