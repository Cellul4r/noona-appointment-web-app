<template>
  <div
    class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 flex flex-col"
    :class="isSelected ? 'ring-2 ring-indigo-400' : ''">

    <!-- Body -->
    <div class="p-5 flex flex-col gap-3 flex-1">

      <!-- Date / Time + Status Badge -->
      <div class="flex justify-between items-start">
        <div>
          <h3 class="font-semibold text-gray-800">
            <template v-if="isDifferentDate">
              {{ formatDate(session.start_datetime) }}, {{ formatTime(session.start_datetime) }} – {{ formatDate(session.end_datetime) }}, {{ formatTime(session.end_datetime) }}
            </template>
            <template v-else>
              {{ formatDate(session.start_datetime) }}<br>
              {{ formatTime(session.start_datetime) }} – {{ formatTime(session.end_datetime) }}
            </template>
          </h3>
        </div>
        <span :class="statusBadge.class" class="text-xs px-3 py-1 rounded-full font-medium">
          {{ statusBadge.label }}
        </span>
      </div>

      <!-- Location -->
      <p v-if="session.location" class="text-sm text-gray-500 flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
            clip-rule="evenodd" />
        </svg>
        {{ session.location }}
      </p>
    </div>

    <!-- Footer -->
    <div class="p-4 border-t flex justify-between items-center">

      <!-- Reserved or Seats left -->
      <span v-if="isSelected" class="text-sm text-indigo-500 font-medium flex items-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
          stroke="currentColor" class="size-5">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
        </svg>
        Reserved for you
      </span>
      <span v-else :class="isFull ? 'text-red-500' : 'text-gray-500'" class="text-sm flex items-center gap-1">
        <svg v-if="isFull" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
          stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
          stroke="currentColor" class="h-5 w-5">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
        </svg>
        {{ session.seat_capacity - session.seat_taken }} seats left
      </span>

      <!-- Action Button -->
      <!-- Loading -->
      <button v-if="buttonState === 'loading'"
        class="text-sm px-4 py-2 rounded-lg bg-gray-200 text-gray-500 cursor-not-allowed">
        ...
      </button>

      <!-- Deselect -->
      <button v-else-if="buttonState === 'deselect'" @click="$emit('toggle-select', session)"
        class="text-sm px-4 py-2 rounded-lg bg-indigo-100 text-indigo-600">
        Deselect
      </button>

      <!-- Waitlist -->
      <button v-else-if="buttonState === 'waitlist'" @click="$emit('toggle-waitlist', session)" :class="[
        'flex items-center gap-2 text-sm px-4 py-2 rounded-lg transition font-medium',
        isWaitlisted
          ? 'bg-yellow-100 text-yellow-600'
          : 'bg-yellow-200 hover:bg-yellow-400 text-yellow-900'
      ]">
        {{ isWaitlisted ? "Leave Waitlist" : "Join Waitlist" }}
      </button>

      <!-- Accept -->
      <button v-else-if="buttonState === 'accept'" @click="$emit('toggle-accept', session)"
        class="text-sm px-4 py-2 rounded-lg bg-green-500 hover:bg-green-600 text-white">
        Accept
      </button>
      <!-- Accept -->


      <!-- Default Select -->
      <button v-else @click="$emit('toggle-select', session)"
        class="text-sm px-4 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-white">
        Select
      </button>

    </div>
    
  </div>
</template>

<script setup>
import { computed } from "vue"


const props = defineProps({
  session: { type: Object, required: true },
  isSelected: { type: Boolean, default: false },
  isWaitlisted: { type: Boolean, default: false },
  isReserved: { type: Boolean, default: false },
  isAvailable: { type: Boolean, default: false },
  isAccepted: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  formatDate: { type: Function, required: true },
  formatTime: { type: Function, required: true },
})

defineEmits(["toggle-select", "toggle-waitlist", "toggle-accept"])

const isFull = computed(() =>
  props.session.seat_taken >= props.session.seat_capacity
)

const isDifferentDate = computed(() => {
  const startDate = new Date(props.session.start_datetime).toDateString()
  const endDate = new Date(props.session.end_datetime).toDateString()
  return startDate !== endDate
})

const buttonState = computed(() => {
  if (props.isLoading) return "loading"
  if (props.isSelected) return "deselect"
  if (props.isWaitlisted) return "waitlist"
  if (props.isAvailable) return "accept"
  if (isFull.value) return "waitlist"
  return "select"
})

const statusBadge = computed(() => {
  if (props.isSelected) return { label: "Registered", class: "bg-sky-100 text-sky-800" }
  if (props.isWaitlisted) return { label: "Waitlisted", class: "bg-yellow-100 text-yellow-800" }
  if (!isFull.value) return { label: "Available", class: "bg-green-50 text-green-600" }
  return { label: "Full", class: "bg-gray-100 text-gray-500" }
})
</script>