<template>
  <div class="min-h-screen bg-base-200 font-display pb-20">
    <nav class="sticky top-0 z-50 bg-white shadow px-6">
      <div class="flex justify-between items-center h-16">
        <button onclick="my_modal_3.showModal()" class="flex items-center gap-2 text-xl hover:opacity-80">

          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>

          <span class="font-bold text-lg">Edit Event</span>
        </button>
        <dialog id="my_modal_3" class="modal">
          <div class="modal-box">
            <form method="dialog">
              <button class="btn btn-lg btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <h3 class="text-lg font-bold">Leave this page?</h3>
            <p class="py-4">You have unsaved changes. What would you like to do?</p>
            <div class="flex gap-4">
              <button type="button" class="btn btn-primary flex-1 p-4" @click="saveChangesAndLeave">
                Save Changes & Leave
              </button>

              <button type="button" @click="goToPreviousPage" class="btn flex-1">
                Leave without saving
              </button>
            </div>
          </div>
        </dialog>

      </div>
    </nav>
    <div class="max-w-4xl mx-auto p-4 lg:p-6 space-y-6 mt-4">
      
      <!-- Event Details Card -->
      <div class="card bg-base-100 shadow-sm border border-base-200">
        <div class="card-body">
          <h2 class="card-title text-xl mb-4">
            Event Details
          </h2>

          <div class="grid md:grid-cols-2 gap-5">
            <div class="md:col-span-2">
              <label class="label pt-0 pb-1">
                <span class="label-text font-semibold">Event Title <span class="text-error">*</span></span>
              </label>
              <input v-model="event.title" type="text" class="input input-bordered w-full focus:input-primary" placeholder="Enter event title" />
            </div>

            <div class="md:col-span-2">
              <label class="label pt-0 pb-1">
                <span class="label-text font-semibold">Location <span class="opacity-60 font-normal">(optional)</span></span>
              </label>
              <input v-model="event.location" type="text" class="input input-bordered w-full focus:input-primary" placeholder="Online, Room 101, etc." />
            </div>

            <div class="md:col-span-2">
              <label class="label pt-0 pb-1">
                <span class="label-text font-semibold">Description <span class="opacity-60 font-normal">(optional)</span></span>
              </label>
              <textarea v-model="event.description" class="textarea textarea-bordered w-full focus:textarea-primary min-h-[100px]" placeholder="Tell participants what this event is about..."></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- Session Management Card -->
      <div class="card bg-base-100 shadow-sm border border-base-200">
        <div class="card-body p-6">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
            <div class="flex items-center gap-3">
              <h2 class="card-title text-xl m-0">
                Session Management
              </h2>
              <span class="badge badge-sm badge-neutral">{{ userTimezone }}</span>
            </div>
            
            <div class="flex items-center gap-3 bg-base-200 px-4 py-2 rounded-lg border border-base-300">
              <span class="text-sm font-semibold">
                Limit sessions per user <span class="opacity-60 font-normal hidden md:inline">(optional)</span>
              </span>
              <input type="checkbox" v-model="limitEnabled" class="toggle toggle-primary toggle-sm" />
              <input 
                type="number" 
                v-model="limit" 
                :disabled="!limitEnabled" 
                min="1"
                class="input input-sm input-bordered w-16 text-center" 
                :class="{'opacity-50': !limitEnabled}"
              />
            </div>
          </div>

          <!-- Session List -->
          <div class="space-y-3">
            <div v-if="sessions.length === 0" class="text-center py-10 bg-base-200/50 rounded-xl border border-dashed border-base-300">
              <span class="material-symbols-outlined text-4xl text-base-content/30 mb-2">event_busy</span>
              <p class="text-base-content/60 font-medium">No sessions added yet.</p>
              <p class="text-xs text-base-content/40 mt-1">Add at least one session so users can register.</p>
            </div>

            <!-- Paginated Sessions View -->
            <div 
              v-for="(s, index) in paginatedSessions" 
              :key="getGlobalIndex(index)"
              class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-base-100 border border-base-200 rounded-xl p-4 hover:shadow-md transition-all group"
            >
              <!-- LEFT INFO -->
              <div class="flex items-center gap-4 w-full sm:w-auto">
                <!-- Date Box -->
                <div class="bg-primary/10 rounded-xl px-3 py-2 text-center min-w-[4.5rem] border border-primary/20">
                  <p class="text-[11px] text-primary font-bold uppercase tracking-widest leading-none mb-1">
                    {{ formatMonth(s.start) }}
                  </p>
                  <p class="text-xl font-black text-primary leading-none">
                    {{ formatDay(s.start) }}
                  </p>
                </div>

                <!-- Text Info -->
                <div class="space-y-1">
                  <!-- Time & Location -->
                  <div class="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm font-medium">
                    <span class="flex items-center gap-1 text-base-content/80">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                      </svg>
                      {{ formatTime(s.start) }} - {{ formatTime(s.end) }}
                    </span>
                    <span class="hidden sm:inline text-base-content/30">|</span>
                    <span v-if="s.location || event.location" class="flex items-center gap-1 text-base-content/80">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                      </svg>

                      {{ s.location || event.location }}
                    </span>
                  </div>

                  <!-- Seats & Recurring Badge -->
                  <div class="flex items-center gap-3 text-xs text-base-content/60">
                    <span class="flex items-center gap-1 font-semibold">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
                      </svg>

                      {{ s.capacity || 'Unlimited' }} seats
                    </span>
                    <span v-if="s.recurring" class="badge badge-primary badge-sm badge-outline text-[10px] font-bold">
                      <span class="material-symbols-outlined text-[12px] mr-1">repeat</span>
                      {{ s.recurring }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- RIGHT ACTIONS -->
              <div class="flex items-center gap-1 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity self-end sm:self-auto mt-2 sm:mt-0">
                <button @click="openDuplicateModal(s)" class="btn btn-sm btn-circle btn-ghost tooltip" data-tip="Duplicate">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                  </svg>
                </button>
                <button @click="openEditModal(s, getGlobalIndex(index))" class="btn btn-sm btn-circle btn-ghost text-info tooltip" data-tip="Edit">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>
                </button>
                <button @click="removeSession(getGlobalIndex(index))" class="btn btn-sm btn-circle btn-ghost text-error tooltip" data-tip="Remove">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Pagination Controls -->
            <div v-if="totalPages > 1" class="flex justify-between items-center bg-base-100 border border-base-200 p-2 rounded-xl mt-4">
              <button class="btn btn-sm btn-ghost" @click="currentPage--" :disabled="currentPage === 1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 mr-1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                </svg>
                Prev
              </button>
              <span class="text-sm font-semibold text-base-content/70">Page {{ currentPage }} of {{ totalPages }}</span>
              <button class="btn btn-sm btn-ghost" @click="currentPage++" :disabled="currentPage === totalPages">
                Next
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 ml-1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </button>
            </div>
            
            <!-- Add New Session Button (Triggers Modal) -->
            <button @click="openAddModal" class="btn btn-outline btn-block border-dashed border-2 hover:bg-base-200 hover:text-base-content mt-4 h-auto py-4">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <span class="text-lg">Add New Session</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="flex gap-4 justify-end pt-4 border-t border-base-300">
        <button @click="goToPreviousPage" class="btn btn-ghost">
          Cancel
        </button>
        <button @click="submit" class="btn btn-primary px-8">
          Save Changes
        </button>
      </div>

    </div>

    <!-- ========================================== -->
    <!-- SESSION MODAL                              -->
    <!-- ========================================== -->
    <dialog id="session_modal" class="modal" ref="sessionModalRef">
      <div class="modal-box w-11/12 max-w-2xl bg-base-100 p-0 overflow-hidden">
        
        <!-- Modal Header -->
        <div class="bg-base-200 px-6 py-4 border-b border-base-300 flex justify-between items-center">
          <h3 class="font-bold text-lg flex items-center gap-2">
            {{ isEditing ? 'Edit Session' : 'Add New Session' }}
          </h3>
          <button @click="closeSessionModal" class="btn btn-sm btn-circle btn-ghost">✕</button>
        </div>
        
        <!-- Modal Body -->
        <div class="p-6 space-y-5">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Start -->
            <div>
              <label class="label pt-0 pb-1"><span class="label-text font-semibold">Start Time ({{ userTimezone }})</span></label>
              <input type="datetime-local" v-model="newSession.start" class="input input-bordered w-full focus:input-primary" />
            </div>

            <!-- End -->
            <div>
              <label class="label pt-0 pb-1"><span class="label-text font-semibold">End Time ({{ userTimezone }})</span></label>
              <input type="datetime-local" v-model="newSession.end" class="input input-bordered w-full focus:input-primary" />
            </div>

            <!-- Capacity -->
            <div>
              <label class="label pt-0 pb-1"><span class="label-text font-semibold">Seat Capacity</span></label>
              <input 
                type="number" 
                v-model="newSession.capacity" 
                placeholder="Unlimited if empty" 
                min="1" 
                @input="newSession.capacity = $event.target.value === '' ? null : Math.max(1, Number($event.target.value))" 
                class="input input-bordered w-full focus:input-primary" 
              />
            </div>

            <!-- Location -->
            <div>
              <label class="label pt-0 pb-1"><span class="label-text font-semibold">Location <span class="opacity-60 font-normal">(optional)</span></span></label>
              <input type="text" v-model="newSession.location" placeholder="Specific room/link" class="input input-bordered w-full focus:input-primary" />
            </div>
          </div>

          <!-- Repeat Settings (Hidden if Editing to prevent complex logic clashes, optional to show) -->
          <div v-if="!isEditing" class="bg-base-200/50 rounded-xl p-4 border border-base-200 mt-4">
            <h4 class="font-bold text-sm mb-3 flex items-center gap-1">
              Repeat Setup
            </h4>
            
            <div class="grid sm:grid-cols-2 gap-4">
              <select class="select select-bordered w-full" v-model="repeatsChoose.type">
                <option value="Does not repeat">Does not repeat</option>
                <option value="Daily">Daily</option>
                <option value="Weekly">Weekly</option>
                <option value="Monthly">Monthly</option>
                <option value="Yearly">Yearly</option>
              </select>

              <input 
                type="number" 
                min="1" 
                v-model="repeatsChoose.interval" 
                :placeholder="repeatsChoose.type !== 'Does not repeat' ? `Every X ${repeatsChoose.type.toLowerCase()}` : 'Every X'" 
                class="input input-bordered w-full"
                :disabled="repeatsChoose.type === 'Does not repeat'" 
              />
            </div>

            <div v-if="repeatsChoose.type !== 'Does not repeat'" class="mt-4 pt-4 border-t border-base-300">
              <label class="flex items-center gap-2 cursor-pointer mb-3">
                <input type="checkbox" v-model="repeatEndEnabled" class="checkbox checkbox-primary checkbox-sm" />
                <span class="font-semibold text-sm">Set end limit</span>
              </label>

              <div v-if="repeatEndEnabled" class="grid sm:grid-cols-2 gap-4 bg-base-100 p-3 rounded-lg border border-base-200">
                <div class="space-y-2">
                  <label class="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="radio" value="date" v-model="repeatEnd.type" class="radio radio-primary radio-sm" /> Until Date
                  </label>
                  <label class="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="radio" value="count" v-model="repeatEnd.type" class="radio radio-primary radio-sm" /> Number of times
                  </label>
                </div>
                
                <div class="flex items-center">
                  <input v-if="repeatEnd.type === 'date'" type="date" v-model="repeatEnd.date" class="input input-bordered input-sm w-full" />
                  <input v-if="repeatEnd.type === 'count'" type="number" min="1" v-model="repeatEnd.count" placeholder="Ex: 5 times" class="input input-bordered input-sm w-full" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="bg-base-200 px-6 py-4 border-t border-base-300 flex justify-end gap-3 rounded-b-xl">
          <button class="btn btn-ghost" @click="closeSessionModal">Cancel</button>
          <button class="btn btn-primary px-8" @click="isEditing ? saveEdit() : addSession()">
            {{ isEditing ? "Save Session" : "Add Session" }}
          </button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button @click="closeSessionModal">close</button>
      </form>
    </dialog>

    <!-- ========================================== -->
    <!-- DUPLICATE SESSION MODAL                    -->
    <!-- ========================================== -->
    <dialog id="duplicate_modal" class="modal" ref="duplicateModalRef">
      <div class="modal-box max-w-sm">
        <form method="dialog">
          <button @click="closeDuplicateModal" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>
        <h3 class="font-bold text-lg mb-4">Duplicate Session</h3>
        <p class="text-sm text-base-content/70 mb-4">How many copies of this session would you like to create?</p>
        <div class="form-control mb-4">
          <input type="number" v-model="duplicateCount" min="1" max="50" class="input input-bordered w-full" />
        </div>
        <div class="modal-action">
          <button class="btn btn-ghost" @click="closeDuplicateModal">Cancel</button>
          <button class="btn btn-primary" @click="confirmDuplicate">Duplicate</button>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button @click="closeDuplicateModal">close</button>
      </form>
    </dialog>

  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from "vue"
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/authStore'
import { getEvent, getSessions, updateEvent } from '@/services/event.js'
// Import date-fns & TZ package
import { format, addDays, addWeeks, addMonths, addYears } from "date-fns"
import { TZDate } from "@date-fns/tz"

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const sessionModalRef = ref(null)

// Computed user timezone fallback
const userTimezone = computed(() => {
  return authStore.user?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone
})

// --- STATE ---
const event = ref({
  title: "",
  location: "",
  description: "",
  is_draft: false
})

const limitEnabled = ref(false)
const limit = ref(1)

const sessions = ref([])
const originalSessions = ref([]) // Used to track which sessions were deleted

// Pagination State
const currentPage = ref(1)
const itemsPerPage = 4

// Duplicate State
const duplicateModalRef = ref(null)
const sessionToDuplicate = ref(null)
const duplicateCount = ref(1)

// Form state for modal
const isEditing = ref(false)
const editingIndex = ref(null)
const backupSession = ref(null)

const newSession = ref({
  start: "",
  end: "",
  capacity: null,
  location: "",
  description: ""
})

const repeatEndEnabled = ref(false)
const repeatEnd = ref({ type: "never", date: "", count: null })
const repeatsChoose = ref({ type: "Does not repeat", interval: "" })

// --- COMPUTED (Pagination) ---
const totalPages = computed(() => Math.max(1, Math.ceil(sessions.value.length / itemsPerPage)))

const paginatedSessions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sessions.value.slice(start, start + itemsPerPage)
})

