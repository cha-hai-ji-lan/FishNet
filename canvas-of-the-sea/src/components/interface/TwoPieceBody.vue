<template>
    <div class="two-piece-body" v-if="netGroup['netBody'] && netGroup['netBody']['segment'] > 0">
        <div class="blank-10pe"></div>
        <div class="item ban-select">
            <div class="part-title "><span>网身</span></div>
            <div class="part-title segments"><span>第{{ segment }}段</span></div>
            <div v-if="netGroup['drawNetSac']" class="part-title segments-port"><span>网囊段</span></div>
        </div>

        <div class="w100 ban-select">
            <div class="item ">
                <div class="item-title">网身目大:</div><input v-model="netGroup['netBody'][`${segment}`][0]"
                    :placeholder="coreConfig['parameterInheritance'] ? netGroup['netBody'][`${segment - 1}`]?.[0] || '目大' : '目大'"
                    type="text">
            </div>
            <div class="item">
                <div class="item-title">网身纵向目数:</div><input v-model="netGroup['netBody'][`${segment}`][1]"
                    :placeholder="coreConfig['parameterInheritance'] ? netGroup['netBody'][`${segment - 1}`]?.[1] || '纵向目数' : '纵向目数'"
                    type="number">
            </div>
            <div class="item">
                <div class="item-title">网身横向目数:</div><input v-model="netGroup['netBody'][`${segment}`][2]"
                    :placeholder="coreConfig['parameterInheritance'] ? netGroup['netBody'][`${segment - 1}`]?.[2] || '横向目数' : '横向目数'"
                    type="number">
            </div>
            <div class="item" v-if="netGroup['drawNetSac'] === false">
                <div class="item-title">边旁剪裁斜率:</div><input v-model="netGroup['netBody'][`${segment}`][3]"
                    placeholder="剪裁斜率默认 1:1" type="text">
            </div>
            <div class="item">
                <div class="item-title">线径规格:</div><input v-model="netGroup['netBody'][`${segment}`][4]"
                    :placeholder="coreConfig['parameterInheritance'] ? netGroup['netBody'][`${segment - 1}`]?.[4] || '线径规格默认:' + coreConfig['defaultParam']['wireDiameter'] : '线径规格默认:' + coreConfig['defaultParam']['wireDiameter']"
                    type="text">
            </div>
            <div class="item">
                <div class="item-title choose-button" :class="{ 'lost-color': netGroup['drawNetSac'] === false }"
                    @click="() => { draw_net_sac() }">{{ netGroup['drawNetSac'] ?
                        '绘制网囊' : '网囊段' }}</div>
                <div class="item-title choose-button"
                    :class="{ 'lost-color': coreConfig['parameterInheritance'] === false }"
                    @click="() => { coreConfig['parameterInheritance'] = !coreConfig['parameterInheritance'] }">{{
                        coreConfig['parameterInheritance'] ?
                            '参数继承' : '参数摒弃' }}</div>
                <div class="item-title choose-button"
                    :class="{ 'lost-color': coreConfig['defaultParam']['-useSegmentSpacing'] === false }"
                    @click="() => { coreConfig['defaultParam']['-useSegmentSpacing'] = !coreConfig['defaultParam']['-useSegmentSpacing'] }">
                    {{
                        coreConfig['defaultParam']['-useSegmentSpacing'] ?
                            '启用横向间隙' : '禁用横向间隙' }}</div>
            </div>
        </div>
        <div class="w100 ban-select">
            <div class="item">
                <div @click="() => { next_segment() }" class="item-title item-button ban-select">下一段</div>
                <div @click="() => { give_up_draw() }" class="item-title item-button-give-up ban-select">放弃</div>
            </div>
            <div class="item">
                <div @click="() => { clean_param() }" class="item-title item-button-warn ban-select">清空</div>
                <div @click="() => { clean_param() }" class="item-title item-button-warn ban-select">全部重置</div>
            </div>
            <div class="item">
                <div class="item-title item-button-warn ban-select">退一步</div>
                <div class="item-title item-button-warn ban-select">进一步</div>
            </div>
            <div class="item">
                <div class="item-title item-button-fin ban-select"><span>完成</span></div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { useRoute, useRouter } from 'vue-router';
