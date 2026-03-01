<template>
    <!-- <svg  class="mid-icon" xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
        <g>
            <path d="M256 128l0 768L768 896 768 320 576 128zM576 128V320h192" fill="none" stroke-width="64" stroke-linejoin="round"
                stroke-linecap="round" />
            <path d="M512 384v160l64 196v96h64v-96L704 544v-160l-64 160h-64zM512 544h192M576 740h64" fill="#e85984"
                stroke="#e51050" stroke-width="32" stroke-linejoin="round" stroke-linecap="round" />
            <path d="M448 128v384M448 608v256M400 560h-144M496 560h272" stroke-width="32" />
            <rect fill="none" width="96" height="96" x="400" y="512" stroke-opacity="1" stroke-width="32" stroke-linejoin="round" />
        </g>
</svg> -->
<svg v-if="whichIcon === 'newFile'" class="mid-icon" xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
	<g>
		<path d="M256 256v512c0 128 0 128 128 128h256c128 0 128 0 128-128v-352c0-96 0-96-64-160l-70.624136-74.831141c-57.375864-53.168859-57.375864-53.168859-121.375864-53.168859h-128c-128 0-128 0-128 128zm320-120v128c0 64 0 64 64 64H750z" fill="#303645"  stroke-width="32" stroke-linejoin="round" stroke-linecap="round" />
		<path d="M512 384v160l64 196v96h64v-96L704 544v-160l-64 160h-64zM512 544h192M576 740h64" fill="#e85984" stroke="#e51050" stroke-width="16" stroke-linejoin="round" stroke-linecap="round" />
		<path d="M448 128v384M448 608v288M400 560h-144M496 560h272" stroke-width="16"  />
		<rect width="96" height="96" x="400" y="512" fill="none"  stroke-opacity="1" stroke-width="16" stroke-linejoin="round" />
	</g>
</svg>
</template>
<script setup lang="ts">
defineProps<{
    whichIcon: string
}>()
</script>