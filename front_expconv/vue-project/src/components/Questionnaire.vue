<template>
    <div class="questionnaire-container">
      <h1>{{ questionnaireData.name }}</h1>
      <h2>{{ questionnaireData.description }}</h2>
  
      <div v-if="questionnaireData.indicators.length">
        <ul class="questions-list">
          <li v-for="(indicator, index) in questionnaireData.indicators" :key="index" class="question-item">
            <h4>{{ indicator.question }}</h4>
  
            <div class="answers-container">
              <label
                v-for="(option, i) in questionnaireData.scale"
                :key="i"
                class="answer-option"
              >
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
  
      <button @click="submitAnswers" class="submit-button">Отправить ответы</button>
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
        responses: []
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
      submitAnswers() {
        console.log('Ответы пользователя:', this.responses);
        // Здесь можно добавить логику для отправки ответов пользователя на сервер
      }
    }
  };
  </script>
  
  <style scoped>
  .questionnaire-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .questions-list {
    list-style-type: none;
    padding: 0;
  }
  
  .question-item {
    margin-bottom: 20px;
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
  
  .submit-button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .submit-button:hover {
    background-color: #45a049;
  }
  </style>
  