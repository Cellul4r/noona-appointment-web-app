<template>
  <div class="drawer lg:drawer-open font-display bg-base-200 min-h-screen">
    <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
    
    <!-- MAIN CONTENT -->
    <div class="drawer-content flex flex-col items-center justify-start">

      <main class="w-full p-6 lg:p-10 max-w-7xl">
        
        <!-- HEADER -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h1 class="text-3xl font-bold text-base-content">
              My Events
              <span v-if="events.length > 0" class="text-lg font-normal text-base-content/50 ml-2">({{ filteredEvents.length }})</span>
            </h1>
            <p class="text-base-content/60 mt-1">Manage and track your scheduled sessions</p>
          </div>
          <button @click.prevent="createEvent" class="btn btn-primary gap-2 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-[1.02] active:scale-95">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Create New Event
          </button>
        </div>

        <!-- CONTROLS & FILTERS -->
        <div class="bg-base-100 p-4 rounded-box shadow-sm mb-8 flex flex-col lg:flex-row gap-4 justify-between items-center">
          
          <!-- Scope Tabs -->
          <div class="tabs tabs-boxed bg-base-200 p-1">
            <a 
              v-for="tab in scopeTabs" 
              :key="tab.value"
              @click="changeScope(tab.value)"
              :class="['tab transition-all duration-200 cursor-pointer', currentScope === tab.value ? 'tab-active font-semibold shadow-sm' : '']"
            >
              {{ tab.label }}
            </a>
          </div>

          <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto">
            <!-- Status Filter -->
            <select v-model="statusFilter" class="select select-bordered w-full sm:w-auto focus:select-primary cursor-pointer">
              <option value="all">All Statuses</option>
              <option value="draft">Drafts Only</option>
              <option value="published">Published Only</option>
            </select>

            <!-- Search -->
            <div class="relative w-full sm:w-64">
              <input 
                v-model="searchQuery" 
                @input="handleSearch"
                type="text" 
                placeholder="Search events..." 
                class="input input-bordered w-full pr-10 focus:input-primary" 
              />
              <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-base-content/50 pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
              </span>
            </div>
          </div>
        </div>

        <!-- ERROR MESSAGE -->
        <div v-if="errorMsg" class="alert alert-error mb-6 shadow-sm">
          <span class="material-symbols-outlined">error</span>
          <span>{{ errorMsg }}</span>
          <button @click="fetchEvents(true)" class="btn btn-xs btn-ghost">Retry</button>
        </div>

        <!-- EVENTS GRID -->
        <div v-if="loading && events.length === 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <div v-for="n in 6" :key="n" class="card bg-base-100 shadow-md border border-base-200 border-t-4 ">
            <div class="card-body p-6 gap-4">
              <div class="flex justify-between items-start">
                <div class="skeleton h-6 w-3/4"></div>
                <div class="skeleton h-5 w-16 rounded-full"></div>
              </div>
              <div class="skeleton h-4 w-1/2"></div>
              <div class="space-y-2">
                <div class="skeleton h-3 w-full"></div>
                <div class="skeleton h-3 w-5/6"></div>
              </div>
              <div class="divider my-1"></div>
              <div class="flex justify-between">
                <div class="skeleton h-4 w-24"></div>
                <div class="skeleton h-4 w-24"></div>
              </div>
              <div class="flex gap-2 mt-2">
                <div class="skeleton h-8 flex-1 rounded-btn"></div>
                <div class="skeleton h-8 w-8 rounded-btn"></div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="filteredEvents.length === 0" class="flex flex-col items-center justify-center py-20 px-4">
          <div class="bg-base-100 rounded-full p-6 mb-6 shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="w-16 h-16 text-base-content/25">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-base-content mb-2">No events found</h3>
          <p class="text-base-content/50 text-center max-w-md mb-6">
            {{ searchQuery || statusFilter !== 'all' ? 'Try adjusting your search or filters.' : "You haven't created any events yet. Get started!" }}
          </p>
          <button v-if="!searchQuery && statusFilter === 'all'" @click="createEvent" class="btn btn-primary gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Create Your First Event
          </button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6" id="scroll-container">
          <div 
            v-for="event in paginatedEvents" 
            :key="event.share_uuid"
            :class="[
              'card rounded-2xl shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-t-4 group',
              event.is_draft ? 'bg-base-300 border-base-content/10' : 'bg-base-100 border-base-200'
            ]"
          >
            <div class="card-body p-6">
              <div class="flex items-start justify-between gap-2">
                <h2 class="card-title text-xl font-bold line-clamp-3 break-words flex-1" :title="event.title">
                  {{ event.title }}
                </h2>
                <div v-if="event.is_draft" class="badge badge-ghost gap-1 shrink-0 opacity-80">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>
                  Draft
                </div>
                <div v-else-if="endedEvents[event.share_uuid]" class="badge badge-ghost gap-1 shrink-0 opacity-70">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                  Ended
                </div>
                <div v-else-if="checkingEnded[event.share_uuid]" class="skeleton h-5 w-14 rounded-full shrink-0"></div>
                <div v-else class="badge badge-success gap-1 shrink-0">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-50 inline-block animate-pulse"></span>
                  Active
                </div>
              </div>
              
              <div class="flex items-center gap-1.5 text-sm text-base-content/70 mt-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 shrink-0">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                </svg>

                <span class="material-symbols-outlined text-lg">{{ event.location || 'Online / TBD' }}</span>
              </div>

              <p class="text-sm text-base-content/60 line-clamp-4">
                {{ event.description || 'No description provided.' }}
              </p>
              
              <div class="divider my-2"></div>

              <div class="flex justify-between items-end text-xs text-base-content/50">
                <div 
                  class="flex flex-col gap-1 tooltip tooltip-bottom" 
                  :data-tip="event.created_at ? 'Created: ' + formatDate(event.created_at) : 'Created: Unknown'"
                >
                  <span>Last Edited</span>
                  <span class="font-semibold text-base-content">{{ formatDate(event.updated_at) }}</span>
                </div>
                <div class="flex flex-col gap-1 text-right">
                  <span>Host</span>
                  <span class="font-semibold text-base-content">
                    {{ user?.id && user.id == event.host?.id ? `${event.host.full_name} (You)` : (event.host?.full_name || 'Unknown') }}
                  </span>
                </div>
              </div>

              <div class="card-actions flex gap-2 mt-4">
                <button 
                  v-if="event.is_draft"
                  class="btn flex-1 btn-sm rounded-xl bg-base-200 border-base-300 text-base-content hover:bg-base-200"
                  @click="editEvent(event)"
                >
                  Edit
                </button>
                <button 
                  v-else
                  class="btn btn-primary flex-1 btn-sm rounded-xl"
                  @click="viewDetails(event)"
                >
                  View Details
                </button>
                
                <button 
                  @click="copyLink(event.share_uuid)"
                  class="btn btn-square btn-sm btn-ghost hover:bg-primary hover:text-white transition-colors tooltip"
                  data-tip="Copy Link"
                  :disabled="event.is_draft"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- LOAD MORE -->
        <div v-if="filteredEvents.length > visibleCount || nextCursor" class="flex justify-center mt-10">
          <button 
            @click="loadMore" 
            :disabled="loading"
            class="btn btn-wide"
          >
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ loading ? 'Loading...' : 'Load More' }}
          </button>
        </div>

        <!-- TOAST NOTIFICATION -->
        <Transition name="toast-slide">
          <div v-if="toastMsg" class="fixed bottom-6 right-6 z-50">
            <div class="alert alert-success shadow-lg gap-2 pr-4">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 shrink-0">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <span class="text-sm font-medium">{{ toastMsg }}</span>
            </div>
          </div>
        </Transition>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'vue-router';
