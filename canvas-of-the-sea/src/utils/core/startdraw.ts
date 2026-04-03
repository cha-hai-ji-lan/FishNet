import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { set_content } from "../warn.ts"

export const hasChoose = ref(false)  // 是否在第一段选择网身
export const focusPart = ref("__NULL__")  // 当前注视的部位
export const netGroup = ref<any>("__NET_TEMPLATE__")

export const DTC = ref<DesignTreeCtr | null>(null)

export const send_parma_to_cli = (param_list: string[]) => {
   console.log(param_list)
   invoke("send_param_to_cli", { command: param_list })
}

class DesignTreeCtr {
   private net_type = ref<string>("__NET_TYPE__")
   /**
    * id_obj: 存储各个 设计树根节点
    * 默认对应 两片式
    * 0: 网身
    * 1: 上网袖
    * 2: 下网袖
   */
   private id_obj = ref<HTMLDetailsElement[]>([])
   private tree_node = ref<any>([])
   constructor(netType: string, id_list: string[]) {
      this.init(netType, id_list)
   }
   /**
    * 初始化设计树控制器
    * 设定拖网类型
   */
   init(netType: string, id_list: string[]): boolean {
      this.net_type.value = netType
      id_list.forEach(element => {
         this.id_obj.value.push(document.getElementById(element) as HTMLDetailsElement)
      })
      return true
   }
   flesh_node() {
      switch (this.net_type.value) {
         case "两片式":
            /**
             * let index = 1 因为组内默认会有"segment"字段所以空应该索引为 1
             * 
            */
            for (let index = 1; index < netGroup.value["netBody"].length; index++) {
               const div_element = document.createElement("div")
               div_element.innerHTML = `段${index + 1}`
               this.id_obj.value[0].appendChild(div_element)
            }
            for (let index = 1; index < netGroup.value["leftSleeve"].length; index++) {
               const div_element = document.createElement("div")
               div_element.innerHTML = `段${index + 1}`
               this.id_obj.value[0].appendChild(div_element)
            }
            for (let index = 1; index < netGroup.value["rightSleeve"].length; index++) {
               const div_element = document.createElement("div")
               div_element.innerHTML = `段${index + 1}`
               this.id_obj.value[0].appendChild(div_element)
            }

            break;
         case "四片式":

            break;
         case "六片式":

            break;
         default:
            set_content("设计树类型错误", 3)
            break;
      }
   }
}
export const canvasRenderer = (netType: string, id_list: string[]) => {
   DTC.value = new DesignTreeCtr(netType, id_list)
}
export default DesignTreeCtr