import { ref } from "vue";
import {interfaceStyle } from "../utils/MainIndex.ts";

export const attentionContent = ref<string>("")  // 注意内容

export const showPromptBox = ref<boolean>(false)  // 是否显示提示框


export const set_content = (content: string) => {
    attentionContent.value = content;
    showPromptBox.value = true;
    console.log(attentionContent.value.length * interfaceStyle.value["atomicTime"])
    setTimeout(() =>{
        showPromptBox.value = false;
        attentionContent.value  = ""
    }, attentionContent.value.length * interfaceStyle.value["atomicTime"]) // interfaceStyle.value["atomicTime"] :原子时间,显示单个警告文字的最短时间
}