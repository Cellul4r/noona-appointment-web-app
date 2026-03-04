<script setup>
import { ref, onMounted } from "vue"
import { computed } from "vue"
import { useRoute } from "vue-router"
import { registerSessions } from "@/services/event"

const route = useRoute()
const filterType = ref("all")
const sessions = ref([])
const loading = ref(false)
const selectedSessions = ref([])
const showSelectedOnly = ref(false)

const toggleSelect = async (session) => {
  if (session.seat_taken >= session.seat_capacity) return

  const index = selectedSessions.value.findIndex(s => s.uuid === session.uuid)

  if (index !== -1) {
    // ❌ remove
    selectedSessions.value.splice(index, 1)
  } else {
    // ✅ add
    selectedSessions.value.push(session)
  }

  // 🔥 CALL API SAVE ทันที
  try {
    const event_uuid = route.params.event_uuid

    await registerSessions(event_uuid, {
      session_uuids: selectedSessions.value.map(s => s.uuid)
    })

    console.log("Saved success")
  } catch (err) {
    console.error("Save failed", err)
  }
}
const filteredSessions = computed(() => {
  let list = sessions.value

  // filter type
  if (filterType.value === "available") {
    list = list.filter(s => s.seat_taken < s.seat_capacity)
  } else if (filterType.value === "full") {
    list = list.filter(s => s.seat_taken >= s.seat_capacity)
  }

  // filter selected only
  if (showSelectedOnly.value) {
    list = list.filter(s =>
      selectedSessions.value.some(sel => sel.uuid === s.uuid)
    )
  }

  return list
})
/* MOCK */
const mockSessions = [
  {
    uuid: "mock-1",
    start_datetime: "2026-03-10T09:00:00Z",
    end_datetime: "2026-03-10T10:30:00Z",
    location: "Room 304",
    seat_capacity: 40,
    seat_taken: 10,
    event: {
      title: "Intro to Chemistry",
      description: "Basic chemistry fundamentals"
    }
  },
  {
    uuid: "mock-2",
    start_datetime: "2026-03-10T11:00:00Z",
    end_datetime: "2026-03-10T12:30:00Z",
    location: "Lab 2",
    seat_capacity: 30,
    seat_taken: 30,
    event: {
      title: "Advanced Physics",
      description: "Quantum mechanics intro"
    }
  },
  {
    uuid: "mock-3",
    start_datetime: "2026-03-11T13:00:00Z",
    end_datetime: "2026-03-11T15:00:00Z",
    location: "Computer Lab",
    seat_capacity: 50,
    seat_taken: 20,
    event: {
      title: "Intro to Algorithms",
      description: "Sorting & searching"
    }
  }
]

const fetchSessions = async () => {
  const event_uuid = route.params.event_uuid

  if (!event_uuid) {
    sessions.value = mockSessions
    return
  }

  try {
    loading.value = true
    const data = await registerSessions(event_uuid, {
      upcoming_only: true,
      size: 20
    })

    if (Array.isArray(data)) {
      sessions.value = data
    } else if (Array.isArray(data.data)) {
      sessions.value = data.data
    } else if (Array.isArray(data.data?.sessions)) {
      sessions.value = data.data.sessions
    } else {
      sessions.value = mockSessions
    }
  } catch (err) {
    sessions.value = mockSessions
  } finally {
    loading.value = false
  }
}

const isSelected = (session) => {
  return selectedSessions.value.some(s => s.uuid === session.uuid)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric"
  })
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit"
  })
}

onMounted(fetchSessions)
</script>