import { fetchUserSettings } from '@/services/user.js';
import { getAllEvents, getEventOverview, getSessions } from '@/services/event.js';

// --- STATE ---
const authStore = useAuthStore();
const router = useRouter();
const user = computed(() => authStore.user);
const events = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const nextCursor = ref(null);
const errorMsg = ref(null);
const toastMsg = ref(null);
const endedEvents = ref({}); // { [share_uuid]: true } for events where all sessions have ended
const checkingEnded = ref({}); // { [share_uuid]: true } while ended-check is in flight

// Filters
const currentScope = ref('all'); 
const statusFilter = ref('all'); 

const scopeTabs = [
  { label: 'All Events', value: 'all' },
  { label: 'Hosted', value: 'hosted' },
  { label: 'Registered', value: 'joined' }
];

// --- PAGINATION (client-side 'Load More') ---
const eventsPerPage = 9;
const visibleCount = ref(eventsPerPage);

// --- API ACTIONS ---
const fetchEvents = async (reset = false) => {
  // Prevent double-loading unless resetting (switching tabs)
  if (loading.value && !reset) return; 
  
  loading.value = true;
  errorMsg.value = null;

  try {
    const params = {
      scope: currentScope.value,
      size: 12,
      ...(searchQuery.value && { title: searchQuery.value }),
      ...(reset ? {} : { cursor: nextCursor.value })
    };

    const response = await getAllEvents(params, authStore.token);

    if (reset) {
      events.value = response.items;
      endedEvents.value = {};
      checkingEnded.value = {};
      // reset visible count when we reset the list
      visibleCount.value = eventsPerPage;
    } else {
      events.value = [...events.value, ...response.items];
    }
    
    nextCursor.value = response.next_page;

    // Check ended status in the background (non-blocking)
    checkEndedStatus(response.items);
  } catch (error) {
    console.error("Failed to fetch events:", error);
    if (error.code === 'ERR_NETWORK') {
      errorMsg.value = "Cannot connect to server. Please check your network or try again later.";
    } else if (error.response) {
      errorMsg.value = `Error ${error.response.status}: ${error.response.data.detail || 'Failed to load events.'}`;
    } else {
      errorMsg.value = "An unexpected error occurred while loading events.";
    }
  } finally {
    loading.value = false;
  }
};

