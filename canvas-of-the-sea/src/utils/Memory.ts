import { ref } from 'vue';

export const netTypes = [ // 拖网类型
  { value: "两片式", label: "两片式" },
  { value: "四片式", label: "四片式" },
  { value: "六片式", label: "六片式" },
]
export const themeTypes = [  // 主题可选样式
  { value: "dark", label: "暗色主题" },
  { value: "light", label: "亮色主题" },
]
/**
 * CADToolState 状态机
 * __WAIT__ : 等待连接操作
 * __READY__: 已连接就绪
 * __FAIL__ : 连接失败
*/
export const CADToolState = ref("__WAIT__")
export const CADToolStateInfo = ref({
  "__READY__":"CAD就绪",
  "__WAIT__":"CAD连接中",
  "__FAIL__":"CAD连接失败",

})


export const cacheRouterPath = ref<string>("__NULL__")  // 上一步操作的地址
export const isNewFile = ref<boolean>(false)  // 是否为一个新建的项目
