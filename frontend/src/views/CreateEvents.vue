<template>
  <div class="min-h-screen bg-base-200">
    <nav class="sticky top-0 z-50 bg-white shadow px-6">
      <div class="flex justify-between items-center h-16">
        <button onclick="my_modal_3.showModal()" class="flex items-center gap-2 text-xl hover:opacity-80">

          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>

          <span class="font-bold text-lg">Create New Event</span>
        </button>
        <dialog id="my_modal_3" class="modal">
          <div class="modal-box">
            <form method="dialog">
              <button class="btn btn-lg btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <h3 class="text-lg font-bold">Leave this page?</h3>
            <p class="py-4">You have unsaved changes. What would you like to do?</p>
            <div class="flex gap-4">
              <button type="button" class="btn btn-primary flex-1 p-4" @click="saveDraftAndLeave">
                Save as draft & leave
              </button>

              <button type="button" @click="goToDashboard" class="btn flex-1">
                Leave without saving
              </button>
            </div>
          </div>
        </dialog>
        <div class="dropdown dropdown-end">

          <!-- Avatar (ปุ่มกด) -->
          <div tabindex="0" role="button" class="avatar avatar-online cursor-pointer">
            <div class="bg-neutral text-neutral-content w-10 rounded-full">
              <!-- <span class="text-xl">AI</span> -->
            </div>
          </div>

          <!-- Dropdown menu -->
          <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
            <li>
              <router-link to="/setting" @click="$event.currentTarget.blur()">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
                Settings
              </router-link>
            </li>
            <li>
              <router-link to="/login" class="text-error" @click="$event.currentTarget.blur()">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
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
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
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
      <div class="bg-base-100 shadow p-6 rounded-lg">
        <div class="flex items-baseline justify-between">
          <div>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-5 inline">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>

            <span class="text-lg font-semibold inline"> Session Management</span>
          </div>
          <div>
            <span class="text-md font-semibold inline">
              Limit sessions per participant
              <span class="opacity-60 mr-2">(optional)</span>
            </span>

            <input type="checkbox" v-model="limitEnabled" class="toggle toggle-primary mr-2" />
            <input type="number" v-model="limit" :disabled="!limitEnabled" min="1"
              class="input input-bordered w-14 text-center mr-2" />
          </div>
        </div>


        <div class="p-3">

          <!-- Add session -->
          <div class="border border-dashed p-6 rounded-xl space-y-3">
            <h2 class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>

              Add New Session
            </h2>

            <div class="flex gap-2">

              <!-- Start -->
              <div>
                <label class="text-sm ">Start</label>
                <input type="datetime-local" v-model="newSession.start" class="input input-bordered w-full" />
              </div>

              <!-- End -->
              <div>
                <label class="text-sm">End</label>
                <input type="datetime-local" v-model="newSession.end" class="input input-bordered p-2" />
              </div>


              <!-- Capacity -->
              <div>
                <label class="text-sm">Seats capacity</label>
                <input type="number" v-model="newSession.capacity" placeholder="Seats" min="1" @input="newSession.capacity = $event.target.value === ''
                  ? null
                  : Math.max(1, Number($event.target.value))" class="input input-bordered w-full" />
              </div>

              <!-- Location -->
              <div>
                <span class="text-sm">Location</span>
                <span class="text-sm opacity-60"> (optional)</span>
                <input type="text" v-model="newSession.location" placeholder="Room 101"
                  class="input input-bordered w-full" />
              </div>

            </div>
            <div class="md:col-span-2">
              <span class="text-sm">Description</span>
              <span class="text-sm opacity-60"> (optional)</span>
              <textarea v-model="newSession.description" class="textarea textarea-bordered w-full"></textarea>
            </div>


            <div class="card bg-base-100 shadow p-4 space-y-4">
              <h2 class="card-title flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>

                Repeat session
              </h2>

              <!-- content -->
              <div class="grid md:grid-cols-3 gap-3">
                <div>
                  <select class="select select-bordered w-full" v-model="repeatsChoose.type">
                    <option value="Does not repeat">Does not repeat</option>
                    <option value="Daily">Daily</option>
                    <option value="Weekly">Weekly</option>
                    <option value="Monthly">Monthly</option>
                    <option value="Yearly">Yearly</option>
                  </select>
                </div>
                <div>
                  <input type="number" min="1" v-model="repeatsChoose.interval" :placeholder="repeatsChoose.type
                    ? `Every X ${repeatsChoose.type.toLowerCase()}`
                    : 'Every X'" class="input input-bordered w-full"
                    :disabled="!repeatsChoose.type || repeatsChoose.type === 'Does not repeat'" />
                </div>
                <div class="text-sm p-2">
                  <!-- เปิด/ปิด -->
                  <label class="flex items-center gap-2">
                    <input type="checkbox" v-model="repeatEndEnabled" checked="checked"
                      class="checkbox checkbox-success checkbox-sm" />
                    <span class="font-semibold">Repeat until</span>
                  </label>

                  <!-- โผล่เมื่อเปิด -->
                  <div v-if="repeatEndEnabled" class="mt-3 space-y-3">

                    <!-- เลือก type -->
                    <div class="flex gap-4 items-center">
                      <label class="flex items-center gap-2">
                        <input type="radio" value="date" v-model="repeatEnd.type" />
                        <span>Until date</span>
                      </label>
                    </div>
                    <div>
                      <label class="flex items-center gap-2">
                        <input type="radio" value="count" v-model="repeatEnd.type" />
                        <span>Number of times</span>
                      </label>
                    </div>

                    <!-- input ตาม type -->
                    <input v-if="repeatEnd.type === 'date'" type="date" v-model="repeatEnd.date"
                      class="input input-bordered w-full" />

                    <input v-if="repeatEnd.type === 'count'" type="number" min="1" v-model="repeatEnd.count"
                      placeholder="Number of times" class="input input-bordered w-full" />
                  </div>
                </div>

              </div>
            </div>
            <div class="flex gap-2">

              <button v-if="isEditing" class="btn flex-1" @click="cancelEdit">
                Cancel
              </button>

              <button class="btn btn-primary flex-1" @click="isEditing ? saveEdit() : addSession()">
                {{ isEditing ? "Save Edit" : "Add Session" }}
              </button>
            </div>
          </div>

          <!-- List -->
          <div class="space-y-2 p-4">
            <div v-for="(s, index) in sessions" :key="index"
              class="flex justify-between items-center bg-base-200 rounded-2xl p-4 hover:shadow-md transition">

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
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                    <span>
                      {{ formatTime(s.start) }} - {{ formatTime(s.end) }}
                    </span>
                    <span>|</span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                    </svg>
                    <span>
                      {{ s.location }}
                    </span>
                  </div>

                  <!-- SEATS + BADGE -->
                  <div class="flex items-center gap-3 text-sm text-gray-500">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
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
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6" @click="copySession(s)">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                </svg>

                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6" @click="editSession(s, index)">
                  <path stroke-linecap=" round" stroke-linejoin="round"
                  d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                </svg>

                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6" @click="removeSession(index)">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>

              </div>

            </div>
          </div>

        </div>
      </div>

      <!-- Footer -->
      <div class="flex gap-4 justify-end">
        <button @click="handleCancel" class="btn">
          Cancel
        </button>

        <button @click="submit" class="btn btn-primary">
          Create Event
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRouter } from 'vue-router'
import { createEvent } from "@/services/event"

