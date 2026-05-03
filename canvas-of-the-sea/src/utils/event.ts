import { listen, UnlistenFn } from '@tauri-apps/api/event'
import { set_content } from '../utils/warn.ts'
import { CADToolState} from '../utils/Memory.ts'


let unlisten_cli_connect: UnlistenFn | null = null  // 开始启动服务端监听器
let unlisten_start_connect: UnlistenFn | null = null  // 开始链接监听器
let unlisten_create_cad_example: UnlistenFn | null = null  // 创建AutoCAD实例监听器
let unlisten_fail_create_cad_example: UnlistenFn | null = null  // 创建AutoCAD实例失败监听器
let unlisten_fail_ready: UnlistenFn | null = null  // 就绪失败
let unlisten_cad_ready: UnlistenFn | null = null  // 创建AutoCAD实例失败监听器
let unlisten_horizontal_scale_zero: UnlistenFn | null = null  // 监听水平缩放为0

// 初始化事件监听
/**
 * 监听cad cli tool 启动
*/
export const listen_cli_connect = async () => {
    if (unlisten_cli_connect) {
        return // 避免重复注册
    }
    unlisten_cli_connect = await listen('cli-connect', (event : any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        set_content(`${event.payload.data}`, 1)
        if (unlisten_cli_connect) {  // 确保监听器存在 时响应了监听就卸载监听
            unlisten_cli_connect()
            unlisten_cli_connect = null
        }
    })
}
/**
 * 监听开始链接AutoCAD事件
*/
export const listen_start_connect = async () => {
    if (unlisten_start_connect) {
        return // 避免重复注册
    }
    unlisten_start_connect = await listen('start-connect', (event: any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        set_content(`${event.payload.data}`, 1)
        if (unlisten_start_connect) {  // 确保监听器存在 时响应了监听就卸载监听
            unlisten_start_connect()
            unlisten_start_connect = null
        }
    })
}
/**
 * 监听创建AutoCAD实例事件
*/
export const listen_create_cad_example = async () => {
    if (unlisten_create_cad_example) {
        return // 避免重复注册
    }
    unlisten_create_cad_example = await listen('create-cad-example', (event: any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        set_content(`${event.payload.data}`, 2)
        if (unlisten_create_cad_example) {  // 确保监听器存在 时响应了监听就卸载监听
            unlisten_create_cad_example()
            unlisten_create_cad_example = null
        }
    })
}
/**
 * 监听CAD就绪失败
*/
export const listen_fail_ready = async () => {
    if (unlisten_fail_ready) {
        return // 避免重复注册

    }
    unlisten_fail_ready = await listen('fail-ready', (event: any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        CADToolState.value = "__FAIL__"
        set_content("AutoCAD连接无法就绪, 请重启服务端", 3)
        cleanup_cad_listen_group()  // 清理监听组，停止监听后续事件
    })
}
/**
 * 监听CAD创建失败
*/
export const listen_fail_create_cad_example = async () => {
    if (unlisten_fail_create_cad_example) {
        return // 避免重复注册
    }
    unlisten_fail_create_cad_example = await listen('fail-create-cad-example', (event: any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        CADToolState.value = "__FAIL__"
        set_content(`${event.payload.data}`, 3)
        cleanup_cad_listen_group()  // 清理监听组，停止监听后续事件
    })
}
/**
 * 监听CAD就绪 
 * 当 CAD一就绪就可以开启 运行时监听组了
*/
export const listen_cad_ready = async () => {
    if (unlisten_cad_ready) {
        return // 避免重复注册

    }
    unlisten_cad_ready = await listen('cad-ready', (event : any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        CADToolState.value = "__READY__"
        set_content(`${event.payload.data}`, 1)
        cleanup_cad_listen_group()  // 清理初始化监听组，停止监听后续事件
        exe_cad_listen_group()  // 执行运行时监听组，开启运行时事件监听
    })
}
/**
 * 监听横向比例尺是否为 0 
*/
export const listen_horizontal_scale_zero = async () => {
    if (unlisten_horizontal_scale_zero) {
        return // 避免重复注册
    }
    unlisten_horizontal_scale_zero = await listen('horizontal-scale-zero', (event : any) => {
        console.log('收到 Rust 消息:', event.payload.data)
        set_content(`${event.payload.data}`, 3)
    })
}
/**
 * 初始化监听组
*/