<template>
  <div class="max-w-7xl mx-auto p-6">

    <div class="flex items-start justify-between mb-6">

      <!-- LEFT -->
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-2xl font-semibold text-gray-900">
            Available Sessions
          </h1>

          <span v-if="selectedSessions.length"
            class="flex items-center gap-1 text-green-700 text-xs font-medium bg-green-100 px-2 py-0.5 rounded-full">
            <img src="https://img.icons8.com/?size=100&id=7u2JvVUjO9ro&format=png&color=16a34a" class="w-3 h-3" />
            Saved
          </span>
        </div>

        <p class="text-sm text-gray-500 mt-1">
          Select sessions to build your personalized schedule.
        </p>
      </div>

      <!-- RIGHT CONTROL PANEL -->
      <div class="bg-gray-50 border border-gray-200 rounded-xl px-4 py-2 flex items-center gap-4 shadow-sm">

        <!-- Filter -->
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <span class="flex items-center gap-1">
            ☰ Filter by:
          </span>

          <select v-model="filterType" class="bg-transparent outline-none font-medium text-gray-800 cursor-pointer">
            <option value="all">All Sessions</option>
            <option value="available">Available</option>
            <option value="full">Full</option>
          </select>
        </div>

        <!-- Divider -->
        <div class="w-px h-5 bg-gray-300"></div>

        <!-- Toggle -->
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <span>Show selected only</span>
          <input type="checkbox" class="toggle toggle-sm toggle-primary" v-model="showSelectedOnly" />
        </div>

        <!-- Divider -->
        <div class="w-px h-5 bg-gray-300"></div>

        <!-- Button -->
        <button class="flex items-center gap-1 text-sm text-gray-700 hover:text-black">
          🔔 Set Reminders
        </button>

      </div>

    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-10">
      Loading...
    </div>

    <!-- Grid -->
    <div v-else class="grid md:grid-cols-2 xl:grid-cols-3 gap-6">

      <div v-for="session in filteredSessions" :key="session.uuid"
        class="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 flex flex-col"
        :class="isSelected(session) ? 'ring-2 ring-indigo-400' : ''">
        <!-- Content -->
        <div class="p-5 flex flex-col gap-3 flex-1">

          <!-- Date + Status -->
          <div class="flex justify-between items-start">
            <div>
              <span class="text-xs text-indigo-500 font-semibold">
                {{ formatDate(session.start_datetime) }}
              </span>

              <h3 class="font-semibold text-gray-800">
                {{ formatTime(session.start_datetime) }} -
                {{ formatTime(session.end_datetime) }}
              </h3>
            </div>

            <span v-if="session.seat_taken < session.seat_capacity"
              class="bg-green-50 text-green-600 text-xs px-3 py-1 rounded-full font-medium">
              Available
            </span>

            <span v-else class="bg-gray-100 text-gray-500 text-xs px-3 py-1 rounded-full font-medium">
              Full
            </span>
          </div>

          <!-- Title -->
          <h4 class="font-semibold text-lg text-gray-900">
            {{ session.event?.title }}
          </h4>

          <!-- Location -->
          <p class="text-sm text-gray-500">
            📍 {{ session.location }}
          </p>

          <!-- Description -->
          <p class="text-sm text-gray-400">
            {{ session.event?.description }}
          </p>

          <!-- Selected label -->
          <p class="text-xs text-indigo-500 font-medium min-h-[16px]">
            <span v-if="isSelected(session)">
              ✔ Reserved for you
            </span>
          </p>
        </div>

        <!-- Footer -->
        <div class="p-4 border-t flex justify-between items-center">

          <span class="text-xs text-gray-500">
            👥 {{ session.seat_capacity - session.seat_taken }} seats left
          </span>

          <button v-if="session.seat_taken < session.seat_capacity" @click="toggleSelect(session)" :class="[
            'text-sm px-4 py-2 rounded-lg transition',
            isSelected(session)
              ? 'bg-indigo-100 text-indigo-600'
              : 'bg-indigo-500 hover:bg-indigo-600 text-white'
          ]">
            {{ isSelected(session) ? "Selected" : "Select" }}
          </button>

          <button v-else class="bg-gray-200 text-gray-500 text-sm px-4 py-2 rounded-lg" disabled>
            Full
          </button>

        </div>

      </div>

    </div>

  </div>
</template>