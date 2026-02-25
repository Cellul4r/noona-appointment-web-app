<template>
    <div class="card bg-base-100 rounded-2xl p-4 border hover:shadow-xl transition-all duration-300">
        <!-- Date/Time Range -->
        <div class="mb-3">
            <div v-if="isSameDay" class="text-base font-semibold">
                <div>{{ sameDayDisplay }}</div>
                <div class="text-sm font-normal">{{ durationDisplay }}</div>
            </div>
            <div v-else class="text-base font-semibold">
                <div>{{ startDateLine }}</div>
                <div class="text-base font-normal">→ {{ endDateLine }}</div>
                <div class="text-sm font-normal">{{ durationDisplay }}</div>
            </div>
        </div>

        <!-- Status Badge -->
        <div class="mb-2">
            <span class="badge" :class="statusClass">{{ statusText }}</span>
        </div>

        <!-- Capacity Progress -->
        <div v-if="session.seat_capacity !== null" class="w-full mb-3">
            <progress class="progress progress-primary w-full h-2" :value="capacityPercent" max="100" />
        </div>

        <!-- Capacity Button -->
        <div class="flex justify-between justify-content-center">
            <button class="btn btn-soft rounded-full text-sm font-medium" :class="capacityButtonClass">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-4">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                </svg>
                <div v-if="session.seat_capacity !== null">
                    {{ session.seat_taken }} / {{ session.seat_capacity }}
                </div>
                <div v-else>
                    {{ session.seat_taken }}
                </div>
            </button>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
    session: {
        type: Object,
        required: true
    }
})

/* ---------------- DATE & TIME ---------------- */

const startDate = computed(() =>
    props.session.start_datetime
        ? new Date(props.session.start_datetime)
        : null
)

const endDate = computed(() =>
    props.session.end_datetime
        ? new Date(props.session.end_datetime)
        : null
)

const isSameDay = computed(() => {
    if (!startDate.value || !endDate.value) return true

    return (
        startDate.value.getFullYear() === endDate.value.getFullYear() &&
        startDate.value.getMonth() === endDate.value.getMonth() &&
        startDate.value.getDate() === endDate.value.getDate()
    )
})

const sameDayDisplay = computed(() => {
    if (!startDate.value || !endDate.value) return ""

    // Same day: "Mon, Feb 24, 2026 · 02:30 PM - 03:30 PM"
    const date = startDate.value.toLocaleDateString(undefined, {
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric"
    })
    const startTime = startDate.value.toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit"
    })
    const endTime = endDate.value.toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit"
    })
    return `${date} · ${startTime} - ${endTime}`
})

const startDateLine = computed(() => {
    if (!startDate.value) return ""

    return startDate.value.toLocaleDateString(undefined, {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    })
})

const endDateLine = computed(() => {
    if (!endDate.value) return ""

    return endDate.value.toLocaleDateString(undefined, {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    })
})

const durationDisplay = computed(() => {
    if (!startDate.value || !endDate.value) return ""

    const diffMs = endDate.value - startDate.value
    const diffMins = Math.floor(diffMs / 60000)
    const hours = Math.floor(diffMins / 60)
    const minutes = diffMins % 60

    if (hours === 0) return `${minutes} min`
    if (minutes === 0) return `${hours}h`
    return `${hours}h ${minutes}m`
})

/* ---------------- CAPACITY ---------------- */

const capacityPercent = computed(() => {
    if (!props.session.seat_capacity) return 0
    return (
        props.session.seat_taken /
        props.session.seat_capacity
    ) * 100
})

const capacityButtonClass = computed(() => {
    if (capacityPercent.value >= 100) return "btn-error"
    if (capacityPercent.value > 75) return "btn-warning"
    return "btn-neutral"
})

/* ---------------- STATUS ---------------- */

const statusText = computed(() => {
    const now = new Date()

    if (!startDate.value || !endDate.value) return ""

    if (capacityPercent.value >= 100) return "Full"
    if (now < startDate.value) return "Upcoming"
    if (now >= startDate.value && now <= endDate.value)
        return "Ongoing"

    return "Finished"
})

const statusClass = computed(() => {
    if (statusText.value === "Full") return "badge-error"
    if (statusText.value === "Upcoming") return "badge-info"
    if (statusText.value === "Ongoing") return "badge-success"
    return "badge-ghost"
})
</script>