export const init_cad_listen_group = () => {
    listen_cli_connect()  // 监控cad cli tool 启动
    listen_start_connect()  // 监控cad启动
    listen_create_cad_example()  // 监控创建cad实例
    listen_fail_create_cad_example() // 监控创建cad实例失败
    listen_fail_ready()  // 监控cad就绪失败
    listen_cad_ready() // 监控cad准备就绪
}
/**
 * 运行时监听组
*/

export const exe_cad_listen_group = () =>{
    listen_horizontal_scale_zero()
}

/**
 * 清理初始化监控组监控器
* unlisten_start_connect: 用于停止监听 'start-connect' 事件的函数。
* unlisten_create_cad_example: 用于停止监听 'create-cad-example' 事件的函数。
* unlisten_fail_create_cad_example: 用于停止监听 'fail-create-cad-example' 事件的函数。
* unlisten_cad_ready: 用于停止监听 'cad_ready' 事件的函数。
*/
export const cleanup_cad_listen_group = () => {
    if (unlisten_cli_connect) {
        unlisten_cli_connect()
        unlisten_cli_connect = null
    }
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
    if (unlisten_fail_ready) {
        unlisten_fail_ready()
        unlisten_fail_ready = null
    }
    if (unlisten_cad_ready) {
        unlisten_cad_ready()
        unlisten_cad_ready = null
    }
}

/**
 * 清理运行时监控组监控器
 * unlisten_horizontal_scale_zero: 用于停止监听 'horizontal-scale-zero' 事件的函数。
 */
export const cleanup_exe_cad_listen_group = () => {
    if (unlisten_horizontal_scale_zero) {
        unlisten_horizontal_scale_zero()
        unlisten_horizontal_scale_zero = null
    }
}
/**
 * 清理监听器
 * @returns {void}

 */
export const cleanup_event_listeners = (): void => {
    cleanup_cad_listen_group()  // 清理初始化监控组监控器
    cleanup_exe_cad_listen_group()  //  清理运行时监控组监控器
}


/**
 * 清理运行时监控组监控器
* unlisten_start_connect: 用于停止监听 'start-connect' 事件的函数。
* unlisten_create_cad_example: 用于停止监听 'create-cad-example' 事件的函数。
* unlisten_fail_create_cad_example: 用于停止监听 'fail-create-cad-example' 事件的函数。
* unlisten_cad_ready: 用于停止监听 'cad_ready' 事件的函数。
*/

/**
 * 前端可监听事件
 * 
 * 键盘上下键监听 -- 用于切换注视input
*/

export const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'ArrowDown') {
        event.preventDefault()
        const inputs = Array.from(document.querySelectorAll('.two-piece-body input')) as HTMLInputElement[]
        const currentIndex = inputs.findIndex(input => input === document.activeElement)

        if (currentIndex !== -1) {
            const nextIndex = (currentIndex + 1) % inputs.length
            inputs[nextIndex].focus()
        } else if (inputs.length > 0) {
            inputs[0].focus()
        }
    } else if (event.key === 'ArrowUp') {
        event.preventDefault()
        const inputs = Array.from(document.querySelectorAll('.two-piece-body input')) as HTMLInputElement[]
        const currentIndex = inputs.findIndex(input => input === document.activeElement)
        if (currentIndex !== -1) {
            const prevIndex = (currentIndex - 1 + inputs.length) % inputs.length
            inputs[prevIndex].focus()
        } else if (inputs.length > 0) {
            inputs[inputs.length - 1].focus()
        }
    }
}