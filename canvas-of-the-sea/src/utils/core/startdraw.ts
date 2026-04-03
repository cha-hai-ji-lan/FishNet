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
   private net_type: string = "__NET_TYPE__"
   /**
    * id_obj: 存储各个 设计树根节点
    * 默认对应 两片式
    * 0: 网身
    * 1: 上网袖
    * 2: 下网袖
   */
   private id_obj: HTMLDetailsElement[] = []
   private tree_node: any = []
   constructor(netType: string, id_list: string[]) {
      this.init(netType, id_list)
   }
   /**
    * 初始化设计树控制器
    * 设定拖网类型
   */
   init(netType: string, id_list: string[]): boolean {
      this.net_type = netType
      id_list.forEach(element => {
         this.id_obj.push(document.getElementById(element) as HTMLDetailsElement)
      })
      this.tree_node = Array(3).fill(null).map(() => [])
      console.log(this.tree_node)
      return true
   }
   flesh_node() {
      switch (this.net_type) {
         case "两片式":
            /**
             * let index = 1 因为组内默认会有"segment"字段所以空应该索引为 1
             * 
            */
            for (const key in netGroup.value["netBody"]) {
               if (key === "segment") continue
               if (this.tree_node[0].includes(`网身段${key}`)) continue // 跳过已存在的节点
               this.tree_node[0].push(`网身段${key}`)
               const div_element = document.createElement("div")
               div_element.innerHTML = `网身段${key}`
               this.id_obj[0].appendChild(div_element)
            }
            for (const key in netGroup.value["leftSleeve"]) {
               if (key === "segment") continue
               if (this.tree_node[1].includes(`上袖段${key}`)) continue
               this.tree_node[1].push(`上袖段${key}`)
               const div_element = document.createElement("div")
               div_element.innerHTML = `上袖段${key}`
               this.id_obj[1].appendChild(div_element)
            }
            for (const key in netGroup.value["rightSleeve"]) {
               if (key === "segment") continue
               if (this.tree_node[2].includes(`下袖段${key}`)) continue
               this.tree_node[2].push(`下袖段${key}`)
               const div_element = document.createElement("div")
               div_element.innerHTML = `下袖段${key}`
               this.id_obj[1].appendChild(div_element)
            }

            break;
         case "四片式":

            break;
         case "六片式":

            break;
         default:
            console.log(this.id_obj)
            console.log(this.net_type)
            console.log(this.tree_node)
            set_content(`设计树类型错误 当前类型为${this.net_type}`, 3)
            break;
      }
   }
}
export const design_tree_ctr = (netType: string, id_list: string[]) => {
   DTC.value = new DesignTreeCtr(netType, id_list)
}
export default DesignTreeCtr