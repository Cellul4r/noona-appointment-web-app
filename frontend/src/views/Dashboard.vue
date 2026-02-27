<template>
  <div class="bg-base-200 min-h-screen font-display pb-20">
    <main class="w-full p-4 lg:p-8 max-w-7xl mx-auto space-y-8">
      
      <!-- ========================================== -->
      <!-- HEADER & TOP ACTIONS                       -->
      <!-- ========================================== -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 bg-base-100 p-6 rounded-box shadow-sm">
        <div>
          <h1 class="text-3xl font-bold text-base-content tracking-tight">Dashboard</h1>
          <p class="text-base-content/60 mt-1">Welcome back, {{ user?.full_name || 'User' }}</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
          
          
          <!-- Create Event -->
          <button @click="goToCreateEvent" class="btn btn-primary gap-2 shadow-sm hover:scale-105 transition-transform w-full sm:w-auto">
            Create Event
          </button>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SECTION 1: MY EVENTS (RECENT)              -->
      <!-- ========================================== -->
      <section class="space-y-4">
        <div class="flex justify-between items-end px-1">
          <h2 class="text-xl font-bold text-base-content flex items-center gap-2">
            Recent Events
          </h2>
          <button @click="router.push('/events')" class="btn btn-sm btn-ghost gap-1 text-primary">
            View All
          </button>
        </div>

        <!-- Loading State for Recent Events -->
        <div v-if="loadingDashboard" class="flex justify-center p-8">
          <span class="loading loading-spinner loading-md text-primary"></span>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="event in recentEvents" :key="event.id" class="card bg-base-100 shadow-sm border border-base-200 hover:shadow-md transition-shadow">
            <div class="card-body p-5 flex flex-col h-full">
              
              <h3 class="card-title text-xl font-bold leading-7 h-[3.5rem] overflow-hidden break-words m-0 p-0" :title="event.title">
                {{ event.title }}
              </h3>
              
              <div class="flex items-center gap-1.5 text-sm text-base-content/70 mt-2">
                <span class="truncate">{{ event.location || 'Online / TBD' }}</span>
              </div>

              <div class="divider my-2 mt-auto"></div>

              <div class="flex justify-between items-end text-xs text-base-content/50">
                <div class="flex flex-col gap-1">
                  <span class="uppercase tracking-wider font-bold opacity-60">Last Edited</span>
                  <span class="font-bold text-base-content text-sm">{{ timeAgo(event.updated_at) }}</span>
                </div>
                <div class="flex flex-col gap-1 text-right">
                  <span class="uppercase tracking-wider font-bold opacity-60">Status</span>
                  <div class="badge badge-sm mt-1 border-none font-bold" :class="event.is_draft ? 'bg-warning/20 text-warning-content' : 'bg-success/20 text-success-content'">
                    {{ event.is_draft ? 'Draft' : 'Active' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="recentEvents.length === 0" class="col-span-3 text-center py-6 text-base-content/50 bg-base-100 rounded-box border border-base-200">
            No recent events found.
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- SECTION 2: WAIT LIST SESSIONS              -->
      <!-- ========================================== -->
      <section class="bg-base-100 rounded-box shadow-sm border border-base-200 overflow-hidden">
        <div class="p-5 border-b border-base-200 bg-base-100 flex items-center gap-2">
          <h2 class="text-lg font-bold">Wait List Sessions</h2>
        </div>
        
        <div class="overflow-x-auto">
          <table class="table table-zebra w-full">
            <thead class="bg-base-200/50">
              <tr>
                <th>Time</th>
                <th>Event</th>
                <th>Host</th>
                <th>Status</th>
                <th class="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingDashboard">
                <td colspan="5" class="text-center py-8"><span class="loading loading-spinner text-primary"></span></td>
              </tr>
              <tr v-else-if="waitlistSessions.length === 0">
                <td colspan="5" class="text-center py-8 text-base-content/50">No waitlisted sessions at this time.</td>
              </tr>
              <tr v-for="session in paginatedWaitlist" :key="session.id">
                <td class="whitespace-nowrap">{{ formatDateTimeRange(session.start_time, session.end_time) }}</td>
                <td>
                  <div class="flex items-center gap-2">
                    <span class="font-medium">{{ session.event_title }}</span>
                    <button @click="goToOverview(session.event_uuid)" class="btn btn-xs btn-circle btn-ghost tooltip" data-tip="Go to Overview">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                      </svg>
                    </button>
                  </div>
                </td>
                <td>
                  <div class="flex items-center gap-2">
                    <div class="avatar placeholder">
                      <div class="bg-neutral text-neutral-content rounded-full w-6">
                        <img :src="getAvatar()" alt="Profile Image">
                      </div>
                    </div>
                    <span class="font-medium">
                      {{ user?.id && user.id == session.host_id ? 'Me' : session.host_name }}
                    </span>
                  </div>
                </td>
                <td>
                  <div class="badge badge-sm" :class="session.is_filled ? 'badge-warning' : 'badge-success'">
                    {{ session.is_filled ? 'Wait List' : 'Available' }}
                    {{ `(${session.seat_taken}/${session.seat_capacity})` }}
                  </div>
                </td>
                <td class="text-right">
                  <button v-if="!session.is_filled" class="btn btn-sm btn-success text-white">Accept</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="waitlistSessions.length > waitVisible" class="p-3 border-t border-base-200 flex justify-center bg-base-100">
          <button @click="loadMoreSection('waitlist')" class="btn btn-sm btn-wide">Load More</button>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- SECTION 3: CURRENT OR UPCOMING SESSIONS    -->
      <!-- ========================================== -->
      <section class="bg-base-100 rounded-box shadow-sm border border-base-200 overflow-hidden">
        <div class="p-5 border-b border-base-200 bg-base-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div class="flex items-center gap-2">
            <h2 class="text-lg font-bold">Current & Upcoming Sessions</h2>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="table table-zebra w-full">
            <thead class="bg-base-200/50">
              <tr>
                <th>Time</th>
                <th>Event</th>
                <th>Host</th>
                <th>Status</th>
                <th class="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingDashboard">
                <td colspan="5" class="text-center py-8"><span class="loading loading-spinner text-primary"></span></td>
              </tr>
              <tr v-else-if="filteredUpcoming.length === 0">
                <td colspan="5" class="text-center py-8 text-base-content/50">No upcoming sessions found.</td>
              </tr>
              <tr v-for="session in paginatedUpcoming" :key="session.id">
                <td class="whitespace-nowrap">{{ formatDateTimeRange(session.start_time, session.end_time) }}</td>
                <td class="font-medium">{{ session.event_title }}</td>
                <td>
                  <div class="flex items-center gap-2">
                    <div class="avatar placeholder">
                      <div class="bg-neutral text-neutral-content rounded-full w-6">
                        <img :src="getAvatar()" alt="Profile Image">
                      </div>
                    </div>
                    <span class="font-medium">
                      {{ user?.id && user.id == session.host_id ? 'Me' : session.host_name }}
                    </span>
                  </div>
                </td>
                <td>
                  <div class="badge badge-sm" :class="user?.id == session.host_id ? 'badge-primary' : 'badge-success'">
                    {{ user?.id == session.host_id ? 'Host' : 'Confirmed' }}
                  </div>
                </td>
                <td class="text-right">
                  <button @click="goToOverview(session.event_uuid)" class="btn btn-sm btn-outline">
                    View Details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="filteredUpcoming.length > upcomingVisible" class="p-3 border-t border-base-200 flex justify-center bg-base-100">
          <button @click="loadMoreSection('upcoming')" class="btn btn-sm btn-wide">Load More</button>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- SECTION 4: PAST SESSIONS (EXPANDABLE)      -->
      <!-- ========================================== -->
      <section class="bg-base-100 rounded-box shadow-sm border border-base-200 overflow-hidden">
        <div class="p-5 border-b border-base-200 bg-base-100 flex items-center gap-2">
          <h2 class="text-lg font-bold">Past Sessions</h2>
        </div>

        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead class="bg-base-200/50">
              <tr>
                <th>Time</th>
                <th>Event</th>
                <th>Host</th>
                <th class="text-right">Details</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingDashboard">
                <td colspan="4" class="text-center py-8"><span class="loading loading-spinner text-primary"></span></td>
              </tr>
              <tr v-else-if="pastSessions.length === 0">
                <td colspan="4" class="text-center py-8 text-base-content/50">No past sessions available.</td>
              </tr>
              <template v-for="session in paginatedPast" :key="session.id">
                <!-- Main Row -->
                <tr class="hover:bg-base-200/30 transition-colors">
                  <td class="whitespace-nowrap text-base-content/80">{{ formatDateTimeRange(session.start_time, session.end_time) }}</td>
                  <td class="font-medium">{{ session.event_title }}</td>
                  <td>
                    <div class="flex items-center gap-2">
                      <div class="avatar placeholder opacity-80">
                        <div class="bg-neutral text-neutral-content rounded-full w-6">
                          <img :src="getAvatar()" alt="Profile Image">
                        </div>
                      </div>
                      <span class="text-base-content/80">
                        {{ user?.id && user.id == session.host_id ? 'Me' : session.host_name }}
                      </span>
                    </div>
                  </td>
                  <td class="text-right">
                    <button @click="toggleRow(session.id)" class="btn btn-sm btn-circle btn-ghost tooltip tooltip-left" data-tip="View Details">
                      <span>
                        <svg v-if="expandedRows.includes(session.id)" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                        </svg>

                        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                      </span>
                    </button>
                  </td>
                </tr>
                
                <!-- Expanded Child Row -->
                <tr v-if="expandedRows.includes(session.id)" class="bg-base-200/30 border-b border-base-200">
                  <td colspan="4" class="p-0">
                    <div class="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
                      <div>
                        <p class="font-bold text-base-content/60 uppercase tracking-wider text-[10px] mb-1">Location</p>
                        <p class="flex items-center gap-1 font-medium"><span class="material-symbols-outlined text-[16px]">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                        </svg>
                        </span> {{ session.location || 'N/A' }}</p>
                      </div>
                      <div class="md:col-span-2">
                        <p class="font-bold text-base-content/60 uppercase tracking-wider text-[10px] mb-1">Description</p>
                        <p class="italic text-base-content/80">{{ session.description || 'No description provided.' }}</p>
                      </div>
                      <div class="md:col-span-3 pt-2">
                        <p class="font-bold text-base-content/60 uppercase tracking-wider text-[10px] mb-1">Invitation Link</p>
                        <div class="flex items-center gap-2">
                          <a :href="`${session.event_uuid}`" class="link link-primary truncate">{{ `${session.event_uuid}` }}</a>
                          <button @click="copyLink(session.event_uuid)" class="btn btn-xs btn-ghost btn-square">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
        <div v-if="pastSessions.length > pastVisible" class="p-3 border-t border-base-200 flex justify-center bg-base-100">
          <button @click="loadMoreSection('past')" class="btn btn-sm btn-wide">Load More</button>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'vue-router';
import { getUserSessions } from '@/services/session.js';
import { fetchUserSettings } from '@/services/user.js';
import { getAllEvents } from '../services/event';

// --- STATE & SETUP ---
const authStore = useAuthStore();
const router = useRouter();
const user = computed(() => authStore.user);

const loadingDashboard = ref(true);

// Data Arrays
const recentEvents = ref([]);
const waitlistSessions = ref([]);
const upcomingSessions = ref([]);
const pastSessions = ref([]);

// --- PAGINATION per-section ---
const sessionsPageSize = 4;
const waitVisible = ref(sessionsPageSize);
const upcomingVisible = ref(sessionsPageSize);
const pastVisible = ref(sessionsPageSize);

// Filters & UI State
const upcomingSearch = ref('');
const upcomingTimeRange = ref('all');
const expandedRows = ref([]); // Holds IDs of expanded past session rows

// --- API FETCH FUNCTIONS ---
const fetchUserProfile = async () => {
  try {
    const data = await fetchUserSettings();
    if (data) authStore.setUser(data);
  } catch (error) {
    console.error("Failed to fetch profile", error);
  }
};

/**
 * Maps a single SessionWithEventPublic backend object to our frontend UI requirement
 */
const mapSessionData = (s) => {
  return {
    id: s.id,
    event_title: s.event?.title || 'Unknown Event',
    event_uuid: s.event?.share_uuid,
    host_id: s.event?.host?.id,
    host_name: s.event?.host?.full_name || 'Unknown Host',
    start_time: s.start_datetime,
    end_time: s.end_datetime,
    location: s.event?.location,
    description: s.event?.description,
    registration_status: s.registration_status,
    seat_capacity: s.seat_capacity,
    seat_taken: s.seat_taken,
    is_filled: s.seat_taken >= s.seat_capacity
  };
};

const fetchDashboardData = async () => {
  loadingDashboard.value = true;
  try {
    const headers = { Authorization: `Bearer ${authStore.token}` };
    const nowISO = new Date().toISOString();

    // 1. Fetch Recent Events
    // ------------------------------------------------------------------
    const eventsRes = await getAllEvents({ size: 3, sort: 'updated_at_desc' });
    recentEvents.value = (eventsRes.items || []).map(e => ({
      id: e.id,
      title: e.title,
      is_draft: e.is_draft,
      updated_at: e.updated_at,
      location: e.location,
      filled_sessions: 0, 
      total_sessions: e.sessions ? e.sessions.length : 0 
    }));

    // 2. Fetch Sessions using backend `get_user_sessions` per requested scopes
    // ------------------------------------------------------------------
    const now = new Date();

    // Wait List Sessions: scope=joined, start_datetime=now, registration_status_list = ['waitlist','available']
    const waitRes = await getUserSessions({
      scope: 'joined',
      start_datetime: nowISO,
      registration_status_list: ['waitlist', 'available']
    });

    // Current & Upcoming Sessions: scope=all, start_datetime=now, registration_status_list = ['confirmed']
    const upcomingRes = await getUserSessions({
      scope: 'all',
      start_datetime: nowISO,
      registration_status_list: ['confirmed']
    });

    // Past Sessions: scope=all, end_datetime=now
    const pastRes = await getUserSessions({
      scope: 'all',
      end_datetime: nowISO,
      registration_status_list: ['confirmed']
    });

    const allWait = (waitRes.items || []);
    const allUpcoming = (upcomingRes.items || []);
    const allPast = (pastRes.items || []);

    const waitlist = allWait.map(mapSessionData);
    const upcoming = allUpcoming.map(mapSessionData);
    const past = allPast.map(mapSessionData);

    // Sort: upcoming by start asc, past by start desc
    upcoming.sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
    past.sort((a, b) => new Date(b.start_time) - new Date(a.start_time));

    // Apply some sensible limits
    upcomingSessions.value = upcoming.slice(0, 50);
    pastSessions.value = past.slice(0, 50);
    waitlistSessions.value = waitlist.slice(0, 50);

    // Reset visible counts when we refresh the dashboard data
    waitVisible.value = sessionsPageSize;
    upcomingVisible.value = sessionsPageSize;
    pastVisible.value = sessionsPageSize;

  } catch (error) {
    console.error("Failed to load dashboard data", error);
  } finally {
    loadingDashboard.value = false;
  }
};

// --- COMPUTED & LOGIC ---

// Filters upcoming sessions based on Search Input 
const filteredUpcoming = computed(() => {
  let result = upcomingSessions.value.slice();

  // Apply time-range filter
  const now = new Date();
  let rangeStart = null;
  let rangeEnd = null;

  switch (upcomingTimeRange.value) {
    case 'today': {
      rangeStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      rangeEnd = new Date(rangeStart);
      rangeEnd.setDate(rangeEnd.getDate() + 1);
      break;
    }
    case 'this_week': {
      // week starting today (next 7 days)
      rangeStart = new Date(now);
      rangeEnd = new Date(now);
      rangeEnd.setDate(rangeEnd.getDate() + 7);
      break;
    }
    case 'this_month': {
      rangeStart = new Date(now.getFullYear(), now.getMonth(), 1);
      rangeEnd = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      break;
    }
    case 'next_month': {
      rangeStart = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      rangeEnd = new Date(now.getFullYear(), now.getMonth() + 2, 1);
      break;
    }
    default:
      break;
  }

  if (rangeStart && rangeEnd) {
    result = result.filter(s => {
      const sStart = s.start_time ? new Date(s.start_time) : null;
      if (!sStart) return false;
      return sStart >= rangeStart && sStart < rangeEnd;
    });
  }

  // Apply text search
  if (upcomingSearch.value) {
    const q = upcomingSearch.value.toLowerCase();
    result = result.filter(s => s.event_title?.toLowerCase().includes(q));
  }

  return result;
});

// --- Paginated views (slice by visible counts) ---
const paginatedWaitlist = computed(() => waitlistSessions.value.slice(0, waitVisible.value));
const paginatedUpcoming = computed(() => filteredUpcoming.value.slice(0, upcomingVisible.value));
const paginatedPast = computed(() => pastSessions.value.slice(0, pastVisible.value));

const getInitials = (name) => {
  if (!name) return 'U';
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
};

const getAvatar = () => {
    return authStore.user?.profile_image
}

const toggleRow = (id) => {
  const index = expandedRows.value.indexOf(id);
  if (index === -1) expandedRows.value.push(id);
  else expandedRows.value.splice(index, 1);
};

// --- Load More handlers for sections ---
const loadMoreSection = (section) => {
  if (section === 'waitlist') {
    if (waitlistSessions.value.length > waitVisible.value) {
      waitVisible.value += sessionsPageSize;
      return;
    }
  }
  if (section === 'upcoming') {
    if (filteredUpcoming.value.length > upcomingVisible.value) {
      upcomingVisible.value += sessionsPageSize;
      return;
    }
  }
  if (section === 'past') {
    if (pastSessions.value.length > pastVisible.value) {
      pastVisible.value += sessionsPageSize;
      return;
    }
  }
};

// Reset upcoming visible count when its filters/search change
watch([upcomingSearch, upcomingTimeRange], () => {
  upcomingVisible.value = sessionsPageSize;
});

const goToCreateEvent = () => router.push({name: 'CreateEvents'});
const goToOverview = (uuid) => router.push({ name: 'EventOverview', params: { event_uuid: uuid } });

const copyLink = (uuid) => {
  const link = `${window.location.origin}/${uuid}`;
  navigator.clipboard.writeText(link);
  alert(`Invitation link copied!`);
};

// --- FORMATTERS ---
const timeAgo = (dateInput) => {
  if (!dateInput) return 'Unknown';
  const date = new Date(dateInput);
  const seconds = Math.floor((new Date() - date) / 1000);
  
  let interval = seconds / 31536000;
  if (interval > 1) return Math.floor(interval) + " years ago";
  interval = seconds / 2592000;
  if (interval > 1) return Math.floor(interval) + " months ago";
  interval = seconds / 86400;
  if (interval >= 1) return Math.floor(interval) + " days ago";
  interval = seconds / 3600;
  if (interval >= 1) return Math.floor(interval) + " hours ago";
  interval = seconds / 60;
  if (interval >= 1) return Math.floor(interval) + " mins ago";
  return "Just now";
};

const formatDateTimeRange = (startStr, endStr) => {
  if (!startStr || !endStr) return 'TBA';
  const startDate = new Date(startStr);
  const endDate = new Date(endStr);
  
  // Format: "15 Feb 2026"
  const dateFmt = new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).format(startDate);
  
  // Format: "10:00 AM"
  const timeOpts = { hour: 'numeric', minute: '2-digit', hour12: true };
  const startTimeFmt = new Intl.DateTimeFormat('en-US', timeOpts).format(startDate);
  const endTimeFmt = new Intl.DateTimeFormat('en-US', timeOpts).format(endDate);
  
  return `${dateFmt}, ${startTimeFmt} - ${endTimeFmt}`;
};

// --- LIFECYCLE ---
onMounted(() => {
  fetchUserProfile();
  fetchDashboardData();
});
</script>