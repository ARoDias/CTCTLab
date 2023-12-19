<!-- components/CourseProgram.vue -->
<template>
    
    <div>
        <h2>Programa da Unidade Curricular</h2>
        <div class="column">
          
                <NewsCard 
                    v-for="week in weeks" 
                    :key="week.id"
                    :title="week.title"
                    :content="week.content"
                />
        
        </div>
    </div>
</template>

<script>
import NewsCard from './NewsCard.vue';

export default {
    components: {
        NewsCard,
    },
    data() {
        return {
            weeks: [
                {
                    title: "1 - Planeamento Curricular para a Empregabilidade",
                    content: "Durante a primeira semana da disciplina, são trabalhados vários aspectos do planeamento de carreira para a empregabilidade: <ul><li>O Curriculum Vitae, sua importância e apresentação.</li><li>Carta de Motivação.</li><li>A Entrevista e a Imagem.</li><li>As Redes Sociais e o Emprego.</li><li>Planeamento Curricular - aspetos a considerar para melhorar o CV.</li><li>O Teste Psicotécnico no processo de seleção e recrutamento.</li></ul>",
                },
                {
                    title: "2 - Gestão do Tempo, Trabalho em Equipa e Liderança",
                    content: "<p>Nesta semana, aborda-se os seguintes temas:</p><h4>Gestão do Tempo:</h4><ul><li>A importância do planeamento diário.</li><li>Objetivos SMART.</li><li>Importante vs. Urgente: Modelo de Stephen-Covey.</li><li>Desperdiçadores de Tempo.</li><li>Eficiência vs. Eficácia.</li><li>Adiamentos sistemáticos.</li><li>Adiamentos vs. Perfecionismo.</li><li>Gestão de e-mails e Redes Sociais.</li></ul><h4>Trabalho em Equipa:</h4><ul><li>Trabalho Colaborativo - Ferramentas de Edição de Textos.</li><li>Fatores de coesão e de perturbação da equipa.</li><li>Escuta Ativa.</li></ul><h4>Liderança:</h4> <ul><li>O Líder e a Gestão de Tarefas, Gestão Individual e a Gestão do Grupo.</li><li>Estilos e Valor da Liderança.</li><li>Caraterísticas de um Líder.</li><li>Linguagem positiva.</li></ul>"
                },
                {
                    title: "3 - Gestão de Informação e Comunicação",
                    content: " <p>Nesta semana, são abordados os seguintes temas:</p><ul><li>Conceitos básicos de gestão da informação.</li><li>Organização e classificação de informação.</li><li>Gestão de documentos físicos e eletrónicos.</li><li>Arquivo e recuperação de informação.</li><li>Comunicação interpessoal e organizacional.</li><li>Comunicação verbal e não verbal.</li><li>Barreiras à comunicação e formas de as superar.</li><li>Técnicas de apresentação e de falar em público.</li></ul>"
                },
                {
                    title: "4 - Utilização Avançada de Folhas de Cálculo",
                    content: "<p>Nesta semana, são abordados os seguintes temas:</p><ul><li>Uso avançado de fórmulas e funções.</li><li>Formatação condicional.</li><li>Criação de tabelas dinâmicas.</li><li>Importação e exportação de dados.</li><li>Trabalhar com várias folhas e livros.</li><li>Uso de gráficos e elementos gráficos.</li><li>Automatização de tarefas com macros.</li><li>Segurança e partilha de dados.</li></ul>"
                },
            ]
        }
    },
}
</script>

<style scoped>
h2 {
  color: #fff;
  background-color: #5CBECC; 
  text-align: center;
}

/* Card Component */
.card {
  padding: 20px;
  margin-top: 20px;
  background-color: #7CBE04;
  margin: 16px;
  color: white;
}

</style>