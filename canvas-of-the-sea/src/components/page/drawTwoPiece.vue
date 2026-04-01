<template>
  <div class="draw-two-piece-main">
    <div class="left-part">
      <div class="parameters-table" :class="{ 'show-para': showPara }"></div>
      <div class="parameters-switch ban-select" @click="() => { show_table('para') }">{{ showPara ? "隐藏特征树" : "显示特征树" }}
      </div>
    </div>
    <div class="mid-part">
      <TwoPieceBody v-if="focusPart === 'two-net-body'"></TwoPieceBody>
      <TwoPieceLeftSleeve v-if="focusPart === 'two-left-sleeve'"></TwoPieceLeftSleeve>
      <TwoPieceRightSleeve v-if="focusPart === 'two-right-sleeve'"></TwoPieceRightSleeve>
    </div>
    <div class="right-part" :class="{ 'show-canvas': showCanvas }">
      <div class="canvas-switch ban-select" @click="() => { show_table('canvas') }">{{ showCanvas ? "隐藏画布" : "显示画布" }}
      </div>
      <canvas id="two-piece-canvas" class="two-piece-canvas"></canvas>
    </div>
  </div>
  <div class="float-option-version" :class="{ 'show-option-version': choosePart }">
    <div class="choose-column ban-select" @click="() => { show_table('part') }">{{ choosePart ? "取消选择" : "部位选择" }}</div>
    <div class="choose-part">
      <div class="blank-10p"></div>
      <div>
        <span @click="() => { choose_part('left-sleeve') }" class="net-part">
          <NetShowIcons whichIcon="left-sleeve"></NetShowIcons>
        </span>
        <span @click="() => { choose_part('right-sleeve') }" class="net-part">
          <NetShowIcons whichIcon="right-sleeve"></NetShowIcons>
        </span>
      </div>
      <div>
        <span @click="() => { choose_part('net-body') }" class="net-part"
          :class="{ 'choose-first': hasChoose === false }">
          <NetShowIcons whichIcon="net-body"></NetShowIcons>
        </span>
      </div>
      <div class="blank-10p"></div>
    </div>
  </div>
</template>
<script setup lang="ts">

import { ref, onMounted } from 'vue';
// import { invoke } from "@tauri-apps/api/core";
import NetShowIcons from '../../assets/icons/NetShowIcons.vue';
import TwoPieceBody from '../../components/interface/TwoPieceBody.vue';
import TwoPieceLeftSleeve from '../../components/interface/TwoPieceLeftSleeve.vue';
import TwoPieceRightSleeve from '../../components/interface/TwoPieceRightSleeve.vue';
import { hasChoose, focusPart, netGroup } from '../../utils/core/startdraw.ts'
import { set_content } from '../../utils/warn.ts'
import { isNewFile } from '../../utils/Memory.ts'
import { canvasRenderer } from "../../utils/canvasRenderer.ts";

// import { coreConfig } from '../../utils/MainIndex.ts'
const choosePart = ref(false)
const showCanvas = ref(false)
const showPara = ref(false)

onMounted(() => {
    canvasRenderer.init('two-piece-canvas')  // 创建画布
  if (isNewFile.value === true) {
    console.log(netGroup.value)
    show_table('part')  // 新文件进入后显示 部位选择
    hasChoose.value = false;
    focusPart.value = "__NULL__"
  }
})
const show_table = (who: string) => {
  switch (who) {
    case 'part':
      if (choosePart.value) {
        choosePart.value = false;
      } else {
        choosePart.value = true;
      }
      break;

    case 'canvas':
      if (showCanvas.value) {
        showCanvas.value = false;
      } else {
        showCanvas.value = true;
        setTimeout(()=>{
          console.log("设置画布尺寸")
          canvasRenderer.resize()
        },2000)
      }
      break;
    case 'para':
      if (showPara.value) {
        showPara.value = false;
      } else {
        showPara.value = true;
      }
      break;
    default:
      break;
  }

}

const choose_part = (who: string) => {
  // invoke("send_param_to_cli", {command:["-i",JSON.stringify(coreConfig.value)]})
  switch (who) {
    case 'net-body':
      isNewFile.value = false  // 已进行了一步操作,可看作不是新文件
      hasChoose.value = true;
      focusPart.value = "two-net-body"
      break;
    case 'right-sleeve':
      if (hasChoose.value == true) {  // 如果已经有网身段 则侧面印证了可以绘制其他部位
        focusPart.value = "two-right-sleeve"
      }
      break;
    case 'left-sleeve':
      if (hasChoose.value == true) {
        focusPart.value = "two-left-sleeve"
      }
      break;

    default:
      break;
  }
  if (hasChoose.value == true) {
    show_table('part')
  } else {
    set_content("请在第一步选择绘制网身,否则无法参数化建模", 2)
  }
}
</script>
<style scoped>
.draw-two-piece-main {
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: row;
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
}

