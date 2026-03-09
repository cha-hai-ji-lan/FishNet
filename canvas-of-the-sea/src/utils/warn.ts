import { ref } from "vue";
import { interfaceStyle } from "../utils/MainIndex.ts";

export const attentionContent = ref<string>("")  // 注意内容

export const showPromptBox = ref<boolean>(false)  // 是否显示提示框
export const promptLevel = ref<string>("__NULL_LEVEL__")  // 是否显示提示框


export const set_content = (content: string, level: number = 2) => {
    switch (level) {  // 不清空警告等级状态位 默认是 一般警告
        case 1:
            promptLevel.value = "1"
            break;
        case 2:
            promptLevel.value = "2"
            break;
        case 3:
            promptLevel.value = "3"
            break;
        default:
            promptLevel.value = "2"
            break;
    }
    attentionContent.value = content;
    showPromptBox.value = true;
    console.log(attentionContent.value.length * interfaceStyle.value["atomicTime"])
    setTimeout(() => {
        showPromptBox.value = false;
        attentionContent.value = ""
    }, attentionContent.value.length * interfaceStyle.value["atomicTime"]) // interfaceStyle.value["atomicTime"] :原子时间,显示单个警告文字的最短时间
}