import { cacheRouterPath, isNewFile } from "../../utils/Memory.ts";
import { netGroup, send_parma_to_cli } from "../../utils/core/startdraw.ts";
import { init_cad_listen_group } from "../../utils/event.ts";
import { coreConfig, fishNetEXE } from "../../utils/MainIndex.ts";
import { DTC } from "../../utils/core/startdraw.ts"
const segment = ref<number>(1)
const route = useRoute()
const router = useRouter()

onMounted(() => {
    console.log("进入网身段")
    cacheRouterPath.value = route.path;  // 缓存当前路由
    if (netGroup.value['netBody'] && netGroup.value['netBody']['segment'] === 0) {
        netGroup.value['netBody']['segment'] += 1;
        netGroup.value['netBody'][`${netGroup.value['netBody']['segment']}`] = Array(5).fill(null);
    };
    segment.value = netGroup.value['netBody']?.['segment'] || 0;
    DTC.value?.flesh_node()  // 刷新设计树

})

watch(() => netGroup.value['netBody']['segment'], () => {
    segment.value = netGroup.value['netBody']['segment'];
})
// watch(() => netGroup.value['netBody'], () => {
//     // canvasRenderer.drawFromNetGroup(netGroup.value, 'netBody')
// }, { deep: true })
const next_segment = () => {
    cacheRouterPath.value = route.path;
    netGroup.value["hasDraw"] = true;
    if (coreConfig.value['parameterInheritance']) {
        check_pre_segment()
    }
    set_default_param()
    send_parma_to_cli(collate_param());
    netGroup.value['netBody']['segment'] += 1;
    netGroup.value['netBody'][`${netGroup.value['netBody']['segment']}`] = Array(5).fill(null);
    DTC.value?.flesh_node()
}

/**
 * 检查上一段参数,如果本段有空位参数则填写前一段的参数
*/
const check_pre_segment = () => {
    if (!netGroup.value['netBody'][`${segment.value - 1}`]) return;
    netGroup.value['netBody'][`${segment.value}`].forEach((val: string | number | null, index: number) => {
        if (val === null && netGroup.value['netBody'][`${segment.value - 1}`][index] !== null) {
            netGroup.value['netBody'][`${segment.value}`][index] = netGroup.value['netBody'][`${segment.value - 1}`][index]
        }
    });
}

const set_default_param = () => {
    if (netGroup.value['netBody'][`${segment.value}`][4] === null) netGroup.value['netBody'][`${segment.value}`][4] = coreConfig.value['defaultParam']['wireDiameter']

    if (netGroup.value['netBody'][`${segment.value}`][3] === null && netGroup.value['drawNetSac']) { netGroup.value['netBody'][`${segment.value}`][3] = "1:0" } else netGroup.value['netBody'][`${segment.value}`][3] = "1:1"
    netGroup.value['netBody'][`${segment.value}`].forEach((val: string | number | null, index: number) => {
        if (val === null) netGroup.value['netBody'][`${segment.value}`][index] = "None"
    });
}

const collate_param = (): string[] => {
    let param: string[] = []
    param.push("-i")
    param.push(`${netGroup.value['netBody'][`${segment.value}`].slice(0, 4)}`)
    param.push("-cfg-wireDiameter")
    param.push(netGroup.value['netBody'][segment.value][4])  // 该元素本来就是字符串无需``
    if (netGroup.value['drawNetSac']) param.push("-drawNetSac")
    if (coreConfig.value['defaultParam']['-useSegmentSpacing']) param.push("-useSegmentSpacing")
    return param
}

const give_up_draw = () => {
    router.push('/')  // 返回首页
    isNewFile.value = true; // 放弃绘制意味着本项目结束,后续操作可视为一个新文件
    netGroup.value = "__NET_TEMPLATE__"  // 清空组
    init_cad_listen_group()
    invoke("reset_cli", { acadToolPath: fishNetEXE.value, command1: ["-config-set", JSON.stringify(coreConfig.value["defaultParam"])] })
}

const clean_param = () => {
    netGroup.value['netBody'][`${segment.value}`].fill(null)
}

