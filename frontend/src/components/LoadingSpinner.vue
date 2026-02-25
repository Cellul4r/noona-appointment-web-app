<template>
    <div :class="[
        'flex items-center justify-center',
        fullPage ? 'fixed inset-0 bg-base-200/70 z-50' : 'py-10'
    ]">
        <div class="flex flex-col items-center gap-4">

            <!-- Animated Spinner -->
            <span class="loading loading-spinner loading-lg text-primary"></span>

            <!-- Optional text -->
            <p v-if="text" class="text-sm opacity-70 animate-pulse">
                {{ text }}
            </p>

        </div>
    </div>
</template>

<script setup>
defineProps({
    text: {
        type: String,
        default: ''
    },
    fullPage: {
        type: Boolean,
        default: false
    }
})
</script>