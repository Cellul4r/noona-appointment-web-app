<template>
  <div class="max-w-7xl mx-auto p-6">

    <!-- Header -->
    <div class="flex items-start justify-between mb-6">

      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-2xl font-semibold text-gray-900">Available Sessions</h1>
          <span v-if="hasSavedSession"
            class="flex items-center gap-1 text-green-700 text-xs font-medium bg-green-100 px-2 py-0.5 rounded-full">
            <img src="https://img.icons8.com/?size=100&id=7u2JvVUjO9ro&format=png&color=16a34a" class="w-3 h-3" />
            Saved
          </span>
        </div>
        <p class="text-sm text-gray-500 mt-1">Select sessions to build your personalized schedule.</p>
      </div>

      <!-- Control Panel -->
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

        <div class="w-px h-5 bg-gray-300" />

        <button class="flex items-center gap-1 text-sm text-gray-700 hover:text-black">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-5">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5" />
          </svg>
          Set Reminders
        </button>

      </div>
    </div>

    <!-- Grid -->
    <TransitionGroup name="session-grid" tag="div" class="grid md:grid-cols-2 xl:grid-cols-3 gap-6">

      <SessionRegistrationCard v-for="session in filteredSessions" :key="session.uuid" :session="session"
        :isSelected="isSelected(session)" :isWaitlisted="isWaitlisted(session)" :isAvailable="isAvailable(session)"
        :isAccepted="isAccepted(session)" :isLoading="loadingSessions.has(session.uuid)" :formatDate="formatDate"
        :formatTime="formatTime" @toggle-select="toggleSelect" @toggle-waitlist="toggleWaitlist"
        @toggle-accept="toggleAccept" />
    </TransitionGroup>

    <div v-if="nextCursor && filteredSessions.length > 0" class="flex justify-center mt-6">
      <button class="btn btn-outline btn-neutral" :disabled="isLoadingMore" @click="loadMore">
        {{ isLoadingMore ? "Loading..." : "Load More" }}
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue"
import { useRoute } from "vue-router"
import { getSessions } from "../services/event"
import { getEvent } from "@/services/event"
import { registerForSession, cancelSession, confirmSession } from "@/services/session"
import SessionRegistrationCard from "@/components/session/SessionRegistrationCard.vue"

const route = useRoute()
const nextCursor = ref(null)
const sessions = ref([])
const sessionsLoading = ref(false)
const filterType = ref("all")
const showSelectedOnly = ref(false)
const loadingSessions = ref(new Set())
const isFull = (session) => {
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

// ─── Actions ──────────────────────────────────────────────────────────────────

const toggleSelect = async (session) => {
  if (loadingSessions.value.has(session.uuid)) return

  const prevStatus = session.registration_status
  const isRegistered = prevStatus === "confirmed"
  const isAcceptedNow = prevStatus === "accepted"
  const event_uuid = route.params.event_uuid
  const event = await getEvent(event_uuid)
  event.max_sessions_per_user
  
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
      : await registerForSession(session.uuid)

    Object.assign(session, res)
  } catch (err) {
    const status = err.response?.status

    if (status === 400) {
      alert("You reached max session limit")
    } else if (status === 500) {
      alert("Internal error, please try again")
    } else {
      alert("Something went wrong")
    }
    session.registration_status = prevStatus
    session.seat_taken += isRemoving ? 1 : -1
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
    await confirmSession(session.uuid)
  } catch (err) {
    console.error(err)

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
  if (session.seat_taken < session.seat_capacity) return

  const prevStatus = session.registration_status
  const wasWaitlisted = prevStatus === "waitlist"
  session.registration_status = wasWaitlisted ? null : "waitlist"

  loadingSessions.value = new Set([...loadingSessions.value, session.uuid])

  try {
    const res = wasWaitlisted
      ? await cancelSession(session.uuid)
      : await registerForSession(session.uuid)

    Object.assign(session, res)
    if (!wasWaitlisted) {
      alert("Aww, this session is full 🥹 But you're now on the waitlist ⏳✨")
    } else {
      alert("You're off the waitlist now 💛 Hope to see you again!")
    }
  } catch (err) {
    console.error("toggleWaitlist failed:", err.response?.data || err.message)
    session.registration_status = prevStatus
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
    const data = await getSessions(uuid, cursor, size);

    sessions.value.push(...data.items)
    nextCursor.value = data.next_page

  } catch (err) {
    const status = err.response?.status
    if (status === 404 || status === 422) {
      router.replace({ name: 'NotFound' })
      return
    }

    error.value = 'Failed to load sessions.'
  } finally {
    sessionsLoading.value = false
  }
}

/* ---------------- PAGINATION ---------------- */

async function loadMore() {
  if (!nextCursor.value) return
  await fetchSessions(route.params.event_uuid, nextCursor.value)
  await nextTick()

  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: "smooth"
  })
}


// ─── Formatters ───────────────────────────────────────────────────────────────

const formatDate = (date) =>
  new Date(date).toLocaleDateString("en-US", { month: "short", day: "numeric" })

const formatTime = (date) =>
  new Date(date).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })

onMounted(() => {
  fetchSessions(route.params.event_uuid)
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
</style>