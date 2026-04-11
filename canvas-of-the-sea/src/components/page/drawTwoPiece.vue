<template>
  <div class="draw-two-piece-main">
    <div class="left-part">
      <div class="parameters-table of-x-hid" :class="{ 'show-para': showPara }">
        <div class="design-tree-head of-x-hid">
          <div class="tolerate" @click="() =>{design_redraw()}">
            <NormalIcons whichIcon="redraw"></NormalIcons>
          </div>
        </div>
        <div class=" design-tree-datail w100 ban-select">
          <details id="two-net-body" class="design-tree of-x-hid">
            <summary class="design-summary of-x-hid"><span>网身</span></summary>
          </details>
          <details id="two-left-sleeve" class="design-tree of-x-hid">
            <summary class="design-summary of-x-hid">上网翼</summary>
          </details>
          <details id="two-right-sleeve" class="design-tree of-x-hid">
            <summary class="design-summary of-x-hid">下网翼</summary>
          </details>
        </div>

      </div>
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
import NormalIcons from '../../assets/icons/NormalIcons.vue';

import { hasChoose, focusPart, netGroup } from '../../utils/core/startdraw.ts'
import { set_content } from '../../utils/warn.ts'
import { isNewFile } from '../../utils/Memory.ts'
import { canvasRenderer, CR } from "../../utils/canvasRenderer.ts";
import { design_tree_ctr } from "../../utils/core/startdraw.ts"
import { DTC } from "../../utils/core/startdraw.ts"
// import { coreConfig } from '../../utils/MainIndex.ts'
const choosePart = ref(false)
const showCanvas = ref(false)
const showPara = ref(false)

onMounted(() => {
  design_tree_ctr("两片式", ["two-net-body", "two-left-sleeve", "two-right-sleeve"])
  canvasRenderer('two-piece-canvas')  // 创建画布
  if (isNewFile.value === true) {
    console.log(netGroup.value)
    show_table('part')  // 新文件进入后显示 部位选择
    hasChoose.value = false;
    focusPart.value = "__NULL__"
  }
})
const show_table = (who: string) => {
  DTC.value?.flesh_node()  // 打开设计树就刷新节点
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
        CR.value?.set_canvas_size(false)
        showCanvas.value = false;
      } else {
        showCanvas.value = true;
        setTimeout(()=>{
          CR.value?.set_canvas_size(true)
        }, 800)
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

const design_redraw = () => {
  DTC.value?.flesh_node()  // 触发重绘前刷新设计树
  console.log("触发重绘")
  DTC.value?.flesh_node()  // 触发重绘后刷新设计树
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
    overflow-y: auto;

    &.show-para {
      transition: width 0.75s ease;
      width: 30vmin;
    }

    & .design-tree-head {
      width: 100%;
      height: 5vmin;
      display: flex;
      justify-content: start;
      justify-self: center;
      align-items: center;
      flex-direction: row;
      background-color: rgba(var(--title), var(--transparency));
      border-top: 2px solid rgba(var(--font), var(--transparency));
      border-bottom: 2px solid rgba(var(--font), var(--transparency));
    }

    & .design-tree-datail {
      max-height: 90vh;
      overflow-y: auto;
      overflow-x: hidden;


      &::-webkit-scrollbar {
        width: 1vmin;
        /* 垂直滚动条宽度 */
        height: 1vmin;
        /* 水平滚动条高度 */

      }

      &::-webkit-scrollbar-track {
        background: rgba(var(--title), var(--pTransparency));
        /* 滚动条轨道背景色 */
        border-radius: 4px;
      }

      &::-webkit-scrollbar-thumb {
        background: rgba(var(--button), var(--pTransparency));
        /* 滚动条滑块颜色 */
        border-radius: 4px;
      }

      &::-webkit-scrollbar-thumb:hover {
        filter: brightness(1.2);
        /* 滑块悬停时的颜色 */
      }

      & .design-tree {
        display: flex;
        justify-content: start;
        align-items: center;
        flex-direction: column;
        font-size: 3vmin;
        width: 30vmin;
        text-align: center;
        border: 1px solid rgba(var(--border-line), var(--transparency));
        border-radius: 1vmin;
        background-color: rgba(var(--background), var(--transparency));

        & .design-summary {
          display: flex;
          justify-content: center;
          align-items: center;
          width: 80%;
          /* height: 5vmin; */
          user-select: none;
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;
          border-radius: 1vmin;
          border: 1px dashed rgba(var(--normal-note), var(--transparency));
          background-color: rgba(var(--title), var(--pTransparency));
        }

        &[open] {
          border: 1px solid rgba(var(--font), var(--transparency));

          & .design-summary {
            border: 2px solid rgba(var(--normal-note), var(--transparency));
          }
        }

      }
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