const getGlobalIndex = (index) => {
  return (currentPage.value - 1) * itemsPerPage + index
}

watch(() => sessions.value.length, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = Math.max(1, totalPages.value)
  }
})

// --- LIFECYCLE (DATA HYDRATION) ---
onMounted(async () => {
  const eventId = route.params.event_uuid;
  if (!eventId) return;

  try {
    const data = await getEvent(eventId)

    event.value.title = data.title || "";
    event.value.location = data.location || "";
    event.value.description = data.description || "";
    event.value.is_draft = data.is_draft || false;

    if (data.max_sessions_per_user) {
      limitEnabled.value = true;
      limit.value = data.max_sessions_per_user;
    }

    const sessionsRes = await getSessions(eventId, null, 100) 
    const sessionsData = sessionsRes.items || [];

    const mappedSessions = sessionsData.map(s => {
      // 1. Convert Backend UTC ISO string to the User's Timezone string format expected by datetime-local (yyyy-MM-ddTHH:mm)
      const startStr = s.start_datetime ? format(new TZDate(s.start_datetime, userTimezone.value), "yyyy-MM-dd'T'HH:mm") : "";
      const endStr = s.end_datetime ? format(new TZDate(s.end_datetime, userTimezone.value), "yyyy-MM-dd'T'HH:mm") : "";

      return {
        id: s.id,
        uuid: s.uuid,
        start: startStr,
        end: endStr,
        capacity: s.seat_capacity,
        taken: s.seat_taken,
        location: s.location || "",
        description: s.description || ""
      }
    });

    sessions.value = mappedSessions;
    originalSessions.value = JSON.parse(JSON.stringify(mappedSessions));

  } catch (error) {
    console.error("Failed to load event details:", error);
    alert("Could not load event data. Please ensure you have permission to edit this event.");
  }
})

