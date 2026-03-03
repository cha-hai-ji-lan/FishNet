<template>
    <svg v-if="whichIcon === 'left-sleeve'" class="left-sleeve" xmlns="http://www.w3.org/2000/svg" width="512" height="1024"
        viewBox="0 0 512 1024">
        <path d="M64 128v768c0 64 0 64 64 64H384c64 0 64 0 64-64L128 128z" stroke-width="32" stroke="#ffb14a"
            stroke-linecap="round" stroke-linejoin="round" fill="#fedc45" fill-opacity="0.75" />
    </svg>
    <svg  v-if="whichIcon === 'right-sleeve'" xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024">
	<path d="M448 128v763c0 64 0 64-64 64H128c-64 0-64 0-64-64L384 128z" stroke-width="32" stroke="#ffb14a" stroke-linecap="round" stroke-linejoin="round" fill="#fedc45" fill-opacity="0.75" />
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
    height: 100%;
}
.right-sleeve {
    margin-right: 10%;
    width: 40%;
    height: 100%;
}
</style>