// Check which published events have all sessions ended (no upcoming sessions)
const checkEndedStatus = async (eventList) => {
  const publishedEvents = eventList.filter(e => !e.is_draft);
  // Mark all published events as "checking" before any API calls
  publishedEvents.forEach(e => { checkingEnded.value[e.share_uuid] = true; });
  checkingEnded.value = { ...checkingEnded.value };

  const checks = publishedEvents.map(async (event) => {
    try {
      // Fetch with upcoming_only=true and size=1: if 0 items, all sessions ended
      const res = await getSessions(event.share_uuid, null, 1, true);
      if (res.items.length === 0) {
        endedEvents.value[event.share_uuid] = true;
      }
    } catch {
      // silently ignore — badge will default to "Active"
    } finally {
      delete checkingEnded.value[event.share_uuid];
    }
  });
  await Promise.all(checks);
  // Trigger reactivity
  endedEvents.value = { ...endedEvents.value };
  checkingEnded.value = { ...checkingEnded.value };
};

const loadUserSettings = async () => {
  try {
    const data = await fetchUserSettings();
    if (data) {
      authStore.setUser(data);
    }
  } catch (error) {
    console.error("Failed to fetch user settings:", error);
  }
};

// --- COMPUTED / FILTERS ---
const filteredEvents = computed(() => {
  if (statusFilter.value === 'draft') {
    return events.value.filter(e => e.is_draft);
  }
  if (statusFilter.value === 'published') {
    return events.value.filter(e => !e.is_draft);
  }
  return events.value;
});

// paginated view used by the template (client-side pagination)
const paginatedEvents = computed(() => {
  return filteredEvents.value.slice(0, visibleCount.value);
});

// --- EVENT HANDLERS ---
const handleSearch = () => {
  if (window.searchTimeout) clearTimeout(window.searchTimeout);
  window.searchTimeout = setTimeout(() => {
    // reset visible count and fetch fresh results
    visibleCount.value = eventsPerPage;
    fetchEvents(true);
  }, 400);
};

const changeScope = (scope) => {
  currentScope.value = scope;
  visibleCount.value = eventsPerPage;
  fetchEvents(true);
};

const loadMore = () => {
  // If we have more items already fetched, just increase visible count.
  if (paginatedEvents.value.length < filteredEvents.value.length) {
    visibleCount.value += eventsPerPage;
    return;
  }

  // Otherwise, try to fetch more from the backend if a cursor exists
  if (nextCursor.value) fetchEvents(false);
};

const createEvent = () => {
  router.push({ name: 'CreateEvents' });
};

const editEvent = (evt) => {
  router.push({ name: 'EditEvent', params: { event_uuid: evt.share_uuid } });
};

const copyLink = (uuid) => {
  const link = `${window.location.origin}/event/overview/${uuid}`;
  navigator.clipboard.writeText(link);
  toastMsg.value = 'Event link copied to clipboard!';
  setTimeout(() => { toastMsg.value = null; }, 2500);
};

// when user clicks the 'View Details' button, fetch overview then navigate
const viewDetails = async (evt) => {
  try {
    // prefetch the overview data (could be used for caching or validation)
    await getEventOverview(evt.share_uuid);
  } catch (error) {
    console.error("Failed to load event overview:", error);
    // we still navigate even on error, user overview page may handle its own fetch
  }
  router.push({ name: 'EventOverview', params: { event_uuid: evt.share_uuid } });
};

const formatDate = (dateString) => {
  if (!dateString) return 'Just now';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' }).format(date);
};

// --- LIFECYCLE ---
onMounted(() => {
  fetchEvents(true);
  loadUserSettings();
});
</script>

<style scoped>
/* Toast slide-in animation */
.toast-slide-enter-active {
  transition: all 0.3s ease-out;
}
.toast-slide-leave-active {
  transition: all 0.3s ease-in;
}
.toast-slide-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>