const router = useRouter()
const isEditing = ref(false)
const editingIndex = ref(null)
const backupSession = ref(null)


const handleCancel = () => {
  event.value = {
    title: "",
    location: "",
    description: ""
  }

  // reset limit
  limitEnabled.value = false
  limit.value = 1

  // reset sessions
  sessions.value = []

  // reset form session
  newSession.value = {
    start: "",
    end: "",
    capacity: "",
    location: "",
    description: ""
  }

  // reset repeat
  repeatEndEnabled.value = false
  repeatEnd.value = {
    type: "never",
    date: "",
    count: null
  }

  repeatsChoose.value = {
    type: "Does not repeat",
    interval: ""
  }

  editingIndex.value = null
}

const goToDashboard = () => {
  router.push("/dashboard")
}

//const openModal = () => {
//  document.getElementById("my_modal_3").showModal()
//}

const event = ref({
  title: "",
  location: "",
  description: ""
})

const limitEnabled = ref(false)
const limit = ref(1)
watch(limitEnabled, (val) => {
  if (!val) {
    limit.value = 1
  } else {
    limit.value = null
  }
})

const sessions = ref([])

const newSession = ref({
  start: "",
  end: "",
  capacity: null,
  location: "",
  desc: ""
})

const repeatEndEnabled = ref(false)

const repeatEnd = ref({
  type: "never",
  date: "",
  count: null
})

