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

      </div>
    </nav>

    <div class="max-w-4xl mx-auto p-2 space-y-6 pb-24">
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
              <input ref="titleInput" v-model="event.title" type="text" class="input input-bordered w-full" required />
              <p v-if="submitted && !event.title.trim()" class="text-red-500 text-sm mt-1">
                Event title is required.
              </p>
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
      <div ref="sessionManagementRef" class="bg-base-100 shadow p-6 rounded-lg">
        <div class="flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-5 inline">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <span class="text-lg font-semibold inline">Session Management</span>

          </div>

          <div class="flex items-center gap-3 px-3 py-1.5 rounded-lg border border-base-300">
            <span class="text-md font-normal flex-1">
              Max sessions per participant
              <span class="text-sm opacity-40 font-normal">(optional)</span>
            </span>
            <div class="flex flex-wrap items-center gap-x-1">
              <input type="checkbox" v-model="limitEnabled" class="toggle toggle-primary" />
              <div class="flex items-center gap-2"></div>
              <input type="number" v-model="limit" :min="limitEnabled ? 1 : undefined" :disabled="!limitEnabled"
                class="input input-bordered w-20" />
            </div>
          </div>
        </div>

        <div class="p-0 mt-3">

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

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">

              <!-- Start -->
              <div class="flex flex-col">
                <label class="text-sm ">Start</label>
                <input type="datetime-local" v-model="newSession.start" class="input input-bordered w-full" />
              </div>

              <!-- End -->
              <div class="flex flex-col">
                <label class="text-sm">End</label>
                <input type="datetime-local" v-model="newSession.end" class="input input-bordered w-full" />
              </div>


              <!-- Capacity -->
              <div>
                <span class="text-sm">Seats capacity</span>
                <span class="text-sm opacity-60"> (optional)</span>
                <input type="number" v-model="newSession.capacity" placeholder="e.g. 30" min="1" @input="newSession.capacity = $event.target.value === ''
                  ? null
                  : Math.max(1, Number($event.target.value))" class="input input-bordered w-full" />
              </div>
            </div>
            <!-- Location -->
            <div>
              <span class="text-sm">Location</span>
              <span class="text-sm opacity-60"> (optional)</span>
              <input type="text" v-model="newSession.location" placeholder="e.g. Room 101"
                class="input input-bordered w-full" />
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
                  <input type="number" min="1" v-model="repeatsChoose.interval" :placeholder="repeatsChoose.type === 'Does not repeat' || !repeatsChoose.type
                    ? 'Repeat interval if repeat session'
                    : repeatsChoose.type === 'Daily' ? 'Every N day(s)'
                      : repeatsChoose.type === 'Weekly' ? 'Every N week(s)'
                        : repeatsChoose.type === 'Monthly' ? 'Every N month(s)'
                          : repeatsChoose.type === 'Yearly' ? 'Every N year(s)'
                            : 'Interval'" class="input input-bordered w-full"
                    :disabled="!repeatsChoose.type || repeatsChoose.type === 'Does not repeat'" />
                </div>
                <div class="text-sm p-2">
                  <!-- เปิด/ปิด -->
                  <label class="flex items-center gap-2">
                    <input type="checkbox" v-model="repeatEndEnabled"
                      :disabled="!repeatsChoose.type || repeatsChoose.type === 'Does not repeat'"
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

          <!-- Divider -->
          <div v-if="sessions.length" class="mt-4">
            <div class="relative py-2">
              <div aria-hidden="true" class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-slate-200 dark:border-slate-800"></div>
              </div>
              <div class="relative flex justify-center">
                <span class="bg-base-100 px-3 text-sm font-medium opacity-60">
                  Added Sessions ({{ sessions.length }})
                </span>
              </div>
            </div>

            <!-- List -->
            <div class="flex flex-col gap-4">
              <div v-for="(s, index) in sessions" :key="index"
                class="group relative flex flex-col sm:flex-row items-center gap-4 p-4 rounded-lg border border-base-300 bg-base-200 hover:border-primary/50 transition-colors">

                <!-- LEFT -->
                <div class="flex-1 min-w-0 w-full">
                  <div class="flex flex-col gap-2">


                    <!-- TIME + LOCATION -->
                    <div class="flex items-center gap-2 text-base font-semibold">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                      </svg>
                      <span>{{ formatDate(s.start) }}, {{ formatTime(s.start) }} – {{ formatDate(s.end) }} ,{{
                        formatTime(s.end) }}</span>
                    </div>
                    <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm opacity-60">
                      <span v-if="getEffectiveSessionLocation(s)" class="flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                        </svg>

                        {{ getEffectiveSessionLocation(s) }}
                      </span>
                      <span v-if="getEffectiveSessionLocation(s) && s.capacity != null" class="opacity-40">|</span>

                      <!-- SEATS + BADGE -->
                      <span v-if="s.capacity != null" class="flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                        </svg>
                        {{ s.capacity }} seats
                      </span>

                      <span v-if="s.recurring"
                        class="flex items-center text-primary bg-primary/10 px-2 py-0.5 rounded text-xs font-medium opacity-100">
                        {{ s.recurring }}
                      </span>

                      <span v-if="s.repeat_every_text"
                        class="flex items-center text-secondary bg-secondary/10 px-2 py-0.5 rounded text-xs font-medium opacity-100">
                        {{ s.repeat_every_text }}
                      </span>

                      <span v-if="s.repeat_until_text"
                        class="flex items-center text-info bg-info/10 px-2 py-0.5 rounded text-xs font-medium opacity-100">
                        {{ s.repeat_until_text }}
                      </span>
                    </div>

                  </div>
                </div>

                <!-- RIGHT -->
                <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
                  <div class="flex items-center gap-2">
                    <template v-if="activeCopyIndex === index">
                      <input v-if="activeCopyIndex === index" ref="copyInput" type="number" v-model.number="copyCount"
                        min="1" class="input input-bordered w-20" />
                      <button v-if="activeCopyIndex === index" class="btn btn-sm btn-primary" @click="confirmCopy(s)">
                        Duplicate
                      </button>
                    </template>
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-blue-500"
                      @click="handleCopyClick(s, index)" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                    </svg>
                  </div>

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
      </div>
    </div>

    <!-- Footer -->
    <div class="fixed bottom-0 left-0 w-full z-20">
      <div
        class="bg-base-100 border-t border-base-300 p-4 pointer-events-auto flex justify-end gap-3 px-10 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <button @click="showDiscardModal = true" class="btn">
          Discard changes
        </button>
        <!-- Discard Modal -->
        <div v-if="showDiscardModal"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/20 backdrop-blur-[2px]"
          @click.self="showDiscardModal = false">
          <div class="bg-base-100 rounded-2xl shadow-xl w-full max-w-sm overflow-hidden border border-base-300">
            <div class="p-8 flex flex-col items-center text-center">

              <!-- Icon -->
              <div class="w-12 h-12 rounded-full bg-warning/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6 text-warning">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
                </svg>
              </div>

              <h3 class="text-xl font-bold mb-2">Discard Changes?</h3>
              <p class="text-sm opacity-60 mb-8 leading-relaxed">
                Are you sure you want to discard your changes? All unsaved information will be lost.
              </p>

              <div class="flex gap-3 w-full">
                <button class="flex-1 btn btn-outline rounded-full" @click="showDiscardModal = false">
                  Keep Editing
                </button>
                <button class="flex-1 btn rounded-full bg-red-400 hover:bg-red-500 text-white border-none"
                  @click="discardChanges">
                  Discard
                </button>
              </div>
            </div>
          </div>
        </div>

        <button @click="submit" class="btn btn-primary">
          Create Event
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue"
import { useRouter } from 'vue-router'
import { createEvent } from "@/services/event"

