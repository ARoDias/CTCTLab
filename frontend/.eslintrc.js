module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ["plugin:vue/vue3-essential", "eslint:recommended"],
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false, // Adiciona esta linha para não precisar de um arquivo de configuração do Babel
  },
  rules: {
    // as tuas regras personalizadas aqui
  },
};
