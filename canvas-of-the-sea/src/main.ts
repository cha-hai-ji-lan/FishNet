import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/router"

createApp(App).mount("#app");
// 创建一个应用
const app = createApp(App)
// 使用路由器
app.use(router)
// 挂载整个应用到app容器中
app.mount("#app");