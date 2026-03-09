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

export const cacheRouterPath = ref<string>("__NULL__")  // 上一步操作的地址
export const isNewFile = ref<boolean>(false)  // 是否为一个新建的项目
