const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: true,
    webSocketServer: false,
    host: "0.0.0.0",
    allowedHosts: ["c99b-2a01-14-8020-7e20-4149-3c30-a6b3-baa8.ngrok-free.app"],
  },
});
