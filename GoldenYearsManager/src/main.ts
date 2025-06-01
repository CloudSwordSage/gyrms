import './assets/main.css'
import 'element-plus/dist/index.css'

import { createApp } from 'vue'
import { createPinia, type PiniaPluginContext } from 'pinia'
import ElementPlus from 'element-plus'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// 初始化pinia并添加插件
const pinia = createPinia()
pinia.use(({ store }: PiniaPluginContext) => {
  store.$auth = {
    hasRole: (role: string) => store.hasRole(role)
  }
})
app.use(pinia)

// 初始化router
app.use(router)

// 添加ElementPlus
app.use(ElementPlus)

// 添加全局错误处理
app.config.errorHandler = (err) => {
  console.error('全局错误:', err)
}

app.mount('#app')
