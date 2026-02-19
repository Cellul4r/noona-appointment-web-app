<template>
  <div class="drawer lg:drawer-open font-display bg-base-200 min-h-screen">
    <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
    
    <!-- MAIN CONTENT -->
    <div class="drawer-content flex flex-col items-center justify-start">
      
      <!-- MOBILE NAVBAR -->
      <div class="w-full navbar bg-base-100 lg:hidden shadow-sm z-20">
        <div class="flex-none">
          <label for="my-drawer-2" class="btn btn-square btn-ghost">
            <span class="material-symbols-outlined">menu</span>
          </label>
        </div>
        <div class="flex-1">
          <a class="btn btn-ghost text-xl">My Events</a>
        </div>
      </div>

      <main class="w-full p-6 lg:p-10 max-w-7xl">
        
        <!-- HEADER -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div>
            <h1 class="text-3xl font-bold text-base-content">My Events</h1>
            <p class="text-base-content/60 mt-1">Manage and track your scheduled sessions</p>
          </div>
          <button @click="createEvent" class="btn btn-primary gap-2 shadow-lg hover:scale-105 transition-transform">
            <span class="material-symbols-outlined text-lg">ผมรักในหลวง</span>
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
              <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-base-content/50 pointer-events-none">search</span>
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
        <div v-if="loading && events.length === 0" class="flex justify-center py-20">
          <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>

        <div v-else-if="filteredEvents.length === 0" class="text-center py-20 opacity-60">
          <span class="material-symbols-outlined text-6xl mb-4">ไม่เจออีเว้นท์</span>
          <p class="text-lg">No events found matching your criteria.</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6" id="scroll-container">
          <div 
            v-for="event in filteredEvents" 
            :key="event.share_uuid"
            class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-300 border border-base-200 group"
          >
            <!-- Card Image -->
            <figure class="relative h-48 overflow-hidden">
              <img 
                :src="`https://picsum.photos/seed/${event.share_uuid}/600/400`" 
                alt="Event banner" 
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-80"></div>
              
              <!-- Badges -->
              <div class="absolute top-3 left-3 flex gap-2">
                <div 
                  class="badge gap-1 border-none font-medium shadow-sm"
                  :class="event.is_draft ? 'badge-warning text-warning-content' : 'badge-success text-success-content'"
                >
                  {{ event.is_draft ? 'Draft' : 'Published' }}
                </div>
              </div>
            </figure>

            <div class="card-body p-6">
              <h2 class="card-title text-xl font-bold line-clamp-1" :title="event.title">
                {{ event.title }}
              </h2>
              
              <div class="flex items-center gap-1.5 text-sm text-base-content/70 mt-1">
                <span class="material-symbols-outlined text-lg">Location:</span>
                <span class="material-symbols-outlined text-lg">{{ event.location || 'Online / TBD' }}</span>
              </div>

              <p class="text-sm text-base-content/60 mt-3 line-clamp-2 h-10">
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
                  <span class="font-semibold text-base-content">{{ event.host?.full_name || 'Unknown' }}</span>
                </div>
              </div>

              <div class="card-actions flex gap-2 mt-4">
                <button 
                  v-if="event.is_draft"
                  class="btn btn-primary flex-1 btn-sm"
                >
                  Resume Editing
                </button>
                <button 
                  v-else
                  class="btn btn-outline flex-1 btn-sm hover:btn-primary"
                >
                  View Details
                </button>
                
                <button 
                  @click="copyLink(event.share_uuid)"
                  class="btn btn-square btn-sm btn-ghost bg-base-200 hover:bg-primary hover:text-white transition-colors tooltip"
                  data-tip="Copy Link"
                  :disabled="event.is_draft"
                >
                  <span class="material-symbols-outlined text-lg">link</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- LOAD MORE -->
        <div v-if="nextCursor" class="flex justify-center mt-10">
          <button 
            @click="loadMore" 
            :disabled="loading"
            class="btn btn-wide"
          >
            <span v-if="loading" class="loading loading-spinner"></span>
            {{ loading ? 'Loading...' : 'Load More Events' }}
          </button>
        </div>

      </main>
    </div>

    <!-- SIDEBAR DRAWER -->
    <div class="drawer-side z-30">
      <label for="my-drawer-2" class="drawer-overlay"></label> 
      <aside class="menu p-4 w-72 min-h-full bg-base-100 border-r border-base-200 text-base-content flex flex-col">
        <!-- User Info -->
        <div class="flex items-center gap-4 mb-8 px-2 mt-2">
          <div class="avatar placeholder">
            <div class="bg-neutral text-neutral-content rounded-full w-12 ring ring-primary ring-offset-base-100 ring-offset-2">
              <span class="text-xl font-bold">{{ userInitials }}</span>
            </div>
          </div>
          <div>
            <div class="font-bold text-lg">{{ user?.full_name || 'Guest User' }}</div>
            <div class="text-xs opacity-60">Host Admin</div>
          </div>
        </div>

        <!-- Navigation -->
        <ul class="menu w-full gap-2 font-medium">
          <li v-for="link in navLinks" :key="link.name">
            <a 
              :class="{ 'active': link.active }"
              class="flex gap-3 py-3"
            >
              <span class="material-symbols-outlined">{{ link.icon }}</span>
              {{ link.name }}
            </a>
          </li>
        </ul>

        <div class="mt-auto border-t border-base-200 pt-4">
          <button @click="handleLogout" class="btn btn-ghost w-full justify-start gap-3 text-error hover:bg-error/10">
            <span class="material-symbols-outlined">logout</span>
            Log Out
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'vue-router';
import axios from 'axios';

