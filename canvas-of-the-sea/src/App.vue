<template>
  <main class="container">
    <div data-tauri-drag-region class="main-head">
      <div data-tauri-drag-region class="title-head left-head">
        <img class="main-base-icon" src="./assets/icon.png" alt="">
      </div>
      <div data-tauri-drag-region class="title-head mid-head"></div>
      <div data-tauri-drag-region class="title-head right-head">
        <div @click="title_bar_click('pin')">
          <BaseIcon :whichIcon="baseIconCtr['pin']"></BaseIcon>
        </div>
        <div @click="title_bar_click('minimize')">
          <BaseIcon whichIcon="minimize"></BaseIcon>
        </div>
        <div @click="title_bar_click('maximize')">
          <BaseIcon :whichIcon="baseIconCtr['maximize']"></BaseIcon>
        </div>
        <div @click="title_bar_click('close')">
          <BaseIcon whichIcon="close"></BaseIcon>
        </div>

      </div>

    </div>
    <RouterView></RouterView>
  </main>
</template>
<script setup lang="ts">

import { ref, onMounted } from "vue";
import { RouterView } from 'vue-router';
import { invoke } from "@tauri-apps/api/core";
import { Window } from "@tauri-apps/api/window";

import { init_app } from "./utils/MainIndex";
import BaseIcon from "./assets/icons/BaseIcon.vue";

const appWindow = Window.getCurrent()

const baseIconCtr = ref({ "maximize": "maximize-max", "pin": "pin" })  // 控制窗口最大化和钉住屏幕图标

onMounted(async () => {
  await init_app();
})

const title_bar_click = (mode: string) => {

  switch (mode) {
    case 'minimize':
      appWindow.minimize()
      break;
    case 'maximize':
      if (baseIconCtr.value["maximize"] === "maximize-max") {
        baseIconCtr.value["maximize"] = "maximize-min"
        appWindow.toggleMaximize();
      } else if (baseIconCtr.value["maximize"] === "maximize-min") {
        baseIconCtr.value["maximize"] = "maximize-max"
        appWindow.toggleMaximize();
      }
      break;
    case 'pin':
      if (baseIconCtr.value["pin"] === "pin") {
        baseIconCtr.value["pin"] = "pin-ing"
        appWindow.setAlwaysOnTop(true);
      } else if (baseIconCtr.value["pin"] === "pin-ing") {
        baseIconCtr.value["pin"] = "pin"
        appWindow.setAlwaysOnTop(false);

      }
      break;
    case 'close':
      appWindow.close();
      break;
    default:

      break;
  }

}

</script>



<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* 确保容器占满整个视口高度 *
  /* border: 0.25vmin solid #fff */
}

.main-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 5vh;
  max-height: 31.5px;
  width: 100%;
  background: var(--title);
}

.title-head {
  width: calc(100% / 3);
}
.left-head{
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: row;
}

.right-head {
  display: flex;
  align-items: center;
  justify-content: end;
  flex-direction: row;
}

.main-base-icon {
  height: 3.5vmin;
  max-height: 22.5px;;
  width: 3.5vmin;
  max-width: 22.5px;
  margin-left: 1vmin;
}
</style>
<style>
@import  "./style/font.css";
html {
  padding: 0;
  margin: 0;
  font: 1.75vmin "宋体", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-weight: 500;
  color: var(--font);
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

body {
  padding: 0;
  margin: 0;
}

.base-icon {
  height: 4vmin;
  max-height: 30px;
  width: 4vmin;
  max-width: 30px;
  margin-right: 2.5vmin;
  stroke: var(--button);
  fill: var(--button);

  &:hover {
    height: 3.5vmin;
    width: 3.5vmin;
    border: 0.25vmin dashed var(--button);
  }
  &:active{
  stroke: var(--font);

  }
}
.mid-icon {
  height: 8vmin;
  width: 8vmin;
  stroke: var(--button);
  fill: var(--button);
}
</style>