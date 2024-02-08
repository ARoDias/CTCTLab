<!-- components/CourseProgram.vue -->
<!-- components/CourseProgram.vue -->
<template>
  <!-- Main container for the course program -->
  <div>
    <!-- Title of the course program section -->
    <h2>
      {{
        currentLanguage === "PT"
          ? "Programa da Unidade Curricular"
          : "Course Program"
      }}
    </h2>
    <!-- Container for the weekly news cards -->
    <div class="column">
      <!-- Loop through the weeks array to display each week's content -->
      <NewsCard
        v-for="week in weeks"
        :key="week.id"
        :title="currentLanguage === 'PT' ? week.titlePT : week.titleEN"
        :content="currentLanguage === 'PT' ? week.contentPT : week.contentEN"
      />
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
      default: "PT", // Default language if not provided by the parent
    },
  },
  data() {
    return {
      weeks: [
        {
          id: 1,
          titlePT: "1 - Planeamento Curricular para a Empregabilidade",
          contentPT:
            "Durante a primeira semana da disciplina, são trabalhados vários aspectos do planeamento de carreira para a empregabilidade: O Curriculum Vitae, sua importância e apresentação; Carta de Motivação; A Entrevista e a Imagem; As Redes Sociais e o Emprego; Planeamento Curricular - aspetos a considerar para melhorar o CV; O Teste Psicotécnico no processo de seleção e recrutamento.",
          titleEN: "1 - Curriculum Planning for Employability",
          contentEN:
            "During the first week of the course, various aspects of career planning for employability are worked on: The Curriculum Vitae, its importance and presentation; Motivation Letter; The Interview and Image; Social Media and Employment; Curriculum Planning - aspects to consider to improve the CV; The Psychotechnical Test in the selection and recruitment process.",
        },
        {
          id: 2,
          titlePT: "2 - Gestão do Tempo, Trabalho em Equipa e Liderança",
          contentPT:
            "Nesta semana, aborda-se os seguintes temas: Gestão do Tempo: A importância do planeamento diário; Objetivos SMART; Importante vs. Urgente: Modelo de Stephen-Covey; Desperdiçadores de Tempo; Eficiência vs. Eficácia; Adiamentos sistemáticos; Adiamentos vs. Perfecionismo; Gestão de e-mails e Redes Sociais. Trabalho em Equipa: Trabalho Colaborativo - Ferramentas de Edição de Textos; Fatores de coesão e de perturbação da equipa; Escuta Ativa. Liderança: O Líder e a Gestão de Tarefas, Gestão Individual e a Gestão do Grupo; Estilos e Valor da Liderança; Caraterísticas de um Líder; Linguagem positiva.",
          titleEN: "2 - Time Management, Teamwork and Leadership",
          contentEN:
            "This week, the following topics are addressed: Time Management: The importance of daily planning; SMART Goals; Important vs. Urgent: Stephen-Covey Model; Time Wasters; Efficiency vs. Effectiveness; Systematic Procrastination; Procrastination vs. Perfectionism; Email and Social Media Management. Teamwork: Collaborative Work - Text Editing Tools; Team cohesion and disturbance factors; Active Listening. Leadership: The Leader and Task Management, Individual Management and Group Management; Styles and Value of Leadership; Characteristics of a Leader; Positive language.",
        },
        {
          id: 3,
          titlePT: "3 - Gestão de Informação e Comunicação",
          contentPT:
            "Nesta semana, são abordados os seguintes temas: Conceitos básicos de gestão da informação; Organização e classificação de informação; Gestão de documentos físicos e eletrónicos; Arquivo e recuperação de informação; Comunicação interpessoal e organizacional; Comunicação verbal e não verbal; Barreiras à comunicação e formas de as superar; Técnicas de apresentação e de falar em público.",
          titleEN: "3 - Information Management and Communication",
          contentEN:
            "This week, the following themes are covered: Basic concepts of information management; Organization and classification of information; Management of physical and electronic documents; Filing and retrieval of information; Interpersonal and organizational communication; Verbal and non-verbal communication; Barriers to communication and ways to overcome them; Presentation techniques and public speaking.",
        },
        {
          id: 4,
          titlePT: "4 - Utilização Avançada de Folhas de Cálculo",
          contentPT:
            "Nesta semana, são abordados os seguintes temas: Uso avançado de fórmulas e funções; Formatação condicional; Criação de tabelas dinâmicas; Importação e exportação de dados; Trabalhar com várias folhas e livros; Uso de gráficos e elementos gráficos; Automatização de tarefas com macros; Segurança e partilha de dados.",
          titleEN: "4 - Advanced Use of Spreadsheets",
          contentEN:
            "This week, the following topics are addressed: Advanced use of formulas and functions; Conditional formatting; Creation of pivot tables; Importing and exporting data; Working with multiple sheets and workbooks; Use of charts and graphic elements; Automation of tasks with macros; Data security and sharing.",
        },
      ],
    };
  },
};
</script>

<style scoped>
h2 {
  color: var(--white);
}
</style>