// --- WATCHERS ---
watch(limitEnabled, (val) => {
  if (!val) limit.value = 1
  else limit.value = null
})

// --- MODAL CONTROLS ---
const openAddModal = () => {
  resetForm()
  isEditing.value = false
  sessionModalRef.value.showModal()
}

const openEditModal = (s, globalIndex) => {
  newSession.value = { ...s }
  isEditing.value = true
  editingIndex.value = globalIndex
  backupSession.value = { ...s }
  
  sessions.value.splice(globalIndex, 1)
  sessionModalRef.value.showModal()
}

const closeSessionModal = () => {
  if (isEditing.value && backupSession.value) {
    sessions.value.splice(editingIndex.value, 0, backupSession.value)
  }
  sessionModalRef.value.close()
  resetForm()
}

// --- DUPLICATE LOGIC ---
const openDuplicateModal = (s) => {
  sessionToDuplicate.value = s
  duplicateCount.value = 1
  duplicateModalRef.value.showModal()
}

const closeDuplicateModal = () => {
  duplicateModalRef.value.close()
  sessionToDuplicate.value = null
}

const confirmDuplicate = () => {
  if (!sessionToDuplicate.value || duplicateCount.value < 1) return
  
  for (let i = 0; i < duplicateCount.value; i++) {
    const s = sessionToDuplicate.value
    // Strip id and uuid so the backend sees them as new creations
    const clone = { ...s, start: s.start, end: s.end, id: undefined, uuid: undefined }
    sessions.value.push(clone)
  }
  
  closeDuplicateModal()
  
  // Navigate to the newly created items on the last page
  currentPage.value = Math.max(1, Math.ceil(sessions.value.length / itemsPerPage))
}

