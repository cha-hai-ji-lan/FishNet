<template>
  <main class="container">
    <div data-tauri-drag-region class="main-head">
      <div data-tauri-drag-region class="title-head left-head">
        <img @click="router_to('/')" class="main-base-icon" src="./assets/icon.png" alt="">
        <a href="mailto:shi2760992374@outlook.com?subject=BUG反馈&body=请发送反馈内容">
          <div class="mar-l-2vm" @click="">
            <BaseIcon whichIcon="report-bug"></BaseIcon>
          </div>
        </a>
        <div @click="router_to('/setting')">
          <BaseIcon whichIcon="setting"></BaseIcon>
        </div>

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
    <!-- <transition-group name="path-item" tag="div"> -->
    <RouterView></RouterView>
    <!-- </transition-group> -->


    <div v-if="showPromptBox" class="warn"
      :class="{ 'nor-warn': promptLevel === '1', 'mid-warn': promptLevel === '2', 'err-warn': promptLevel === '3' }">{{
        attentionContent }} <span class="ban-select" @click="shut_down_note()">X</span></div>
  </main>
</template>
<script setup lang="ts">

import { ref, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute, RouterView } from 'vue-router';
import { invoke } from "@tauri-apps/api/core";
import { Window } from "@tauri-apps/api/window";
import { init_app, fishNetEXE, coreConfig } from "./utils/MainIndex.ts";
import { init_cad_listen_group, cleanup_event_listeners } from "./utils/event.ts";
import { cacheRouterPath, CADToolState } from "./utils/Memory.ts"
import { attentionContent, showPromptBox, promptLevel, shut_down_note } from "./utils/warn";
import BaseIcon from "./assets/icons/BaseIcon.vue";


const appWindow = Window.getCurrent()

const baseIconCtr = ref({ "maximize": "maximize-max", "pin": "pin" })  // 控制窗口最大化和钉住屏幕图标

const router = useRouter()
const route = useRoute()

onMounted(async () => {
  await init_app();
  if (coreConfig.value["bootLink"]) {
    init_cad_listen_group()
    invoke("connect_cad_cli", { acadToolPath: fishNetEXE.value, command1: ["-config-set", JSON.stringify(coreConfig.value["defaultParam"])] })
  } else{
    CADToolState.value = "__OUT_CONNECT__"
  }
})

onUnmounted(async () => {
  cleanup_event_listeners()
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

const router_to = (where: string) => {
  switch (where) {
    case '/':
      router.push("/")
      break;
    case '/setting':
      if (route.path === "/setting") {
        router.push(cacheRouterPath.value)
      } else {
        cacheRouterPath.value = route.path
        if (cacheRouterPath.value === "__NULL__") {
          router.push("/")
        } else {
          router.push("/setting")
        }
      }
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
  height: 100vh;
  /* 确保容器占满整个视口高度 *
  /* border: 0.25vmin solid #fff */
  /* filter: opacity(var(--transparency)); */
}

.main-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 5vh;
  max-height: 31.5px;
  width: 100%;
  background: rgba(var(--title), var(--transparency));
  transition: all 1.25s ease-in-out;

}

.title-head {
  width: calc(100% / 3);
}

.left-head {
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
  max-height: 22.5px;
  ;
  width: 3.5vmin;
  max-width: 22.5px;
  margin-left: 1vmin;
}

/* -------------------------------------- 警告设置 -------------------------------------- */
.warn {
  font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
  position: absolute;
  bottom: 5vmin;
  right: 2vmin;
  display: flex;
  z-index: 999;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: rgba(var(--warn-note), var(--pTransparency));
  border: 0.25vmin solid rgba(var(--warn-note), 1);
  padding: 0.75vmin 1vmin;
  border-radius: 0.5vmin;

  &.nor-warn {
    background-color: rgba(var(--normal-note), var(--pTransparency));
    border: 0.25vmin solid rgba(var(--normal-note), 1);
  }

  &.mid-warn {
    background-color: rgba(var(--warn-note), var(--pTransparency));
    border: 0.25vmin solid rgba(var(--warn-note), 1);
  }

  &.err-warn {
    background-color: rgba(var(--error-note), var(--pTransparency));
    border: 0.25vmin solid rgba(var(--error-note), 1);
  }
}
</style>
<style>
/* @import  "./style/animation.css"; */
@import "./style/font.css";
@import "./style/setting.css";

html {
  padding: 0;
  margin: 0;
  font: 1.75vmin "宋体", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-weight: 500;
  color: rgba(var(--font), 1);
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

body {
  padding: 0;
  margin: 0;
}
</style>