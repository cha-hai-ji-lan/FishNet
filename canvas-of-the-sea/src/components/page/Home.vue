<template>
  <div class="home-main">
    <div class="blank-17_5pe"></div>
    <div class="flex-r-div"><img class="main-icon" src="../../assets/icon.png" alt="">
      <h1>Canvas of the sea</h1>
      <div class="app-version">{{ appConfig['version'] }}</div>
    </div>
    <div class="flex-r-div home-subtitle">{{ welcomeTitle }} 欢迎回来.{{ careTitle }}</div>
    <div class="blank-10pe"></div>
    <div class="select-bar-frame">
      <SelectBar v-model="drawMode" :options="netTypes" placeholder="拖网类型"></SelectBar>
    </div>
    <input v-if="drawMode !== ''" v-model="netGroup['corePos']" type="text" :placeholder="'原点默认:' + coreConfig['defaultParam']['originPosition']">
    <div class="blank-10pe"></div>
    <div class="enter-frame">
      <div @click="() => { start_drawing() }" class="flex-r-div but-frame ban-select">
        <div class="flex-r-div">
          <NormalIcons whichIcon="newFile"></NormalIcons>
        </div>
        <div>新建绘图</div>
      </div>
      <div class="ready-info ban-select"
        :class="{ 'cadtool-ready': CADToolState === '__READY__', 'cadtool-wait': CADToolState === '__WAIT__', 'cadtool-fail': CADToolState === '__FAIL__' }">
        <div @click="reset_server()">
          <div>{{ CADToolStateInfo[CADToolState as keyof typeof CADToolStateInfo] }}</div>
        </div>
      </div>
    </div>

    <div class="blank-10pe"></div>
    <div v-if="typeof netGroup !== 'string' && netGroup['hasDraw'] !== false" @click="() => { back_drawing() }"
      class="flex-r-div but-frame ban-select">
      <div class="flex-r-div">
        返回绘图
      </div>
    </div>



  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { invoke } from "@tauri-apps/api/core";
import NormalIcons from '../../assets/icons/NormalIcons.vue';
import SelectBar from '../utils/SelectorBar.vue';
import { netTypes, isNewFile, cacheRouterPath, CADToolState, CADToolStateInfo } from '../../utils/Memory.ts'
import { set_content } from '../../utils/warn.ts'
import { useRouter } from "vue-router"; // 引入 useRoute
import { appConfig, coreConfig, fishNetEXE, twoNetT, fourNetT, sixNetT } from "../../utils/MainIndex.ts";
import { netGroup } from '../../utils/core/startdraw.ts'
import { init_cad_listen_group } from "../../utils/event.ts";

// 响应式变量存储当前时间
const currentTime = ref('');
const welcomeTitle = ref("__WELCOME_SENTENCES__")
const careTitle = ref("") // __CARE_SENTENCES__
const drawMode = ref("")

const router = useRouter()

onMounted(() => {
  updateTime(); // 立即更新一次时间
  console.log(typeof netGroup.value)
});

watch(drawMode, (NewVal: string) => {
  console.log(netGroup.value)
  switch (NewVal) {  // 纯数据对象深拷贝
    case '两片式':
      netGroup.value = JSON.parse(JSON.stringify(twoNetT.value))
      break;
    case '四片式':
      netGroup.value = JSON.parse(JSON.stringify(fourNetT.value))
      break;
    case '六片式':
      netGroup.value = JSON.parse(JSON.stringify(sixNetT.value))
      break;

    default:
      break;
  }
  console.log(netGroup.value)
})
const updateTime = () => {
  const now = new Date().getHours();
  currentTime.value = now.toLocaleString(); // 格式化时间为本地字符串
  if (Number(currentTime.value) >= 4 && Number(currentTime.value) <= 9) {
    welcomeTitle.value = "🌅早上好";
    careTitle.value = "又是元气满满的一天";
  } else if (Number(currentTime.value) > 9 && Number(currentTime.value) < 12) {
    welcomeTitle.value = "☀️上午好";
    careTitle.value = "清醒头脑,才思泉涌";
  } else if (Number(currentTime.value) >= 12 && Number(currentTime.value) < 15) {
    welcomeTitle.value = "🌞午间好";
    careTitle.value = "加油!";
  } else if (Number(currentTime.value) >= 15 && Number(currentTime.value) < 18) {
    welcomeTitle.value = "🌇下午好";
    careTitle.value = "祝你工作顺利完成,早点结束";
  } else if (Number(currentTime.value) >= 18 && Number(currentTime.value) < 24) {
    welcomeTitle.value = "⭐️晚上好";
    careTitle.value = "熬夜会损害我们的健康,注意早点休息";
  } else if (Number(currentTime.value) >= 0 && Number(currentTime.value) < 4) {
    welcomeTitle.value = "🌙午夜好";
    careTitle.value = "已经到凌晨了,这么晚工作对身体不好早点休息吧";
  }
  console.log(currentTime.value)
};

const start_drawing = () => {
  switch (drawMode.value) {
    case '两片式':
      isNewFile.value = true
      router.push("/draw-two-piece")
      break;
    case '四片式':
      set_content("四片式逻辑开发中...", 2)
      // isNewFile.value = true
      // router.push("/draw-four-piece")
      break;
    case '六片式':
      set_content("六片式逻辑开发中...", 2)
      // isNewFile.value = true
      // router.push("/draw-six-piece")
      break;

    default:
      set_content("请选择绘图类型后再开始绘制拖网.", 2)
      break;
  }
  if (netGroup.value['corePos'] === "") {
    netGroup.value['corePos'] = coreConfig.value['defaultParam']['originPosition']
  }
}