// --- SESSION ACTIONS ---
function addSession() {
  if (!newSession.value.start || !newSession.value.end) {
    alert("Please provide both start and end times.")
    return
  }
  if (newSession.value.start >= newSession.value.end) {
    alert("End time must be after start time.")
    return
  }

  const type = repeatsChoose.value.type
  const interval = Number(repeatsChoose.value.interval) || 1
  
  // Use TZDate to parse local datetime-local strings as UserTimezone!
  const startDate = new TZDate(newSession.value.start, userTimezone.value)
  const endDate = new TZDate(newSession.value.end, userTimezone.value)

  const addByType = (date) => {
    if (type === "Daily") return addDays(date, interval)
    if (type === "Weekly") return addWeeks(date, interval)
    if (type === "Monthly") return addMonths(date, interval)
    if (type === "Yearly") return addYears(date, interval)
    return date
  }

  const formatLocal = (date) => format(date, "yyyy-MM-dd'T'HH:mm")

  if (type === "Does not repeat") {
    sessions.value.push({
      ...newSession.value,
      start: formatLocal(startDate),
      end: formatLocal(endDate),
    })
  } else {
    let currentStart = startDate
    let currentEnd = endDate
    let i = 0

    while (true) {
      sessions.value.push({
        ...newSession.value,
        start: formatLocal(currentStart),
        end: formatLocal(currentEnd),
        recurring: type
      })
      i++

      if (repeatEndEnabled.value && repeatEnd.value.type === "count") {
        if (repeatEnd.value.count && i >= repeatEnd.value.count) break
      }
      if (repeatEndEnabled.value && repeatEnd.value.type === "date") {
        // Evaluate limit using user Timezone
        const limitDate = new TZDate(repeatEnd.value.date, userTimezone.value)
        if (currentStart >= limitDate) break
      }
      if (i > 100) break 
      
      currentStart = addByType(currentStart)
      currentEnd = addByType(currentEnd)
    }
  }
  
  sessionModalRef.value.close()
  resetForm()
  
  currentPage.value = Math.max(1, Math.ceil(sessions.value.length / itemsPerPage))
}