// --- STATE ---
const authStore = useAuthStore();
const router = useRouter();
const user = computed(() => authStore.user);
const events = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const nextCursor = ref(null);
const errorMsg = ref(null);

// Filters
const currentScope = ref('all'); 
const statusFilter = ref('all'); 

const scopeTabs = [
  { label: 'All Events', value: 'all' },
  { label: 'Hosted', value: 'hosted' },
  { label: 'Registered', value: 'joined' }
];

const navLinks = [
  { name: 'Dashboard', active: false },
  { name: 'My Events',active: true },
  { name: 'Calendar', active: false },
  { name: 'Settings', active: false },
];

const userInitials = computed(() => {
  const name = user.value?.full_name || 'Guest';
  return name.substring(0, 2).toUpperCase();
});

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

    const baseUrl = 'http://localhost:56733'; 
    const response = await axios.get(`${baseUrl}/events/`, { 
      params,
      headers: { Authorization: `Bearer ${authStore.token}` },
      timeout: 5000 
    });

    if (reset) {
      events.value = response.data.items;
    } else {
      events.value = [...events.value, ...response.data.items];
    }
    
    nextCursor.value = response.data.next_page;
  } catch (error) {
    console.error("Failed to fetch events:", error);
    if (error.code === 'ERR_NETWORK') {
      errorMsg.value = "Cannot connect to server. Is the backend running on port 56733?";
    } else {
      errorMsg.value = "Failed to load events.";
    }
  } finally {
    loading.value = false;
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

// --- EVENT HANDLERS ---
const handleSearch = () => {
  if (window.searchTimeout) clearTimeout(window.searchTimeout);
  window.searchTimeout = setTimeout(() => {
    fetchEvents(true);
  }, 400);
};

const changeScope = (scope) => {
  currentScope.value = scope;
  fetchEvents(true);
};

const loadMore = () => {
  if (nextCursor.value) fetchEvents(false);
};

const createEvent = () => {
  // router.push('/events/create');
  console.log("Create event clicked");
};

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

const copyLink = (uuid) => {
  const link = `${window.location.origin}/vote/${uuid}`;
  navigator.clipboard.writeText(link);
  alert(`Link copied: ${link}`);
};

const formatDate = (dateString) => {
  if (!dateString) return 'Just now';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' }).format(date);
};

// --- LIFECYCLE ---
onMounted(() => {
  fetchEvents(true);
});
</script>