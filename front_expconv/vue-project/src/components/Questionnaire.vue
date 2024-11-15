<template>
  <div>
    <header class="header-with-logo">
      <img src="@/assets/fic_ran.png" alt="Логотип" class="logo" />
      <span class="username-container" @click="fetchUserInfo">
        {{ username || 'Профиль' }}
      </span>
    </header>

    <div>
      <h1>Предпросмотр опросника</h1>
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
      <div v-if="questionnaireData.indicators && questionnaireData.indicators.length">
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
    </div>
  </div>
</template>

<script>
import config from '@/config.js';
export default {
  data() {
    return {
      questionnaireData: {
        name: '',
        description: '',
        scale: [],
        indicators: []
      },
      responses: [],
      username: '',
      showUserModal: false,
      userInfo: {}
    };
  },
  mounted() {
    this.username = localStorage.getItem('username') || '';
  },
  async created() {
    if (localStorage.getItem('auth_token')) {
      await this.fetchQuestionnaireData();
    }
  },
  methods: {
    async fetchQuestionnaireData() {
      const taskId = this.$route.params.id;
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) throw new Error('Токен не найден');
        
        const response = await fetch(`${config.apiBaseUrl}api/v1/questionnaire/${taskId}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          }
        });
        
        if (response.ok) {
          this.questionnaireData = await response.json();
        } else {
          const errorData = await response.json();
          console.error('Ошибка загрузки данных опросника:', errorData);
        }
      } catch (error) {
        console.error('Ошибка отправки запроса:', error.message);
      }
    },
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) throw new Error('Токен не найден');
        
        const response = await fetch(`${config.apiBaseUrl}api/v1/userinfo`, {
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
          const errorData = await response.json();
          console.error('Ошибка при получении информации о пользователе:', errorData);
        }
      } catch (error) {
        console.error('Ошибка при отправке запроса:', error.message);
      }
    },
    async logoutUser() {
      try {
        const token = localStorage.getItem('auth_token');
        if (!token) throw new Error('Токен не найден');

        const response = await fetch(`${config.apiBaseUrl}auth/token/logout/`, {
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
          this.$router.push('/');
        } else {
          const errorData = await response.json();
          console.error('Ошибка при выходе из системы:', errorData);
        }
      } catch (error) {
        console.error('Ошибка при отправке запроса на выход:', error.message);
      }
    }
  }
};
</script>

<style scoped>
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
}

.close:hover {
  color: darkred;
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

.questions-list {
  list-style-type: none;
  padding: 0;
}

.questionnaire-container {
  flex: 1;
  padding: 20px;
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
</style>
