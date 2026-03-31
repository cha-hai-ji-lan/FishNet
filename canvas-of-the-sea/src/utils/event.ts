import { listen, UnlistenFn } from '@tauri-apps/api/event'
import { set_content } from '../utils/warn.ts'

let unlisten_start_connect: UnlistenFn | null = null  // 开始链接监听器
let unlisten_create_cad_example: UnlistenFn | null = null  // 创建AutoCAD实例监听器
let unlisten_fail_create_cad_example: UnlistenFn | null = null  // 创建AutoCAD实例失败监听器
let unlisten_cad_ready: UnlistenFn | null = null  // 创建AutoCAD实例失败监听器

// 初始化事件监听
export const listen_start_connect = async () => {
    if (unlisten_start_connect) {
        return // 避免重复注册
    }
    unlisten_start_connect = await listen('start-connect', (event) => {
        console.log('收到 Rust 消息:', event.payload)
        // 在这里调用你的 TypeScript 函数
        set_content("开始链接AutoCAD活动实例", 1)
        if (unlisten_start_connect) {  // 确保监听器存在 时响应了监听就卸载监听
            unlisten_start_connect()
            unlisten_start_connect = null
        }
    })
}
export const listen_create_cad_example = async () => {
    if (unlisten_create_cad_example) {
        return // 避免重复注册

    }
    unlisten_create_cad_example = await listen('create-cad-example', (event) => {
        console.log('收到 Rust 消息:', event.payload)
        // 在这里调用你的 TypeScript 函数
        set_content("链接AutoCAD失败开始创建AutoCAD实例", 2)
        if (unlisten_create_cad_example) {  // 确保监听器存在 时响应了监听就卸载监听
            unlisten_create_cad_example()
            unlisten_create_cad_example = null
        }
    })
}
export const listen_fail_create_cad_example = async () => {
    if (unlisten_fail_create_cad_example) {
        return // 避免重复注册

    }
    unlisten_fail_create_cad_example = await listen('fail-create-cad-example', (event) => {
        console.log('收到 Rust 消息:', event.payload)
        // 在这里调用你的 TypeScript 函数
        set_content("AutoCAD实例创建失败...请重启软件", 3)
        cleanup_cad_listen_group()  // 清理监听组，停止监听后续事件
    })
}
export const listen_cad_ready = async () => {
    if (unlisten_cad_ready) {
        return // 避免重复注册

    }
    unlisten_cad_ready = await listen('cad-ready', (event) => {
        console.log('收到 Rust 消息:', event.payload)
        // 在这里调用你的 TypeScript 函数
        set_content("AutoCAD准备就绪", 1)
        cleanup_cad_listen_group()  // 清理监听组，停止监听后续事件
    })
}
/**
 * 初始化监听组
*/

export const init_cad_listen_group = () => {
    listen_start_connect()  // 监控cad启动
    listen_create_cad_example()  // 监控创建cad实例
    listen_fail_create_cad_example() // 监控创建cad实例失败
    listen_cad_ready() // 监控cad准备就绪
}

/**
 * 清理初始化监控组监控器
* unlisten_start_connect: 用于停止监听 'start-connect' 事件的函数。
* unlisten_create_cad_example: 用于停止监听 'create-cad-example' 事件的函数。
* unlisten_fail_create_cad_example: 用于停止监听 'fail-create-cad-example' 事件的函数。
* unlisten_cad_ready: 用于停止监听 'cad_ready' 事件的函数。
*/
export const cleanup_cad_listen_group = () => {
    if (unlisten_start_connect) {
        unlisten_start_connect()
        unlisten_start_connect = null
    }
    if (unlisten_create_cad_example) {
        unlisten_create_cad_example()
        unlisten_create_cad_example = null
    }
    if (unlisten_fail_create_cad_example) {
        unlisten_fail_create_cad_example()
        unlisten_fail_create_cad_example = null
    }
    if (unlisten_cad_ready) {
        unlisten_cad_ready()
        unlisten_cad_ready = null
    }
}
/**
 * 清理监听器
 * @returns {void}

 */
export const cleanup_event_listeners = (): void => {
    cleanup_cad_listen_group()
}
