import { listen, UnlistenFn } from '@tauri-apps/api/event'

let unlisten_start_connect: UnlistenFn | null = null

// 初始化事件监听
export async function listen_start_connect() {
    if (unlisten_start_connect) {
        return // 避免重复注册
    }
    
    unlisten_start_connect = await listen('cli-start-connect', (event) => {
        console.log('收到 Rust 消息:', event.payload)
        // 在这里调用你的 TypeScript 函数
        if (unlisten_start_connect) {  // 确保监听器存在 时响应了监听就卸载监听
            unlisten_start_connect()
            unlisten_start_connect = null
        }
    })
}

// 清理监听器
export function cleanup_event_listeners() {
    if (unlisten_start_connect) {
        unlisten_start_connect()
        unlisten_start_connect = null
    }
}
