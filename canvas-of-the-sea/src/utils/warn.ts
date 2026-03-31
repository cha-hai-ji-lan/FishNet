import { ref } from "vue";
import { interfaceStyle } from "../utils/MainIndex.ts";

export const attentionContent = ref<string>("")  // 注意内容

export const showPromptBox = ref<boolean>(false)  // 是否显示提示框
export const promptLevel = ref<string>("__NULL_LEVEL__")  // 是否显示提示框

let promptTimer: ReturnType<typeof setTimeout> | null = null;  // 提示框定时器

// const info_queue = ref<string[]>([])  // 提示信息队列

/**
 * 显示提示框
 * @param {string} content - 提示内容
 * @param {number} level - 警告等级 1:一般警告 2:重要警告 3:紧急警告
 * @returns {void}
*/
export const set_content = (content: string, level: number = 2): void => {
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
    console.log(content)
    shut_down_note()  // 关闭之前的提示框
    attentionContent.value = content;
    showPromptBox.value = true;
    // console.log(attentionContent.value.length * interfaceStyle.value["atomicTime"])
    promptTimer = setTimeout(() => {
        showPromptBox.value = false;
        attentionContent.value = ""
    }, attentionContent.value.length * interfaceStyle.value["atomicTime"]) // interfaceStyle.value["atomicTime"] :原子时间,显示单个警告文字的最短时间
}

/**
 * 关闭提示框
 * @returns {void}
 */
export const shut_down_note = (): void => {
    if (promptTimer) {
        clearTimeout(promptTimer);
        promptTimer = null;
    }
    showPromptBox.value = false;
    attentionContent.value = ""
}