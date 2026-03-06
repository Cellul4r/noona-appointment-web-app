<template>
  <div class="max-w-7xl mx-auto p-6 pb-32">

    <!-- Header -->
    <div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between mb-6">

      <div>
        <div class="flex flex-wrap items-center gap-2">
          <button type="button" class="btn btn-ghost btn-sm btn-circle" aria-label="Back to event overview"
            @click="goToEventOverview">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>

          </button>
          <h1 class="text-xl sm:text-2xl font-semibold text-gray-900">Available Sessions</h1>
          <span v-if="hasSavedSession"
            class="flex items-center gap-1 text-green-700 text-xs font-medium bg-green-100 px-2 py-0.5 rounded-full">
            <img src="https://img.icons8.com/?size=100&id=7u2JvVUjO9ro&format=png&color=16a34a" class="w-3 h-3" />
            Saved
          </span>
        </div>
        <p class="text-sm text-gray-500 mt-1 sm:ml-10">Select sessions to build your personalized schedule.</p>
        <p class="text-sm text-blue-600 font-medium mt-2 sm:ml-10" v-if="maxSessionsPerUser > 0">
          Sessions Selected: <span class="font-bold">{{ selectedSessionsCount }}</span> / <span class="font-bold">{{
            maxSessionsPerUser }}</span> sessions
        </p>
      </div>

      <!-- Control Panel -->
      <div class="w-fit space-y-3">
        <!-- Row 1: Filter and Show Selected -->
        <div class="bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 flex items-center gap-4 shadow-sm">
          <div class="flex items-center gap-2 text-sm text-gray-600">
            <span>☰ Filter by:</span>
            <select v-model="filterType" class="bg-transparent outline-none font-medium text-gray-800 cursor-pointer">
              <option value="all">All Sessions</option>
              <option value="available">Available</option>
              <option value="full">Full</option>
            </select>
          </div>

          <div class="w-px h-5 bg-gray-300" />

          <div class="flex items-center gap-2 text-sm text-gray-600">
            <span>Show selected only</span>
            <input type="checkbox" class="toggle toggle-sm toggle-primary" v-model="showSelectedOnly" />
          </div>
        </div>

        <!-- Row 2: Set Reminders and Summary -->
        <div v-if="hasSavedReminderSettings" class="bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 flex items-center gap-4 shadow-sm justify-end">
          <button class="group flex items-center gap-1 text-sm text-gray-700 hover:text-indigo-600 transition-all duration-200 hover:scale-105 active:scale-95" @click="openReminderModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-5 transition-all duration-300 group-hover:animate-bell-ring">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5" />
            </svg>
            Set Reminders
          </button>

          <div class="flex items-center gap-2">
            <div class="text-xs text-blue-700 bg-blue-50 border border-blue-200 rounded-full px-3 py-1">
              {{ reminderSummaryText }}
            </div>
            <button @click="clearReminderSettings" class="text-xs text-red-600 hover:text-red-800 transition-colors" title="Clear reminders">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Set Reminders Button (when no reminders saved) -->
        <button v-else class="group bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 flex items-center justify-center gap-1 text-sm text-gray-700 hover:text-indigo-600 hover:border-indigo-300 hover:bg-indigo-50 transition-all duration-200 hover:scale-105 hover:shadow-md active:scale-95 shadow-sm" @click="openReminderModal">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-5 transition-all duration-300 group-hover:animate-bell-ring">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5" />
          </svg>
          Set Reminders
        </button>
      </div>
    </div>

    <!-- Grid -->
    <TransitionGroup name="session-grid" tag="div" class="grid grid-cols-2 xl:grid-cols-3 gap-6">

      <EventRegistrationCard v-for="session in filteredSessions" :key="session.uuid" :session="session"
        :event="event" :isSelected="isSelected(session)" :isWaitlisted="isWaitlisted(session)" :isAvailable="isAvailable(session)"
        :isAccepted="isAccepted(session)" :isLoading="loadingSessions.has(session.uuid)" :formatDate="formatDate"
        :formatTime="formatTime" @toggle-select="toggleSelect" @toggle-waitlist="toggleWaitlist"
        @toggle-accept="toggleAccept" />
    </TransitionGroup>

    <div v-if="nextCursor && filteredSessions.length > 0" class="flex justify-center mt-6">
      <button class="btn btn-outline btn-neutral" :disabled="isLoadingMore" @click="loadMore">
        {{ isLoadingMore ? "Loading..." : "Load More" }}
      </button>
    </div>

    <div
      class="fixed left-0 right-0 bottom-0 z-50 bg-gradient-to-b from-gray-50 to-gray-100 p-4 shadow-xl border-t border-gray-200">
      <div class="flex justify-end">
        <button type="button" class="btn btn-primary self-end mr-1 rounded-lg transition-all duration-200 hover:scale-105 hover:shadow-lg active:scale-95" :disabled="summaryLoading"
          @click="openConfirmModal">
          {{ summaryLoading ? "Loading..." : "Send Registration Summary" }}
        </button>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 z-[60] flex items-center justify-center">
      <!-- Backdrop with blur -->
      <div class="absolute inset-0 bg-black/20 backdrop-blur-sm" @click="cancelSendSummary"></div>
      
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4 animate-in fade-in zoom-in duration-200">
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Send Registration Summary</h3>
        <p class="text-sm text-gray-600 mb-6">
          This will send your registration summary to your email. Do you want to continue?
        </p>
        <div class="flex gap-3 justify-end">
          <button
            type="button"
            class="btn btn-ghost transition-all duration-200 hover:bg-gray-100 hover:scale-105 active:scale-95"
            @click="cancelSendSummary"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-primary transition-all duration-200 hover:scale-105 hover:shadow-lg active:scale-95"
            @click="fetchRegistrationSummary"
            :disabled="summaryLoading"
          >
            {{ summaryLoading ? "Sending..." : "Confirm" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Reminder Modal -->
    <div v-if="showReminderModal" class="fixed inset-0 z-[60] flex items-center justify-center">
      <div class="absolute inset-0 bg-black/20 backdrop-blur-sm reminder-backdrop" @click="closeReminderModal"></div>

      <div class="relative bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4 animate-in fade-in zoom-in duration-200 reminder-modal-pop">
        <h3 class="text-lg font-semibold text-gray-900 mb-1">Set Reminders</h3>
        <p class="text-sm text-gray-600 mb-5">Choose reminder times before the session starts. First alert is required.</p>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">First Alert <span class="text-red-500">*</span></label>
            <select v-model.number="firstAlertMinutes" class="select select-bordered w-full transition-all duration-200 focus:scale-[1.01]">
              <option :value="-1">None</option>
              <option :value="0">When event starts</option>
              <option v-for="minute in reminderOptions" :key="`first-${minute}`" :value="minute">
                {{ formatReminderOption(minute) }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1 flex items-center justify-between">
              <span>Second Alert (Optional)</span>
              <span v-if="firstAlertMinutes === -1" class="text-xs text-gray-500">Select first alert first</span>
            </label>
            <select v-model.number="secondAlertMinutes" :disabled="firstAlertMinutes === -1" class="select select-bordered w-full transition-all duration-200 focus:scale-[1.01] disabled:opacity-50 disabled:cursor-not-allowed">
              <option :value="-1">None</option>
              <option :value="0">When event starts</option>
              <option v-for="minute in reminderOptions" :key="`second-${minute}`" :value="minute" :disabled="minute <= firstAlertMinutes">
                {{ formatReminderOption(minute) }}
              </option>
            </select>
          </div>
        </div>

        <div class="flex gap-3 justify-between mt-6">
          <button v-if="hasSavedReminderSettings" type="button" class="btn btn-error btn-outline transition-all duration-200 hover:scale-105 active:scale-95" @click="clearReminderSettings">
            Clear
          </button>
          <div class="flex gap-3 ml-auto">
            <button type="button" class="btn btn-ghost transition-all duration-200 hover:bg-gray-100 hover:scale-105 active:scale-95" @click="closeReminderModal">Cancel</button>
            <button type="button" class="btn btn-primary transition-all duration-200 hover:scale-105 hover:shadow-lg active:scale-95" @click="saveReminderSettings">Save</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getSessions } from "../services/event"
import { getEvent, getEventRegistrationSummary } from "@/services/event"
import { registerForSession, cancelSession, confirmSession } from "@/services/session"
import EventRegistrationCard from "@/components/session/EventRegistrationCard.vue"
import { TZDate } from "@date-fns/tz"
import { format } from "date-fns"
import { useAuthStore } from "@/store/authStore"

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const nextCursor = ref(null)
const sessions = ref([])
const event = ref(null)
const sessionsLoading = ref(false)
const filterType = ref("all")
const showSelectedOnly = ref(false)
const loadingSessions = ref(new Set())
const error = ref(null)
const isLoadingMore = ref(false)
const maxSessionsPerUser = ref(0)
const summaryLoading = ref(false)
const showConfirmModal = ref(false)
const showReminderModal = ref(false)
const firstAlertMinutes = ref(15)
const secondAlertMinutes = ref(0)
const hasSavedReminderSettings = ref(false)
const reminderOptions = [5, 10, 15, 30, 60, 120, 1440, 2880, 10080]
// const reminderOptionsWithStart = [0, ...reminderOptions]
const selectedSessionsCount = computed(() =>
  sessions.value.filter(s => s.registration_status === "confirmed").length
)
const isFull = (session) => {
  if (session.seat_capacity == null) return false
  const isMine = session.registration_status === "confirmed"
  const takenByOthers = session.seat_taken - (isMine ? 1 : 0)
  return takenByOthers >= session.seat_capacity
}
// ─── Helpers ──────────────────────────────────────────────────────────────────

const isSelected = (session) => session.registration_status === "confirmed"
const isAvailable = (session) => session.registration_status === "available"
const isWaitlisted = (session) => session.registration_status === "waitlist"
const isAccepted = (session) => session.registration_status === "accepted"

const hasSavedSession = computed(() =>
  sessions.value.some((s) => s.registration_status === "confirmed")
)

const formatReminderOption = (minute) => {
  if (minute === -1) return "None"
  if (minute === 0) return "When event starts"

  const days = Math.floor(minute / 1440)
  const hours = Math.floor((minute % 1440) / 60)
  const minutes = minute % 60

  if (days > 0 && hours > 0) return `${days} day${days > 1 ? "s" : ""} ${hours} hour${hours > 1 ? "s" : ""} before`
  if (days > 0) return `${days} day${days > 1 ? "s" : ""} before`
  if (hours > 0 && minutes > 0) return `${hours} hour${hours > 1 ? "s" : ""} ${minutes} minute${minutes > 1 ? "s" : ""} before`
  if (hours > 0) return `${hours} hour${hours > 1 ? "s" : ""} before`
  return `${minutes} minute${minutes > 1 ? "s" : ""} before`
}

const reminderSummaryText = computed(() => {
  const firstText = formatReminderOption(firstAlertMinutes.value)
  const secondText = secondAlertMinutes.value >= 0 ? formatReminderOption(secondAlertMinutes.value) : "None"
  return `First: ${firstText} | Second: ${secondText}`
})

const filteredSessions = computed(() => {
  let list = sessions.value

  if (filterType.value === "available") {
    list = list.filter((s) => !isFull(s))
  } else if (filterType.value === "full") {
    list = list.filter((s) => isFull(s))
  }

  if (showSelectedOnly.value) {
    list = list.filter((s) => s.registration_status === "confirmed")
  }

  return list
})

const goToEventOverview = () => {
  router.push({
    name: "EventOverview",
    params: { event_uuid: route.params.event_uuid }
  })
}

const openConfirmModal = () => {
  if (selectedSessionsCount.value === 0) {
    alert("Please select at least one session before sending registration summary")
    return
  }
  showConfirmModal.value = true
}

const fetchRegistrationSummary = async () => {
  showConfirmModal.value = false
  summaryLoading.value = true
  try {
    await getEventRegistrationSummary(route.params.event_uuid)
    alert("Registration summary has been sent to your email!")
  } catch (err) {
    console.error("Failed to send registration summary:", err)
    alert(err.response?.data?.detail || "Failed to send registration summary")
  } finally {
    summaryLoading.value = false
  }
}

const cancelSendSummary = () => {
  showConfirmModal.value = false
}

const openReminderModal = () => {
  showReminderModal.value = true
}

const closeReminderModal = () => {
  showReminderModal.value = false
}

const getReminderPayload = () => {
  if (!hasSavedReminderSettings.value || firstAlertMinutes.value === -1) return []
  return [firstAlertMinutes.value, secondAlertMinutes.value]
}

const saveReminderSettings = () => {
  if (firstAlertMinutes.value === -1) {
    alert("Please select at least the first alert")
    return
  }
  if (secondAlertMinutes.value && secondAlertMinutes.value >= 0 && secondAlertMinutes.value <= firstAlertMinutes.value) {
    alert("Second Alert must be greater than First Alert")
    return
  }
  const eventUuid = route.params.event_uuid
  const reminderSettings = {
    eventUuid,
    firstAlertMinutes: firstAlertMinutes.value,
    secondAlertMinutes: secondAlertMinutes.value
  }
  localStorage.setItem(`reminder_settings_${eventUuid}`, JSON.stringify(reminderSettings))
  hasSavedReminderSettings.value = true
  closeReminderModal()
  alert("Reminder settings saved")
}

const clearReminderSettings = () => {
  const eventUuid = route.params.event_uuid
  localStorage.removeItem(`reminder_settings_${eventUuid}`)
  firstAlertMinutes.value = -1
  secondAlertMinutes.value = -1
  hasSavedReminderSettings.value = false
  closeReminderModal()
  alert("Reminder settings cleared")
}

// Watch for first alert changes to reset second alert when None is selected
watch(firstAlertMinutes, (newValue) => {
  if (newValue === -1) {
    secondAlertMinutes.value = -1
  }
})

const loadReminderSettings = () => {
  const eventUuid = route.params.event_uuid
  try {
    const stored = localStorage.getItem(`reminder_settings_${eventUuid}`)
    if (stored) {
      const reminderSettings = JSON.parse(stored)
      firstAlertMinutes.value = reminderSettings.firstAlertMinutes || 15
      secondAlertMinutes.value = reminderSettings.secondAlertMinutes || 0
      hasSavedReminderSettings.value = true
    } else {
      hasSavedReminderSettings.value = false
    }
  } catch (err) {
    console.error("Failed to load reminder settings:", err)
    hasSavedReminderSettings.value = false
  }
}

// ─── Actions ──────────────────────────────────────────────────────────────────

const toggleSelect = async (session) => {
  if (loadingSessions.value.has(session.uuid)) return

  const prevStatus = session.registration_status
  const isRegistered = prevStatus === "confirmed"
  const isAcceptedNow = prevStatus === "accepted"
  const event_uuid = route.params.event_uuid
  if (!maxSessionsPerUser.value) {
    const event = await getEvent(event_uuid)
    maxSessionsPerUser.value = event.max_sessions_per_user || 0
  }

  //ถ้าเป็น accepted → ใช้ cancel เหมือนกัน
  const isRemoving = isRegistered || isAcceptedNow

  if (!isRemoving && isFull(session)) return

  // optimistic
  session.registration_status = isRemoving ? null : "confirmed"
  session.seat_taken += isRemoving ? -1 : 1


  loadingSessions.value = new Set([...loadingSessions.value, session.uuid])

  try {
    const res = isRemoving
      ? await cancelSession(session.uuid)
      : await registerForSession(session.uuid, getReminderPayload())

    Object.assign(session, res)
  } catch (err) {
    const status = err.response?.status
    const errorMsg = err.response?.data?.detail || err.response?.data?.message

    if (status === 400) {
      error.value = errorMsg || "You reached max session limit"
      alert(errorMsg || "You reached max session limit")
    } else if (status === 404) {
      error.value = "Session not found"
      if (confirm("This session no longer exists. Do you want to refresh the page?")) {
        router.go(0)
      }
    } else if (status === 409) {
      error.value = "Session state conflict. Please refresh."
      alert("Session state has changed. Please refresh the page.")
    } else if (status === 500) {
      error.value = "Server error occurred"
      alert("Internal error, please try again")
    } else {
      error.value = err.message || "Something went wrong"
      alert("Something went wrong")
    }
    session.registration_status = prevStatus
    session.seat_taken += isRemoving ? 1 : -1
    console.error('Toggle select error:', { status, errorMsg, err })
  } finally {
    const next = new Set(loadingSessions.value)
    next.delete(session.uuid)
    loadingSessions.value = next
  }
}

const toggleAccept = async (session) => {
  if (loadingSessions.value.has(session.uuid)) return
  const target = sessions.value.find(s => s.id === session.id)
  if (!target) return

  target.isAccepted = !target.isAccepted

  const prevStatus = session.registration_status
  // ต้องเป็น available เท่านั้น
  if (prevStatus !== "available") return
  // Optimistic update
  session.registration_status = "confirmed"
  session.seat_taken += 1

  loadingSessions.value = new Set([...loadingSessions.value, session.uuid])

  try {
    await confirmSession(session.uuid, getReminderPayload())
  } catch (err) {
    console.error(err)
    const status = err.response?.status
    const errorMsg = err.response?.data?.detail || err.response?.data?.message

    if (status === 400) {
      error.value = errorMsg || "You reached max session limit"
      alert(errorMsg || "You reached max session limit")
    } else if (status === 404) {
      error.value = "Session not found"
      if (confirm("This session no longer exists. Do you want to refresh the page?")) {
        router.go(0)
      }
    } else if (status === 409) {
      error.value = "Session state conflict. Please refresh."
      alert("Session state has changed. Please refresh the page.")
    } else if (status === 500) {
      error.value = "Server error occurred"
      alert("Internal error, please try again")
    } else {
      error.value = err.message || "Something went wrong"
      alert("Something went wrong")
    }
    // rollback
    session.registration_status = prevStatus
    session.seat_taken -= 1
  } finally {
    const next = new Set(loadingSessions.value)
    next.delete(session.uuid)
    loadingSessions.value = next
  }
}

const toggleWaitlist = async (session) => {
  if (loadingSessions.value.has(session.uuid)) return
  if (session.seat_capacity == null || session.seat_taken < session.seat_capacity) return

  const prevStatus = session.registration_status
  const wasWaitlisted = prevStatus === "waitlist"
  session.registration_status = wasWaitlisted ? null : "waitlist"

  loadingSessions.value = new Set([...loadingSessions.value, session.uuid])

  try {
    const res = wasWaitlisted
      ? await cancelSession(session.uuid)
      : await registerForSession(session.uuid, getReminderPayload())

    Object.assign(session, res)
    if (!wasWaitlisted) {
      alert("Aww, this session is full 🥹 But you're now on the waitlist ⏳✨")
    } else {
      alert("You're off the waitlist now 💛 Hope to see you again!")
    }
  } catch (err) {
    const status = err.response?.status
    const errorMsg = err.response?.data?.detail || err.response?.data?.message

    if (status === 404) {
      error.value = "Session not found"
      alert("This session no longer exists")
    } else if (status === 500) {
      error.value = "Server error occurred"
      alert("Internal error, please try again")
    } else {
      error.value = err.message || "Something went wrong"
      alert("Something went wrong")
    }
    session.registration_status = prevStatus
    console.error('Toggle waitlist error:', { status, errorMsg, err })
  } finally {
    const next = new Set(loadingSessions.value)
    next.delete(session.uuid)
    loadingSessions.value = next
  }
}

// ─── Fetch ────────────────────────────────────────────────────────────────────

async function fetchSessions(uuid, cursor = null, size = 15) {
  sessionsLoading.value = true
  try {
    if (!cursor) {
      sessions.value = []
      nextCursor.value = null
    }
    const data = await getSessions(uuid, cursor, size, true);

    sessions.value.push(...data.items)
    nextCursor.value = data.next_page

  } catch (err) {
    const status = err.response?.status
    if (status === 404 || status === 422) {
      error.value = 'Event not found'
      console.error("Event not found:", err)
      setTimeout(() => {
        router.replace({ name: 'NotFound' })
      }, 1000)
      return
    }

    error.value = err.response?.data?.message || 'Failed to load sessions.'
    console.error('Session fetch error:', err.response?.data || err.message)
  } finally {
    sessionsLoading.value = false
  }
}

/* ---------------- PAGINATION ---------------- */

async function loadMore() {
  if (!nextCursor.value) return
  isLoadingMore.value = true
  try {
    await fetchSessions(route.params.event_uuid, nextCursor.value)
    await nextTick()

    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth"
    })
  } catch (err) {
    console.error("Load more failed:", err)
    error.value = "Failed to load more sessions"
  } finally {
    isLoadingMore.value = false
  }
}


