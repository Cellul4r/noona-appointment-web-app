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
          <span v-if="event.is_draft" class="badge badge-warning gap-1 text-xs font-semibold ml-1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-3"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" /></svg>
            Draft
          </span>
          <span v-else class="badge badge-success gap-1 text-xs font-semibold ml-1">
            <span class="w-1.5 h-1.5 rounded-full bg-current animate-pulse"></span>
            Active
          </span>
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

        <!-- Notify Participants Modal -->
        <dialog id="notify_participants_modal" class="modal">
          <div class="modal-box">
            <h3 class="text-lg font-bold">Save Changes</h3>
            <p class="py-4">
              You have made changes to this event. Would you like to notify participants about these updates?
            </p>
            <div class="flex flex-col gap-3">
              <button type="button" class="btn btn-outline" @click="closeNotifyModal">
                Cancel
              </button>
              <button type="button" class="btn" @click="proceedWithoutNotify">
                Save Without Notifying
              </button>
              <button type="button" class="btn btn-primary" @click="proceedWithNotify">
                Save & Notify Participants
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
            <input type="checkbox" v-model="limitEnabled" class="toggle toggle-primary" />
            <span class="text-md font-normal flex-1">
              Max sessions per participant
              <span class="text-sm opacity-40 font-normal">(optional)</span>
            </span>
            <div class="flex flex-wrap items-center gap-x-1">
              <div class="w-px h-8 bg-base-300"></div>
              <div class="flex items-center gap-2">
                <input type="number" pattern="[0-9]*" v-model="limit" :min="limitEnabled ? 1 : undefined"
                  :disabled="!limitEnabled" class="input input-bordered w-14 validator" />
              </div>
            </div>
          </div>
        </div>


        <!-- Timezone -->
        <div class="flex items-center justify-center p-1 rounded-lg mt-4
            bg-blue-50 dark:bg-blue-900/20
            text-blue-700 dark:text-blue-300
            border border-blue-100 dark:border-blue-800
            text-xs font-medium">
          <span class="text-xs mr-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-5">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
            </svg>

          </span>
          All times are in {{ userTimezone }}
        </div>



          <!-- Session Management Component -->
          <EditEventSession 
            ref="sessionComponentRef"
            :event-id="route.params.event_uuid"
            :event-location="event.location"
            :user-timezone="userTimezone"
            :sessions="sessions"
            @sessions-change="sessions = $event"
          />

        </div>

        <div class="flex gap-2 justify-end pt-6 pb-6 pr-6">
          <div class="pl-4"></div>
          <button @click="onDeleteEvent" :disabled="deletingEvent" class="btn btn-outline btn-error">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.166L18.16 19.673A2.25 2.25 0 0 1 15.916 21.75H8.084a2.25 2.25 0 0 1-2.245-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
            {{ deletingEvent ? 'Deleting...' : 'Delete Event' }}
          </button>
          <div class="flex-1"></div>
          <button @click="goToPreviousPage" class="btn btn-ghost">
            Cancel
          </button>
          <button @click="submit" :class="event.is_draft ? 'btn-outline border-base-300' : 'btn-primary'" class="btn px-8">
            {{ event.is_draft ? 'Save Draft' : 'Save Changes' }}
          </button>
          <button v-if="event.is_draft" @click="publish" class="btn btn-primary px-8 shadow-sm shadow-primary/20">
            Publish
          </button>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from "vue"
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/authStore'
import { getEvent, updateEvent, deleteEvent } from '@/services/event.js'
import EditEventSession from '@/components/session/EditEventSession.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const sessionComponentRef = ref(null)

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
const maxSessionsPerUserOriginal = ref(null)
const pendingSubmitWithNotify = ref(false)
const deletingEvent = ref(false)

// Store original values for change detection
const originalEvent = ref({
  title: "",
  location: "",
  description: "",
  max_sessions_per_user: null
})

const sessions = ref([])

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

    // Store original values for comparison
    originalEvent.value.title = data.title || "";
    originalEvent.value.location = data.location || "";
    originalEvent.value.description = data.description || "";
    originalEvent.value.max_sessions_per_user = data.max_sessions_per_user;

    if (data.max_sessions_per_user !== null && data.max_sessions_per_user !== undefined) {
      limitEnabled.value = true;
      limit.value = Number(data.max_sessions_per_user);
      maxSessionsPerUserOriginal.value = Number(data.max_sessions_per_user);
    } else {
      limitEnabled.value = false;
      limit.value = 1;
      maxSessionsPerUserOriginal.value = null;
    }

    // Load sessions via component
    if (sessionComponentRef.value?.loadSessions) {
      await sessionComponentRef.value.loadSessions();
    }

  } catch (error) {
    console.error("Failed to load event details:", error);
    alert("Could not load event data. Please ensure you have permission to edit this event.");
  }
})