function saveEdit() {
  if (!newSession.value.start || !newSession.value.end) return alert("Please provide both start and end times.")
  if (newSession.value.start >= newSession.value.end) return alert("End time must be after start time.")
  if (newSession.value.taken > newSession.value.capacity) return alert("Capacity cannot be less than the number of taken seats.")
  
  sessions.value.splice(editingIndex.value, 0, { ...newSession.value })
  sessionModalRef.value.close()
  resetForm()
}

function removeSession(globalIndex) {
  if(confirm("Remove this session?")) {
    sessions.value.splice(globalIndex, 1)
  }
}

function resetForm() {
  newSession.value = { start: "", end: "", capacity: null, location: "", description: "" }
  repeatsChoose.value = { type: "Does not repeat", interval: "" }
  repeatEnd.value = { type: "never", date: "", count: null }
  repeatEndEnabled.value = false
  isEditing.value = false
  editingIndex.value = null
  backupSession.value = null
}

// --- SUBMIT ACTIONS ---
const saveChangesAndLeave = async () => {
  await submit()
  document.getElementById("my_modal_3")?.close()
}

const submit = async () => {
  const eventId = route.params.event_uuid;
  
  const sessionsPayload = [];
  const currentUuids = new Set(sessions.value.map(s => s.uuid).filter(Boolean));

  // 1. Mark Deleted Sessions
  originalSessions.value.forEach(os => {
    if (!currentUuids.has(os.uuid)) {
      sessionsPayload.push({
        action: "delete",
        session_uuid: os.uuid
      });
    }
  });

  // 2. Mark Created and Updated Sessions
  sessions.value.forEach(s => {
    
    // Parse the local strings back out as TZDate bound to the User Timezone
    // and extract the correct UTC ISOString for the backend!
    const data = {
      start_datetime: s.start ? new TZDate(s.start, userTimezone.value).toISOString() : null,
      end_datetime: s.end ? new TZDate(s.end, userTimezone.value).toISOString() : null,
    };
    
    if (s.capacity) data.seat_capacity = Number(s.capacity);
    if (s.location) data.location = s.location;
    if (s.description) data.description = s.description;

    if (s.uuid) {
      sessionsPayload.push({
        action: "update",
        session_uuid: s.uuid,
        data: data
      });
    } else {
      sessionsPayload.push({
        action: "create",
        data: data
      });
    }
  });

  const payload = {
    title: event.value.title,
    location: event.value.location || "",
    description: event.value.description || "",
    max_sessions_per_user: limitEnabled.value && limit.value ? Number(limit.value) : null,
    is_draft: event.value.is_draft,
    sessions: sessionsPayload
  }

  try {
    await updateEvent(eventId, payload);
    router.push('/events')
  } catch (err) {
    console.error("Update event failed:", err)
    if (err.response && err.response.status === 400) {
      alert("Validation Error: Please check your input and try again.\nDetails: " + JSON.stringify(err.response.data));
      return;
    }
    
    let errorMsg = "Failed to save changes.";
    if (err.response && err.response.data && err.response.data.detail) {
      errorMsg += "\nDetails: " + JSON.stringify(err.response.data.detail);
    }
    alert(errorMsg);
  }
}

const goToDashboard = () => router.push("/events")
const goToPreviousPage = () => window.history.length > 1 ? router.back() : router.push("/events")

// --- FORMATTERS ---
// Format the input strings ("yyyy-MM-dd'T'HH:mm") representing userTimezone directly into readable pieces
function formatDay(dateStr) { 
  if(!dateStr) return '';
  return format(new TZDate(dateStr, userTimezone.value), 'd');
}
function formatMonth(dateStr) { 
  if(!dateStr) return '';
  return format(new TZDate(dateStr, userTimezone.value), 'MMM').toUpperCase(); 
}
function formatTime(dateStr) { 
  if(!dateStr) return '';
  return format(new TZDate(dateStr, userTimezone.value), 'hh:mm a'); 
}
</script>