// ─── Timezone Configuration ───────────────────────────────────────────────────

const timezoneLabel = computed(() =>
  authStore.user?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone
)

const eventTimezone = computed(() => timezoneLabel.value)

// ─── Formatters ───────────────────────────────────────────────────────────────

const formatTime = (date) => {
  return format(new TZDate(date, eventTimezone.value), "HH:mm")
}

const formatDate = (date) => {
  return format(new TZDate(date, eventTimezone.value), "MMM d")
}

const minStartDateTime = computed(() => {
  const now = new Date()
  const tzDate = new TZDate(now, eventTimezone.value)
  const pad = (n) => String(n).padStart(2, "0")
  return `${tzDate.getFullYear()}-${pad(tzDate.getMonth() + 1)}-${pad(tzDate.getDate())}T${pad(tzDate.getHours())}:${pad(tzDate.getMinutes())}`
})

onMounted(async () => {
  const event_uuid = route.params.event_uuid
  try {
    const eventData = await getEvent(event_uuid)
    event.value = eventData
    maxSessionsPerUser.value = eventData.max_sessions_per_user || 0
  } catch (err) {
    console.error("Failed to fetch event details:", err)
  }
  fetchSessions(event_uuid)
  loadReminderSettings()
})
</script>
''
<style>
.session-grid-enter-active,
.session-grid-leave-active {
  transition: all 0.5s ease;
}

.session-grid-enter-from,
.session-grid-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.reminder-backdrop {
  animation: reminderBackdropFade 0.18s ease-out;
}

.reminder-modal-pop {
  animation: reminderModalPop 0.22s ease-out;
}

@keyframes reminderBackdropFade {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes reminderModalPop {
  from {
    opacity: 0;
    transform: translateY(6px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes bell-ring {
  0% { transform: rotate(0deg); }
  10% { transform: rotate(15deg); }
  20% { transform: rotate(-12deg); }
  30% { transform: rotate(15deg); }
  40% { transform: rotate(-12deg); }
  50% { transform: rotate(10deg); }
  60% { transform: rotate(-8deg); }
  70% { transform: rotate(6deg); }
  80% { transform: rotate(-4deg); }
  90% { transform: rotate(2deg); }
  100% { transform: rotate(0deg); }
}

.animate-bell-ring {
  animation: bell-ring 0.8s ease-in-out;
}
</style>