<template>
<svg v-if="whichIcon === 'newFile'" xmlns="http://www.w3.org/2000/svg" class="mid-icon" width="1024" height="1024" viewBox="0 0 1024 1024">
	<g>
		<path d="M256 256V733.7c0 128 0 128 128 128h256c128 0 128 0 128-128V417.4c0-96 0-96-64-160l-70.624136-74.831141c-57.375864-53.168859-57.375864-53.168859-121.375864-53.168859h-128c-128 0-128 0-128 128zM567.8 139.2v128c0 64 0 64 64 64H762.6z" fill="#484b54"  stroke-width="32" stroke-linejoin="round" stroke-linecap="round" />
		<path d="M518.8 361.8v160l64 196v98.4h64v-96l64-198.4v-160l-64 160h-64zm0 160h192m-128 196h64" fill="#e85984" stroke="#e51050" stroke-width="16" stroke-linejoin="round" stroke-linecap="round" />
		<path d="M448 128v384M448 608v257M400 560h-144M496 560h272" stroke-width="16"  />
		<rect width="96" height="96" x="400" y="512" fill="none"  stroke-opacity="1" stroke-width="16" stroke-linejoin="round" />
	</g>
</svg>
</template>
<script setup lang="ts">
defineProps<{
    whichIcon: string
}>()
</script>