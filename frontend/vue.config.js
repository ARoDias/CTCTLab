const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: true,
    webSocketServer: false,
    host: "0.0.0.0",
    allowedHosts: [
      "1fc2-2a01-14-8020-7e20-e9d2-9197-151a-7ef.ngrok-free.app",
      "127.0.0.1",
      "localhost",
    ],
  },
});