const router = useRouter()
const isEditing = ref(false)
const editingIndex = ref(null)
const backupSession = ref(null)
const submitted = ref(false)
const titleInput = ref(null)
const showDiscardModal = ref(false)

const trimFields = () => {
  if (event.value.title != null) {
    event.value.title = event.value.title.trim()
  }
  if (event.value.location != null) {
    event.value.location = event.value.location.trim()
  }
  if (event.value.description != null) {
    event.value.description = event.value.description.trim()
  }
}

const getEffectiveSessionLocation = (session) => {
  const sessionLocation = typeof session?.location === "string" ? session.location.trim() : ""
  if (sessionLocation) return sessionLocation

  return typeof event.value?.location === "string" ? event.value.location.trim() : ""
}


const handleCancel = () => {
  event.value = {
    title: "",
    location: "",
    description: ""
  }

  // reset limit
  limitEnabled.value = false
  limit.value = null

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

const discardChanges = () => {
  handleCancel()
  resetForm()
  showDiscardModal.value = false
}


const event = ref({
  title: "",
  location: "",
  description: ""
})

const limitEnabled = ref(false)
const limit = ref(null)
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

const copyCount = ref(1)
const activeCopyIndex = ref(null)
const copyInput = ref(null)
const sessionManagementRef = ref(null)

const handleCopyClick = async (session, index) => {
  if (activeCopyIndex.value === index) {
    activeCopyIndex.value = null
    return
  }

  activeCopyIndex.value = index
  copyCount.value = 1

  await nextTick()
  const inputElement = Array.isArray(copyInput.value) ? copyInput.value[0] : copyInput.value
  inputElement?.focus()
}

const confirmCopy = (session) => {
  if (!copyCount.value || copyCount.value < 1) return

  for (let i = 0; i < copyCount.value; i++) {
    sessions.value.push({ ...session })
  }

  activeCopyIndex.value = null
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

async function editSession(s, index) {
  newSession.value = { ...s }

  isEditing.value = true
  editingIndex.value = index

  // เก็บของเดิมไว้
  backupSession.value = { ...s }

  sessions.value.splice(index, 1)

  await nextTick()
  sessionManagementRef.value?.scrollIntoView({
    behavior: "smooth",
    block: "start"
  })

}

function addSession() {
  if (!newSession.value.start || !newSession.value.end) {
    alert("Start and end are required")
    return
  }
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

  const repeatUntilText =
    repeatEndEnabled.value && repeatEnd.value.type === "count" && repeatEnd.value.count
      ? `Repeat session for ${repeatEnd.value.count} time(s)`
      : repeatEndEnabled.value && repeatEnd.value.type === "date" && repeatEnd.value.date
        ? `Repeat until ${formatDate(repeatEnd.value.date)}`
        : null

  const repeatUnitByType = {
    Daily: "day",
    Weekly: "week",
    Monthly: "month",
    Yearly: "year"
  }

  const repeatEveryText = type !== "Does not repeat" && repeatUnitByType[type]
    ? `Every ${interval} ${repeatUnitByType[type]}(s)`
    : null

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
        recurring: type,
        repeat_every_text: repeatEveryText,
        repeat_until_text: repeatUntilText
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
      location: getEffectiveSessionLocation(s),
      seat_capacity: s.capacity ? Number(s.capacity) : null
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
  submitted.value = true
  trimFields()
  if (!event.value.title) {
    titleInput.value?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    titleInput.value?.focus()
    return
  }
  const payload = {
    title: event.value.title,
    location: event.value.location,
    description: event.value.description,
    max_sessions_per_user: limitEnabled.value ? limit.value : null,
    is_draft: false,
    sessions: sessions.value.map(s => ({
      start_datetime: s.start ? new Date(s.start).toISOString() : null,
      end_datetime: s.end ? new Date(s.end).toISOString() : null,
      location: getEffectiveSessionLocation(s),
      seat_capacity: s.capacity ? Number(s.capacity) : null
    }))
  }

  console.log("Payload:", payload)

  try {
    const createdEvent = await createEvent(payload)
    const eventUuid = createdEvent?.share_uuid || createdEvent?.uuid || createdEvent?.event_uuid

    if (eventUuid) {
      router.push(`/event/overview/${eventUuid}`)
    } else {
      router.push('/events')
    }
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

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

function formatTime(date) {
  return new Date(date).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });
}



</script>