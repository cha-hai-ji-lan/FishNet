<template>
    <svg v-if="whichIcon === 'left-sleeve'" class="left-sleeve" xmlns="http://www.w3.org/2000/svg" width="512"
        height="1024" viewBox="0 0 512 1024">
        <path d="M64 128v768c0 64 0 64 64 64H384c64 0 64 0 64-64L128 128z" stroke-width="32" stroke="#ffb14a"
            stroke-linecap="round" stroke-linejoin="round" fill="#fedc45" fill-opacity="0.75" />
    </svg>
    <svg v-if="whichIcon === 'right-sleeve'" class="right-sleeve" xmlns="http://www.w3.org/2000/svg" width="512"
        height="1024" viewBox="0 0 512 1024">
        <path d="M448 128v763c0 64 0 64-64 64H128c-64 0-64 0-64-64L384 128z" stroke-width="32" stroke="#ffb14a"
            stroke-linecap="round" stroke-linejoin="round" fill="#fedc45" fill-opacity="0.75" />
    </svg>
    <svg v-if="whichIcon === 'net-body'" class="net-body" xmlns="http://www.w3.org/2000/svg" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <path
            d="M128 64h768C960 64 960 64 960 128l-128 768c-10.667297 64 0 64-64 64h-512c-64 0-53.332432.005405-64-64l-128-768c0-64 0-64 64-64"
            stroke-width="32" stroke="#ffb14a" fill="#fedc45" fill-opacity="0.75" />
    </svg>
</template>
<script setup lang="ts">
defineProps<{
    whichIcon: string
}>()
</script>
<style scoped>
.left-sleeve {
    margin-left: 10%;
    width: 40%;
    height: fit-content;
}

.right-sleeve {
    margin-right: 10%;
    width: 40%;
    height: fit-content;
}

.net-body {
    margin: 0 10%;
    width: 80%;
    height: fit-content;
}
</style>