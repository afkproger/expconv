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

    <div class="buttons-container">
      <button @click="goToTasks" type="button">К списку задач</button>
    </div>

    <div>
      <h2>Настройки для рассылки опроса экспертам</h2>
      <form @submit.prevent="createExpertData">
        <div v-for="(expert, index) in expertData" :key="index" class="expert-container">
          <div>
            <label for="expert_name_{{ index }}">Имя эксперта:</label>
            <input
              type="text"
              :id="'expert_name_' + index"
              v-model="expert.expert_name"
              placeholder="Введите имя пользователя"
              required
            />
          </div>
          <div>
            <label for="opinion_weight_{{ index }}">Вес мнения эксперта:</label>
            <input
              type="number"
              :id="'opinion_weight_' + index"
              v-model="expert.opinion_weight"
              step="0.01"
              required
            />
          </div>
          <button @click="removeExpert(index)" type="button" v-if="expertData.length > 1">Удалить</button>
        </div>
        <button @click="addExpert" type="button">Добавить</button>
        <button type="submit">Сохранить выбор экспертов для ответов</button>
      </form>
    </div>
    <table v-if="questionnaireData.experts_responses && questionnaireData.experts_responses.length > 0">
    <thead>
      <tr>
        <th>Имя эксперта</th>
        <th>Ссылка</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(expert, index) in questionnaireData.experts_responses" :key="index">
        <td>{{ expert.name }}</td>
        <td>
          <span>{{ `${expert_questionnaire_URL}answers/?token=${expert.expert_token}&task=${this.$route.params.id}` }}</span>
        </td>
      </tr>
    </tbody>
    </table>
    <div>
      <h3>response</h3>
      <pre>{{questionnaireData}}</pre>
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
        indicators: [],
        experts_responses: [],
      },
      expertData: [
        {
          expert_name: '',
          opinion_weight: 0.0
        }
      ],
      expert_questionnaire_URL : "http://10.1.8.169:8080/",
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
    goToTasks() {
      this.$router.push('/tasks');
    },
    addExpert() {
      this.expertData.push({
        expert_name: '',
        opinion_weight: 0.0
      });
    },
    removeExpert(index) {
      if (this.expertData.length > 1) {
        this.expertData.splice(index, 1);
      }
    },
    async createExpertData() {
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${config.apiBaseUrl}api/v1/questionnaire/choice_experts/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
          task_id: this.$route.params.id,
          experts: this.expertData
        })
      });

      if (response.ok) {
        console.log('Отправка данных');
      } else {
        const errorData = await response.json();
        console.error('Ошибка отправки данных:', errorData);
      }
    } catch (error) {
      console.error('Ошибка отправки запроса:', error.message);
    }
    },
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

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f5f5f5;
  color: #333;
  font-weight: bold;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
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
.buttons-container {
    display: flex;
    gap: 30px;
    margin-top: 20px;
    width: 300px;
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


form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

form div {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}

input[type="text"], input[type="number"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}
input[required] {
  border-color: #7b9ab8;
}

input[required]:focus {
  border-color: #7b9ab8;
  outline: none;
}

.expert-container {
  margin-bottom: 15px;
  padding: 15px;
  background-color: #f1f1f1;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

button {
  margin-top: 10px;
  padding: 8px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
}

button:hover {
  background-color: #45a049;
}

button[type="button"]:not(:last-child) {
  background-color: #003050;
}

button[type="button"]:not(:last-child):hover {
  background-color: #7b9ab8;
}
</style>
