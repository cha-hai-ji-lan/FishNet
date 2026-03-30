import { ref} from "vue";
import { invoke } from "@tauri-apps/api/core";

export const hasChoose = ref(false)  // 是否在第一段选择网身
export const focusPart = ref("__NULL__")  // 当前注视的部位
export const netGroup = ref<any>("__NET_TEMPLATE__")

export const send_parma_to_cli = (param_json: any) => {
   console.log(param_json)
}
export const initCAD = () => {
   // invoke()
}