const repeatsChoose = ref({
  type: "Does not repeat",
  interval: "",
})

function copySession(s) {
  const clone = {
    ...s,
    start: s.start,
    end: s.end
  }

  sessions.value.push(clone)
}

function saveEdit() {
  sessions.value.splice(editingIndex.value, 0, {
    ...newSession.value
  })

  resetForm()
}

function cancelEdit() {
  sessions.value.splice(editingIndex.value, 0, backupSession.value)

  resetForm()
}

function editSession(s, index) {
  newSession.value = { ...s }

  isEditing.value = true
  editingIndex.value = index

  // เก็บของเดิมไว้
  backupSession.value = { ...s }

  sessions.value.splice(index, 1)
}

function addSession() {
  if (!newSession.value.start || !newSession.value.end) return
  if (newSession.value.start >= newSession.value.end) {
    alert("End must be after start")
    return
  }
  const type = repeatsChoose.value.type
  const interval = Number(repeatsChoose.value.interval) || 1

  const startDate = new Date(newSession.value.start)
  const endDate = new Date(newSession.value.end)

  const clone = (d) => new Date(d.getTime())

  const addByType = (date) => {
    const d = new Date(date)

    if (type === "Daily") d.setDate(d.getDate() + interval)
    if (type === "Weekly") d.setDate(d.getDate() + 7 * interval)
    if (type === "Monthly") d.setMonth(d.getMonth() + interval)
    if (type === "Yearly") d.setFullYear(d.getFullYear() + interval)

    return d
  }

  const format = (date) => {
    const pad = (n) => n.toString().padStart(2, "0")
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
  }

  if (type === "Does not repeat") {
    sessions.value.push({
      ...newSession.value,
      start: format(startDate),
      end: format(endDate),
    })
  } else {
    let currentStart = clone(startDate)
    let currentEnd = clone(endDate)

    let i = 0

    while (true) {
      sessions.value.push({
        ...newSession.value,
        start: format(currentStart),
        end: format(currentEnd),
        recurring: type
      })

      i++

      // stop by count
      if (repeatEndEnabled.value && repeatEnd.value.type === "count") {
        if (repeatEnd.value.count && i >= repeatEnd.value.count) break
      }

      // stop by date
      if (repeatEndEnabled.value && repeatEnd.value.type === "date") {
        if (currentStart >= new Date(repeatEnd.value.date)) break
      }

      // safety กัน infinite
      if (i > 1000) break

      currentStart = addByType(currentStart)
      currentEnd = addByType(currentEnd)
    }
  }
  resetForm()
}

const saveDraftAndLeave = async () => {
  const payload = {
    title: event.value.title,
    location: event.value.location,
    description: event.value.description,
    max_sessions_per_user: limitEnabled.value ? limit.value : null,
    is_draft: true,
    sessions: sessions.value.map(s => ({
      start_datetime: s.start ? new Date(s.start).toISOString() : null,
      end_datetime: s.end ? new Date(s.end).toISOString() : null,
      seat_capacity: s.capacity ? Number(s.capacity) : 0
    }))
  }

  try {
    await createEvent(payload)

    const modal = document.getElementById("my_modal_3")
    modal?.close()

    router.push('/events')
  } catch (err) {
    console.error("Save draft failed:", err)
  }
}

function resetForm() {
  newSession.value = {
    start: "",
    end: "",
    capacity: null,
    location: "",
    desc: ""
  }

  repeatsChoose.value = {
    type: "Does not repeat",
    interval: ""
  }

  repeatEnd.value = {
    type: "never",
    date: "",
    count: null
  }

  repeatEndEnabled.value = false

  isEditing.value = false
  editingIndex.value = null
  backupSession.value = null
}

function removeSession(index) {
  sessions.value.splice(index, 1)
}

const submit = async () => {
  const payload = {
    title: event.value.title,
    location: event.value.location,
    description: event.value.description,
    max_sessions_per_user: limitEnabled.value ? limit.value : null,
    is_draft: false,
    sessions: sessions.value.map(s => ({
      start_datetime: s.start ? new Date(s.start).toISOString() : null,
      end_datetime: s.end ? new Date(s.end).toISOString() : null,
      seat_capacity: s.capacity ? Number(s.capacity) : 0
    }))
  }

  try {
    await createEvent(payload)
    router.push('/events')
  } catch (err) {
    console.error("Create event failed:", err)
  }
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