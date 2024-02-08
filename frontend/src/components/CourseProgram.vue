<!-- components/CourseProgram.vue -->
<template>
  <div>
    <h2>
      {{ currentLanguage === "PT" ? "PROGRAMA" : "COURSE PROGRAM" }}
    </h2>
    <div class="column">
      <div v-for="week in weeks" :key="week.id" class="week-container">
        <NewsCard
          :title="currentLanguage === 'PT' ? week.titlePT : week.titleEN"
          :content="currentLanguage === 'PT' ? week.contentPT : week.contentEN"
        ></NewsCard>
      </div>
    </div>
  </div>
</template>

<script>
import NewsCard from "./NewsCard.vue";
export default {
  components: {
    NewsCard,
  },
  props: {
    currentLanguage: {
      type: String,
      default: "PT",
    },
  },
  data() {
    return {
      weeks: [
        {
          id: 1,
          titlePT: "1 - Planeamento Curricular para a Empregabilidade",
          contentPT:
            "Durante a primeira semana da disciplina, são trabalhados vários aspectos do planeamento de carreira para a empregabilidade:<ul><li>O Curriculum Vitae, sua importância e apresentação</li><li>Carta de Motivação</li><li>A Entrevista e a Imagem</li><li>As Redes Sociais e o Emprego</li><li>Planeamento Curricular - aspectos a considerar para melhorar o CV</li><li>O Teste Psicotécnico no processo de seleção e recrutamento</li></ul>",
          titleEN: "1 - Curriculum Planning for Employability",
          contentEN:
            "During the first week of the course, various aspects of career planning for employability are worked on:<ul><li>The Curriculum Vitae, its importance and presentation</li><li>Motivation Letter</li><li>The Interview and Image</li><li>Social Media and Employment</li><li>Curriculum Planning - aspects to consider to improve the CV</li><li>The Psychotechnical Test in the selection and recruitment process</li></ul>",
        },
        {
          id: 2,
          titlePT: "2 - Gestão do Tempo, Trabalho em Equipa e Liderança",
          contentPT:
            "Nesta semana, aborda-se os seguintes temas:<ul><li>Gestão do Tempo: A importância do planeamento diário</li><li>Objetivos SMART</li><li>Importante vs. Urgente: Modelo de Stephen-Covey</li><li>Desperdiçadores de Tempo</li><li>Eficiência vs. Eficácia</li><li>Adiamentos sistemáticos</li><li>Adiamentos vs. Perfecionismo</li><li>Gestão de e-mails e Redes Sociais</li></ul><ul><li>Trabalho em Equipa: Trabalho Colaborativo - Ferramentas de Edição de Textos</li><li>Fatores de coesão e de perturbação da equipa</li><li>Escuta Ativa</li></ul><ul><li>Liderança: O Líder e a Gestão de Tarefas, Gestão Individual e a Gestão do Grupo</li><li>Estilos e Valor da Liderança</li><li>Caraterísticas de um Líder</li><li>Linguagem positiva</li></ul>",
          titleEN: "2 - Time Management, Teamwork and Leadership",
          contentEN:
            "This week, the following topics are addressed:<ul><li>Time Management: The importance of daily planning</li><li>SMART Goals</li><li>Important vs. Urgent: Stephen-Covey Model</li><li>Time Wasters</li><li>Efficiency vs. Effectiveness</li><li>Systematic Procrastination</li><li>Procrastination vs. Perfectionism</li><li>Email and Social Media Management</li></ul><ul><li>Teamwork: Collaborative Work - Text Editing Tools</li><li>Team cohesion and disturbance factors</li><li>Active Listening</li></ul><ul><li>Leadership: The Leader and Task Management, Individual Management and Group Management</li><li>Styles and Value of Leadership</li><li>Characteristics of a Leader</li><li>Positive language</li></ul>",
        },
        {
          id: 3,
          titlePT: "3 - Gestão de Informação e Comunicação",
          contentPT:
            "Nesta semana, são abordados os seguintes temas:<ul><li>Conceitos básicos de gestão da informação</li><li>Organização e classificação de informação</li><li>Gestão de documentos físicos e eletrónicos</li><li>Arquivo e recuperação de informação</li><li>Comunicação interpessoal e organizacional</li><li>Comunicação verbal e não verbal</li><li>Barreiras à comunicação e formas de as superar</li><li>Técnicas de apresentação e de falar em público</li></ul>",
          titleEN: "3 - Information Management and Communication",
          contentEN:
            "This week, the following themes are covered:<ul><li>Basic concepts of information management</li><li>Organization and classification of information</li><li>Management of physical and electronic documents</li><li>Filing and retrieval of information</li><li>Interpersonal and organizational communication</li><li>Verbal and non-verbal communication</li><li>Barriers to communication and ways to overcome them</li><li>Presentation techniques and public speaking</li></ul>",
        },
        {
          id: 4,
          titlePT: "4 - Utilização Avançada de Folhas de Cálculo",
          contentPT:
            "Nesta semana, são abordados os seguintes temas:<ul><li>Uso avançado de fórmulas e funções</li><li>Formatação condicional</li><li>Criação de tabelas dinâmicas</li><li>Importação e exportação de dados</li><li>Trabalhar com várias folhas e livros</li><li>Uso de gráficos e elementos gráficos</li><li>Automatização de tarefas com macros</li><li>Segurança e partilha de dados</li></ul>",
          titleEN: "4 - Advanced Use of Spreadsheets",
          contentEN:
            "This week, the following topics are addressed:<ul><li>Advanced use of formulas and functions</li><li>Conditional formatting</li><li>Creation of pivot tables</li><li>Importing and exporting data</li><li>Working with multiple sheets and workbooks</li><li>Use of charts and graphic elements</li><li>Automation of tasks with macros</li><li>Data security and sharing</li></ul>",
        },
      ],
    };
  },
  methods: {
    getFormattedContent(week) {
      return this.currentLanguage === "PT" ? week.contentPT : week.contentEN;
    },
  },
};
</script>

<style scoped>
h2 {
  color: var(--white);
}
.column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: var(--primary-blue);
}

.week-container h3 {
  color: var(--dark-blue); /* Ajuste a cor conforme a necessidade */
  margin-bottom: 10px;
}

.week-container div {
  font-size: 16px;
  color: var(--dark-blue);
}
</style>
