import { ref, reactive, onMounted } from "vue";
import { twoNetT } from "../MainIndex.ts";
onMounted(() => {
    if (netGroup.value === ""){
        netGroup.value = twoNetT.value
    }

})
export const netGroup = ref<any>("")