.float-option-version {
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: row;
  position: absolute;
  bottom: 0;
  right: 0;
  height: 95vh;
  width: 4.5vmin;
  z-index: 1;
  transition: width 0.75s ease;
  pointer-events: none;

  &.show-option-version {
    width: 40vmin
  }

  & .choose-column {
    font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    writing-mode: vertical-rl;
    /* 从上到下，从右到左 */
    text-orientation: upright;
    /* 保持字符直立 */
    background: transparent;
    border: 2px solid rgba(var(--font), var(--transparency));
    border-right: 0px solid rgba(var(--font), var(--transparency));
    border-radius: 1vmin 0 0 2.5vmin;
    padding: 1vmin;
    /* padding-right: 0.5vmin; */
    pointer-events: auto;
  }

  & .choose-part {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background: rgba(var(--border-line), var(--transparency));
    background-image:
      linear-gradient(to right, rgba(var(--title), var(--transparency)) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(var(--title), var(--transparency)) 1px, transparent 1px);
    /* 创建虚线网格 */
    background-size: var(--grid-size) var(--grid-size);
    border-left: 2px solid rgba(var(--font), var(--transparency));
    border-radius: 2.5vmin 0 0 2.5vmin;
    height: 100%;
    pointer-events: auto;

    & .net-part {
      &:hover {
        filter: drop-shadow(0 0 0.75em rgba(243, 89, 122, 0.75));
      }

      &:active {
        filter: brightness(1.35);
      }
    }

    & .choose-first {
      filter: drop-shadow(0 0 0.75em rgba(243, 89, 122, 0.75));
    }
  }
}



.left-part {
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: row;
  width: fit-content;
  height: 100%;

  & .parameters-switch {
    font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    writing-mode: vertical-rl;
    text-orientation: upright;
    background: transparent;
    border: 2px solid rgba(var(--font), var(--transparency));
    border-left: 0px solid rgba(var(--font), var(--transparency));
    border-radius: 0 2.5vmin 2.5vmin 0;
    padding: 1vmin;

  }

  & .parameters-table {
    height: 100%;
    transition: width 0.75s ease;
    background-color: rgba(var(--border-line), var(--transparency));
    width: 0;
    border-right: 2px solid rgba(var(--font), var(--transparency));
    border-radius: 0 2.5vmin 2.5vmin 0;
    background-image:
      linear-gradient(to right, rgba(var(--title), var(--transparency)) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(var(--title), var(--transparency)) 1px, transparent 1px);
    /* 创建虚线网格 */
    background-size: var(--grid-size) var(--grid-size);

    &.show-para {
      transition: width 0.75s ease;
      width: 30vmin;
    }
  }


}

.mid-part {
  flex-grow: 1;
  height: 100%;
}

.right-part {
  width: fit-content;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  height: 100%;

  /* 让canvas出现过渡自然 */
  &.show-canvas {
    & .two-piece-canvas {
      transition: width 0.75s ease;
      height: 100%;
      width: 40vmin;
    }
  }

  & .canvas-switch {
    font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    width: fit-content;
    writing-mode: vertical-rl;
    text-orientation: upright;
    margin-bottom: 20vmin;
    background: transparent;
    border: 2px solid rgba(var(--font), var(--transparency));
    border-right: 0px solid rgba(var(--font), var(--transparency));
    border-radius: 2.5vmin 0 0 1vmin;
    padding: 1vmin;
  }

  & .two-piece-canvas {
    background: rgba(var(--border-line), var(--transparency));
    transition: width 0.75s ease;
    height: 100%;
    width: 0vmin;
    border-left: 2px solid rgba(var(--font), var(--transparency));
    border-radius: 2.5vmin 0 0 2.5vmin;
    background-image:
      linear-gradient(to right, rgba(var(--title), var(--transparency)) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(var(--title), var(--transparency)) 1px, transparent 1px);
    /* 创建虚线网格 */
    background-size: var(--grid-size) var(--grid-size);
  }

}


@keyframes active-icon {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.85);
  }

  100% {
    transform: scale(1);
  }

}
</style>