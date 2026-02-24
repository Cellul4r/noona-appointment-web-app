<template>
  <div class="min-h-screen bg-base-200">
    <nav class="sticky top-0 z-50 bg-white shadow px-6">
      <div class="flex justify-between items-center h-16">
          <router-link to="/events" class="flex items-center gap-2 text-xl hover:opacity-80">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>

            <span class="text-xl font-bold">Create New Event</span>
          </router-link>
          <div class="dropdown dropdown-end">
  
            <!-- Avatar (ปุ่มกด) -->
            <div tabindex="0" role="button" class="avatar avatar-online cursor-pointer">
                <div class="bg-neutral text-neutral-content w-10 rounded-full">
                <!-- <span class="text-xl">AI</span> -->
                </div>
            </div>

            <!-- Dropdown menu -->
            <ul
            tabindex="0"
            class="dropdown-content menu bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
            >
            <li>
                <router-link to="/setting" @click="$event.currentTarget.blur()">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
                Settings
                </router-link>
            </li>
            <li>
                <router-link to="/login" class="text-error" @click="$event.currentTarget.blur()">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                </svg>

                Logout
                </router-link>
            </li>
            </ul>

        </div>
      </div>
    </nav>

    <div class="max-w-4xl mx-auto p-6 space-y-6">
      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
            </svg>
            Event Details
          </h2>

          <div class="grid md:grid-cols-2 gap-4">

            <div class="md:col-span-2">
              <span>Event Title</span>
              <span class="text-red-500"> *</span>
              <input v-model="event.title" type="text" class="input input-bordered w-full" />
            </div>

            <div class="md:col-span-2">
              <span>Location</span>
              <span class="opacity-60"> (optional)</span>
              <input v-model="event.location" type="text" class="input input-bordered w-full" />
            </div>

            <div class="md:col-span-2">
              <span>Description</span>
              <span class="opacity-60"> (optional)</span>
              <textarea v-model="event.description" class="textarea textarea-bordered w-full"></textarea>
            </div>

          </div>
        </div>
      </div>

      <!-- Session -->
      <div class="card bg-base-100 shadow">
        <div class="card-body space-y-4">

          <div class="flex justify-between items-center">
            <h2 class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              Session Management
            </h2>

            <div class="flex items-center gap-2">
              <span>Limit sessions per participant</span>
              <span class="opacity-60"> (optional)</span>
              <input
                type="checkbox"
                v-model="limitEnabled"
                class="toggle toggle-primary"
              />
              
              <input
                type="number"
                v-model="limit"
                :disabled="!limitEnabled"
                @input="limit = Math.max(1, Number(limit))"
                class="input input-bordered w-20 disabled:opacity-50"
              />
            </div>
          </div>

          <!-- Add session -->
          <div class="border border-dashed p-4 rounded-xl space-y-3">
            <h2 class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>

              Add New Session
            </h2>

           <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

              <!-- Start -->
              <input
                type="datetime-local"
                v-model="newSession.start"
                class="input input-bordered w-full"
              />

              <!-- End -->
              <input
                type="datetime-local"
                v-model="newSession.end"
                class="input input-bordered w-full"
              />

              <!-- Capacity -->
              <input
                type="number"
                v-model="newSession.capacity"
                placeholder="Seats"
                min="1"
                @input="newSession.capacity = $event.target.value === ''
                  ? null
                  : Math.max(1, Number($event.target.value))"
                class="input input-bordered w-full"
              />

              <!-- Location -->
              <input
                type="text"
                v-model="newSession.location"
                placeholder="Room 101"
                class="input input-bordered w-full"
              />

            </div>
            <input type="text" v-model="newSession.desc" placeholder="Description (optional)" class="input input-bordered w-full"/>
            <div class="card bg-base-100 shadow p-4 space-y-4">
              <h2 class="card-title flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>

                Recurrence
              </h2>

              <!-- content -->
              <div class="grid md:grid-cols-3 gap-3">

                <select class="select select-bordered w-full">
                  <option>Does not repeat</option>
                  <option>Daily</option>
                  <option>Weekly</option>
                </select>

                <input type="number" min="1"
                  placeholder="Every X days"
                  class="input input-bordered w-full" />

                <input type="date"
                  class="input input-bordered w-full" />

              </div>
            </div>
            <button class="btn btn-primary w-full" @click="addSession">
              Add Session
            </button>
          </div>

          <!-- List -->
          <div class="space-y-3">
            <div
              v-for="(s, index) in sessions"
              :key="index"
              class="flex justify-between items-center bg-base-200 rounded-2xl p-4 hover:shadow-md transition"
            >

              <!-- LEFT -->
              <div class="flex items-center gap-4">

                <!-- DATE BOX -->
                <div class="bg-base-100 rounded-xl px-3 py-2 text-center w-16">
                  <p class="text-xs text-primary font-semibold">
                    {{ formatMonth(s.start) }}
                  </p>
                  <p class="text-lg font-bold">
                    {{ formatDay(s.start) }}
                  </p>
                </div>

                <!-- INFO -->
                <div class="space-y-1">

                  <!-- TIME + LOCATION -->
                  <div class="flex items-center gap-2 text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    <span>
                      {{ formatTime(s.start) }} - {{ formatTime(s.end) }}
                    </span>
                    <span>|</span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                    </svg>
                    <span>
                      {{ s.location }}
                    </span>
                  </div>

                  <!-- SEATS + BADGE -->
                  <div class="flex items-center gap-3 text-sm text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                    </svg>

                    <span>
                      {{ s.capacity }} seats
                    </span>

                    <span v-if="s.recurring" class="badge badge-primary badge-sm">
                      {{ s.recurring }}
                    </span>
                  </div>

                </div>
              </div>

              <!-- RIGHT -->
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                </svg>

                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                </svg>

                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6" @click="removeSession(index)">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>

              </div>

            </div>
          </div>

        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end gap-3">
        <button class="btn">Cancel</button>
        <button class="btn btn-primary" @click="submit">
          Create Event
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"

const event = ref({
  title: "",
  location: "",
  description: ""
})

const limitEnabled = ref(true)
const limit = ref(1)
watch(limitEnabled, (val) => {
  if (val) {
    limit.value = 1
  } else {
    limit.value = null
  }
})

const sessions = ref([])

const newSession = ref({
  start: "",
  end: "",
  capacity: "",
  location: "",
  desc: ""
})

function addSession() {
  sessions.value.push({ ...newSession.value })
  newSession.value = {
    start: "",
    end: "",
    capacity: "",
    location: "",
    desc: ""
  }
}

function removeSession(index) {
  sessions.value.splice(index, 1)
}

function submit() {
  console.log({
    event: event.value,
    sessions: sessions.value
  })
}

function formatDay(date) {
  return new Date(date).getDate();
}

function formatMonth(date) {
  return new Date(date).toLocaleString('en-US', { month: 'short' }).toUpperCase();
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });
}


</script>