<template>
    <div>
        <header>
            <img src="@/assets/fic_ran.png" alt="Логотип" class="logo" />
        </header>
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
      <button @click="sendAnswers()" type="button">Отправить ответы</button>
    </div>

    </div>
</template>

<script>
import config from '@/config';
export default{
    data(){
        return {
            questionnaireData: {
                name: '',
                description: '',
                scale: [],
                indicators: [],
            }, 
            taskId: "",
            expertToken: "",
            responses:[]
        }
    },
    async created(){
        this.taskId = this.$route.query.task;
        this.expertToken = this.$route.query.token;
        await this.fetchQuestionnaireData();
    },
    methods: {
        async fetchQuestionnaireData(){
        try {
            if (!this.taskId) throw new Error('Задача не найдена');
            const response = await fetch(`${config.apiBaseUrl}answers/?token=${this.expertToken}&task=${this.taskId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
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
        async sendAnswers(){
            // тут обработать отправку на сервер ) 
        }
    }
}
</script>

<style scoped>
.logo {
  position: absolute;
  top: 0;
  left: 0;
  width: 50px;
  height: 50px;
}

.questionnaire-container {
  flex: 1;
  padding: 20px;
}
.questions-list {
  list-style-type: none;
  padding: 0;
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

.buttons-container {
    display: flex;
    gap: 30px;
    margin-top: 20px;
    width: 300px;
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
</style>