const draw_net_sac = () => {
    netGroup.value['drawNetSac'] = !netGroup.value['drawNetSac']
    coreConfig.value['parameterInheritance'] = false
}


</script>
<style scoped>
.two-piece-body {
    font-family: "思印宋", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    display: flex;
    justify-content: start;
    align-items: start;
    flex-direction: column;
    width: 100%;
    height: 100%;
    font-size: 2.75vmin;

    & table {
        width: 100%;
    }

    & .item {
        display: flex;
        justify-content: start;
        align-items: start;
        flex-direction: row;
        width: 100%;
        border-bottom: 2px solid rgba(var(--button), var(--transparency));
        padding-top: 1vmin;
        padding-bottom: 1vmin;


        /* 数字输入框移除上下箭头 */
        & input[type="number"]::-webkit-inner-spin-button,
        & input[type="number"]::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }

        & input {
            /* 移除所有默认样式 */
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;

            /* 重置边框和背景 */
            border: 2px solid rgba(var(--title), var(--transparency));
            ;
            outline: none;
            background: transparent;

            /* 重置其他样式 */
            padding: 0;
            margin: 0;
            font-family: inherit;
            font-size: inherit;
            color: inherit;
            border-radius: 0;

            width: 50%;
            max-width: 400px;
            background-color: rgba(var(--border-line), var(--transparency));
            border-radius: 1vmin;
            text-align: center;
            height: 3vmin;

            &:hover {
                filter: drop-shadow(0 0 0.25em rgba(var(--normal-note), 0.75));
            }

            &:active {
                border: 2px solid rgba(var(--normal-note), 1);
            }

            &:focus {
                border: 2px dashed rgba(var(--normal-note), 0.75);
            }
        }

        & .part-title {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: row;
            font-size: 5vmin;
            font-weight: bold;

            &.segments-port {
                margin-left: 2vmin;
                padding: 0.5vmin 1vmin;
                border: 2px solid rgba(var(--warn-note), 1);
                background-color: rgba(var(--warn-note), var(--pTransparency));
                border-radius: 2vmin;
            }
        }

        & .segments {
            margin-left: 2vmin;
            padding: 0.5vmin 1vmin;
            border: 2px solid rgba(var(--normal-note), 1);
            background-color: rgba(var(--normal-note), var(--pTransparency));
            border-radius: 2vmin;
        }

        & .item-title {
            width: 50%;
            max-width: 300px;

            &.choose-button {
                width: fit-content;
                padding: 0 1vmin;
                text-align: center;
                background-color: rgba(var(--ready-note), var(--pTransparency));
                border: 2px solid rgba(var(--ready-note), 1);
                border-radius: 1vmin;
                margin: 0 1vmin;
            }

            &.item-button {
                width: calc(40% - 2vmin);
                text-align: center;
                background-color: rgba(var(--normal-note), var(--pTransparency));
                border: 2px solid rgba(var(--normal-note), 1);
                border-radius: 1vmin;
                margin: 0 1vmin;
            }

            &.item-button-warn {
                width: calc(40% - 2vmin);
                text-align: center;
                background-color: rgba(var(--warn-note), var(--pTransparency));
                border: 2px solid rgba(var(--warn-note), 1);
                border-radius: 1vmin;
                margin: 0 1vmin;


            }

            &.item-button-give-up {

                width: calc(40% - 2vmin);
                text-align: center;
                background-color: rgba(var(--error-note), var(--pTransparency));
                border: 2px solid rgba(var(--error-note), 1);
                border-radius: 1vmin;
                margin: 0 1vmin;
            }

            &.lost-color {
                border: 2px solid rgba(var(--normal-note), 1);
                background-color: rgba(var(--normal-note), var(--pTransparency));
            }

            &.item-button-fin {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: row;
                height: 5vmin;
                width: calc(40% - 2vmin);
                max-width: 400px;
                text-align: center;
                background-color: rgba(var(--normal-note), var(--pTransparency));
                border: 2px solid rgba(var(--normal-note), 1);
                border-radius: 1vmin;
                margin: 0 15vmin;
            }
        }
    }
}
</style>