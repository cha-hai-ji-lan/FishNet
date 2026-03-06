import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/page/Home.vue'
import DrawTwoPiece from '../components/page/DrawTwoPiece.vue'
const router = createRouter({
    history: createWebHistory(), // 路由器的工作模式
    routes: [
        {
            path: '/', // 添加根路径路由
            component: Home // 可以选择一个组件作为默认页面
        },
        {
            path: '/draw-two-piece', // 添加根路径路由
            component: DrawTwoPiece // 可以选择一个组件作为默认页面
        },
        // {
        //     path: '/deal-file',
        //     component: DealFile
        // },
        // {
        //     path: '/make-shutdown',
        //     component: MakeShutDown
        // },
        // {
        //     path: '/live-picture',
        //     component: LivePicture
        // },
        // {
        //     path: '/document',
        //     component: Document
        // },
        // // {
        // //     path: '/child',
        // //     component: Temp
        // // },
        // {
        //     path: '/record-screen',
        //     component: RecordScreen
        // }
    ]
})

// 暴露路由
export default router