const back_drawing = () => {
  if (cacheRouterPath.value !== '__NULL__') {
    router.push(cacheRouterPath.value)
  }
}

const reset_server = () => {
  if (CADToolState.value === "__FAIL__") {
    init_cad_listen_group()
    invoke("reset_cli", { acadToolPath: fishNetEXE.value, command1: ["-config-set", JSON.stringify(coreConfig.value["defaultParam"])] })
  }
}


</script>
<style scoped>
h1 {
  font-size: 6vmin;
  margin-left: 2vmin;
  font-family: "Judou-Heavy", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
}

.home-main {
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: column;
  width: 100%;
  flex: 1%;
  /* height: 95vh; */
  background-color: rgba(var(--background), var(--transparency));
  /* background-color: rgba(33, 40, 48, 1); */
  /* 淡灰色底色 */
  background-image:
    linear-gradient(to right, rgba(var(--border-line), var(--transparency)) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(var(--border-line), var(--transparency)) 1px, transparent 1px);
  /* 创建虚线网格 */
  background-size: var(--grid-size) var(--grid-size);

  & input {

    /* 移除所有默认样式 */
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;

    /* 重置边框和背景 */
    border: 2px solid rgba(var(--title), var(--transparency));
    outline: none;
    background: transparent;

    /* 重置其他样式 */
    padding: 0;
    margin: 0;
    margin-top: 2.5vmin;
    font-family: "Judou-Heavy", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;

    font-size: inherit;
    color: inherit;
    border-radius: 0;
    background-color: rgba(var(--border-line), var(--transparency));
    border-radius: 1vmin;
    text-align: center;
    width: 30vmin;
    height: 4vmin;

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
}

.blank {
  width: 100%;
  height: 17.5%;
}

.main-icon {
  width: 20vmin;
  height: 20vmin;
}

.enter-frame {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: row;

  & .ready-info {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    font-size: 2vmin;
    margin-left: 2vmin;
    width: 12vmin;
    height: 5vmin;
    border-radius: 1.25vmin;
    border-top: 1px dashed rgba(var(--warn-note), var(--transparency));
    border-bottom: 1px dashed rgba(var(--warn-note), var(--transparency));
    background-color: rgba(var(--warn-note), var(--pTransparency));

    &.cadtool-ready {
      border-top: 1px dashed rgba(var(--ready-note), var(--transparency));
      border-bottom: 1px dashed rgba(var(--ready-note), var(--transparency));
      background-color: rgba(var(--ready-note), var(--pTransparency));
    }

    &.cadtool-wait {
      border-top: 1px dashed rgba(var(--warn-note), var(--transparency));
      border-bottom: 1px dashed rgba(var(--warn-note), var(--transparency));
      background-color: rgba(var(--warn-note), var(--pTransparency));

    }

    &.cadtool-fail {
      border-top: 1px dashed rgba(var(--error-note), var(--transparency));
      border-bottom: 1px dashed rgba(var(--error-note), var(--transparency));
      background-color: rgba(var(--error-note), var(--pTransparency));
      box-shadow: 0 0 1.5vmin rgba(var(--error-note), 0.75);
      transition: transform 100ms;

      &:hover {
        filter: brightness(1.25);
      }

      &:active {
        filter: brightness(1.5);
        transform: scale(0.8);
      }
    }
  }


}

.flex-r-div {
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: row;
}

.select-bar-frame {
  font-family: "Judou-Heavy", "宋体", 'Courier New', Courier, monospace;
  font-size: 2.5vmin;
  text-align: center;
  width: 35vmin;
  height: 6vmin;
  background-color: rgba(var(--title), var(--transparency));
  border-radius: 2vmin;
  /* filter: brightness(0.75); */
}

.but-frame {

  font-size: 3vmin;
  font-family: "Judou-Heavy", "宋体", 'Courier New', Courier, monospace;
  width: fit-content;
  scale: 1;
  padding: 1vmin 2vmin;
  border-radius: 2vmin;
  /* border : 2px solid var(--button); */
  background: linear-gradient(45deg, rgba(var(--border-line), var(--transparency)), rgba(var(--button), var(--transparency)));
  background-size: cover;
  /* 确保渐变覆盖整个区域 */
  box-shadow:
    -0.25vmin -0.25vmin 1.75vmin rgba(var(--border-line), var(--transparency)),
    0.25vmin 0.25vmin 1.75vmin rgba(var(--button), var(--transparency)),
    -0.75vmin -0.75vmin 1.75vmin rgba(var(--button), var(--transparency)),
    0.75vmin 0.75vmin 1.75vmin rgba(var(--border-line), var(--transparency));

  transition: scale 100ms ease;

  &:hover {
    filter: brightness(1.2);
  }

  &:active {
    scale: 0.8;
  }
}

.app-version {
  margin-left: 2vmin;
  width: fit-content;
  height: fit-content;
  border: 2px solid #1177bb;
  background-color: rgba(17, 119, 187, 0.3);
  border-radius: 2vmin;
  padding: 0.5vmin 1vmin;
  font-size: 3.5vmin;
}

.home-subtitle {
  font-size: 2.75vmin;
}
</style>