// --- WATCHERS ---
watch(limitEnabled, (val) => {
  if (!val) {
    limit.value = 1
    return
  }

  if (limit.value == null || Number(limit.value) < 1) {
    limit.value = 1
  }
})

// --- SUBMIT ACTIONS ---
const saveChangesAndLeave = async () => {
  await submit()
  document.getElementById("my_modal_3")?.close()
}

const publish = async () => {
  if (!confirm("Are you sure you want to publish this event? It will become visible to users.")) return;
  event.value.is_draft = false;
  await submit();
}

const closeNotifyModal = () => {
  document.getElementById("notify_participants_modal")?.close()
}

const proceedWithoutNotify = () => {
  pendingSubmitWithNotify.value = false
  closeNotifyModal()
  submitPayload()
}

const proceedWithNotify = () => {
  pendingSubmitWithNotify.value = true
  closeNotifyModal()
  submitPayload()
}

const submit = async () => {
  // Check if any changes have been made
  const eventChanged = 
    event.value.title !== originalEvent.value.title ||
    event.value.location !== originalEvent.value.location ||
    event.value.description !== originalEvent.value.description;
  
  const newLimit = limitEnabled.value && limit.value ? Number(limit.value) : null
  const limitChanged = originalEvent.value.max_sessions_per_user !== newLimit;
  
  const sessionsChanged = sessions.value.some(s => s.action === "create" || s.action === "update" || s.action === "delete");
  
  const hasAnyChanges = eventChanged || limitChanged || sessionsChanged;
  
  // Show notification modal if any changes were made
  if (hasAnyChanges) {
    document.getElementById("notify_participants_modal")?.showModal()
    return
  }

  pendingSubmitWithNotify.value = false
  await submitPayload()
}
const submitPayload = async () => {
  const eventId = route.params.event_uuid;
  
  // Track if any sessions have been modified
  const sessionsWithActions = sessions.value.filter(s => s.action === "create" || s.action === "update" || s.action === "delete");
  const hasSessionChanges = sessionsWithActions.length > 0;
  
  const sessionsPayload = sessions.value.map(s => {
    // Only include sessions with explicit actions
    if (!s.action) return null;

    const normalizedCapacity =
      s.capacity === null || s.capacity === undefined || s.capacity === ""
        ? null
        : Number(s.capacity);

    // s.start & s.end are actual Date objects, .toISOString() returns UTC
    const data = {
      start_datetime: s.start ? s.start.toISOString() : null,
      end_datetime: s.end ? s.end.toISOString() : null,
      seat_capacity: normalizedCapacity,
    };
    
    if (s.location) data.location = s.location;
    if (s.description) data.description = s.description;

    if (s.action === "delete") {
      return {
        action: "delete",
        session_uuid: s.uuid
      };
    } else if (s.action === "update") {
      return {
        action: "update",
        session_uuid: s.uuid,
        data: data
      };
    } else if (s.action === "create") {
      return {
        action: "create",
        data: data
      };
    }
  }).filter(Boolean); // Remove null entries

  const payload = {
    title: event.value.title,
    location: event.value.location || "",
    description: event.value.description || "",
    max_sessions_per_user: limitEnabled.value && limit.value ? Number(limit.value) : null,
    is_draft: event.value.is_draft,
    sessions: hasSessionChanges ? sessionsPayload : null
  }

  try {
    await updateEvent(eventId, payload, pendingSubmitWithNotify.value);
    router.push('/event/overview/' + eventId);
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

const onDeleteEvent = async () => {
  if (deletingEvent.value) return

  const confirmed = window.confirm('Delete this event? This action cannot be undone.')
  if (!confirmed) return

  deletingEvent.value = true
  try {
    await deleteEvent(route.params.event_uuid)
    router.replace({ name: 'AllEvents' })
  } catch (err) {
    console.error('Failed to delete event:', err)
    alert('Failed to delete event.')
  } finally {
    deletingEvent.value = false
  }
}

const goToPreviousPage = () => window.history.length > 1 ? router.back() : router.push("/events")
</script>