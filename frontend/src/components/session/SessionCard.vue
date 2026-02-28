<template>
    <div
        class="card bg-base-100 rounded-2xl p-4 border border-gray-300 hover:shadow-lg transition-all duration-300 hover:-translate-y-0.5">
        <!-- Date/Time Range -->
        <div class="mb-4">
            <!-- same day display format -->
            <div v-if="isSameDay" class="text-sm font-semibold text-base-content">
                <div class="text-base">Date: {{ dateDisplay }}</div>
                <div>Time: {{ timeDisplay }}</div>
                <div class="mt-1 text-xs font-medium w-fit px-2 py-1 rounded-full bg-base-200 text-base-content/70">
                    Duration: {{ durationDisplay }}</div>
            </div>
            <!-- else split into 2 lines -->
            <div v-else class="text-base text-base-content">
                <div>
                    <span class="font-bold">Start: </span>
                    <span class="font-medium"> {{ startDateLine }}</span>
                </div>
                <div class="mt-1">
                    <span class="font-bold">End: </span>
                    <span class="font-medium"> {{ endDateLine }}</span>
                </div>
                <div class="mt-1 text-xs font-medium w-fit px-2 py-1 rounded-full bg-base-200 text-base-content/70">
                    Duration: {{ durationDisplay }}</div>
            </div>
        </div>

        <!-- Status Badge -->
        <div class="mb-3 flex flex-wrap items-center gap-2">
            <span class="badge badge-sm" :class="statusClass">{{ statusText }}</span>
        </div>

        <div v-if="session.location" class="mb-3 text-sm text-base-content/80">
            <span class="font-semibold">Location:</span> {{ session.location }}
        </div>

        <!-- Capacity Progress -->
        <div v-if="session.seat_capacity !== null" class="w-full mb-4">
            <progress class="progress w-full h-2" :class="progressCapacityClass" :value="capacityPercent" max="100" />
        </div>

        <!-- Capacity Button -->
        <div class="flex items-center justify-between">
            <button class="btn btn-sm bg-base-300 hover:bg-gray-300  rounded-full text-sm font-medium"
                :disabled="!props.isCurrentUserHost" @click="showRegisteredUsers">
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

            <span v-if="showRegistrationStatusBadge" class="badge badge-sm ml-3" :class="registrationStatusBadgeClass">
                {{ currentUserRegistrationStatus }}
            </span>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue"
import { TZDate } from "@date-fns/tz"
import { format, formatDuration, intervalToDuration } from "date-fns"

const props = defineProps({
    session: {
        type: Object,
        required: true
    },
    isCurrentUserHost: {
        type: Boolean,
        required: false
    },
    timezone: {
        type: String,
        required: false,
        default: Intl.DateTimeFormat().resolvedOptions().timeZone || "Europe/London"
    }
})

const emit = defineEmits(['open-registered-users'])

const showRegisteredUsers = () => {
    if (!props.isCurrentUserHost) return
    const sessionUuid = props.session.uuid
    if (!sessionUuid) return
    emit('open-registered-users', sessionUuid) // emit event to parent to open the modal and pass sessionUuid value
}

/* ---------------- DATE & TIME ---------------- */

const startDate = computed(() =>
    props.session.start_datetime
        ? new TZDate(props.session.start_datetime, props.timezone)
        : null
)

const endDate = computed(() =>
    props.session.end_datetime
        ? new TZDate(props.session.end_datetime, props.timezone)
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

// only used if start and end are on the same day, format: "Mon, Feb 24, 2026 - 02:30 PM - 03:30 PM"
const dateDisplay = computed(() => {
    if (!startDate.value) return ""

    return format(startDate.value, "iii, MMM d, yyyy")
})
const timeDisplay = computed(() => {
    if (!startDate.value || !endDate.value) return ""

    const startTime = format(startDate.value, "hh:mm aa")
    const endTime = format(endDate.value, "hh:mm aa")

    return `${startTime} - ${endTime}`
})

const startDateLine = computed(() => {
    if (!startDate.value) return ""

    return format(startDate.value, "iii, MMM d, yyyy - hh:mm aa")
})

const endDateLine = computed(() => {
    if (!endDate.value) return ""

    return format(endDate.value, "iii, MMM d, yyyy - hh:mm aa")
})

const durationDisplay = computed(() => {
    if (!startDate.value || !endDate.value) return ""

    const duration = intervalToDuration({
        start: startDate.value,
        end: endDate.value
    })

    return formatDuration(duration, { format: ['years', 'months', 'days', 'hours', 'minutes'] })
})

/* ---------------- CAPACITY ---------------- */

const capacityPercent = computed(() => {
    if (!props.session.seat_capacity) return 0
    return (
        props.session.seat_taken /
        props.session.seat_capacity
    ) * 100
})

const progressCapacityClass = computed(() => {
    if (capacityPercent.value < 50) return "progress-neutral"
    if (capacityPercent.value < 80) return "progress-warning"
    return "progress-error"
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
    if (statusText.value === "Full") return "bg-red-300 text-red-800"
    if (statusText.value === "Upcoming") return "bg-sky-300 text-sky-800"
    if (statusText.value === "Ongoing") return "bg-amber-300 text-amber-800"
    return "bg-emerald-300 text-emerald-800"
})

const currentUserRegistrationStatus = computed(() => {
    const status = props.session?.registration_status
    return status
})

const showRegistrationStatusBadge = computed(() => Boolean(currentUserRegistrationStatus.value))

const registrationStatusBadgeClass = computed(() => {
    if (currentUserRegistrationStatus.value === "confirmed") return "badge-success"
    if (currentUserRegistrationStatus.value === "waitlist") return "badge-warning"
    if (currentUserRegistrationStatus.value === "available") return "badge-info"
    return "badge-neutral"
})
</script>