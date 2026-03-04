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

        <div class="flex gap-2 justify-end pt-4">
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
import { getEvent, updateEvent } from '@/services/event.js'
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

    if (data.max_sessions_per_user) {
      limitEnabled.value = true;
      limit.value = data.max_sessions_per_user;
    }

    // Load sessions via component
    if (sessionComponentRef.value?.loadSessions) {
      await sessionComponentRef.value.loadSessions(null);
    }

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

const submit = async () => {
  const eventId = route.params.event_uuid;
  
  const sessionsPayload = sessions.value.map(s => {
    // s.start & s.end are actual Date objects, .toISOString() returns UTC
    const data = {
      start_datetime: s.start ? s.start.toISOString() : null,
      end_datetime: s.end ? s.end.toISOString() : null,
    };
    
    if (s.capacity) data.seat_capacity = Number(s.capacity);
    if (s.location) data.location = s.location;
    if (s.description) data.description = s.description;

    if (s.uuid) {
      return {
        action: "update",
        session_uuid: s.uuid,
        data: data
      };
    } else {
      return {
        action: "create",
        data: data
      };
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

const goToPreviousPage = () => window.history.length > 1 ? router.back() : router.push("/events")
</script>