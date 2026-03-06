<template>
    <div class="min-h-screen bg-base-200 pb-28">
        <div class="mx-auto max-w-7xl px-4 py-6 md:px-6">

            <!-- Global Error Toast -->
            <div v-if="error" class="toast toast-center toast-top z-50">
                <div class="alert alert-error shadow-lg">
                    <span>{{ error }}</span>
                </div>
            </div>

            <div class="grid grid-cols-1 gap-6 lg:grid-cols-4">

                <!-- Right Column (Event Details) -->
                <div class="order-1 lg:order-2 lg:col-span-1">

                    <div v-if="eventLoading" class="flex justify-center py-10">
                        <LoadingSpinner />
                    </div>

                    <div v-else
                        class="card bg-base-100 border border-gray-200 shadow-lg rounded-2xl wrap-anywhere lg:sticky lg:top-24">
                        <div class="card-body gap-5">

                            <h2 class="card-title text-xl wrap-anywhere leading-tight">
                                {{ event.title }}
                            </h2>

                            <div class="space-y-3 text-base">
                                <p v-if="event.location" class="flex items-start gap-2 min-w-0">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor"
                                        class="size-5 shrink-0 mt-0.5 text-primary">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                                    </svg>
                                    <span class="wrap-anywhere">{{ event.location }}</span>
                                </p>

                                <div class="flex items-center gap-2">
                                    <img :src="event?.host?.profile_image"
                                        class="w-8 h-8 rounded-full object-cover ring ring-base-300" alt="host" />
                                    <div v-if="!isCurrentUserHost" class="font-medium">{{
                                        event?.host?.full_name }}</div>
                                    <div v-else class="font-medium">{{ event?.host?.full_name }} (You)</div>
                                </div>
                            </div>

                            <div v-if="event.description" class="divider my-0"></div>

                            <div v-if="event.description" class="text-base wrap-anywhere">
                                <h3 class="font-semibold mb-2 text-base-content">Event Description</h3>
                                <p class="opacity-80 leading-relaxed">
                                    {{ event.description }}
                                </p>
                            </div>

                        </div>
                    </div>
                </div>

                <!-- Left Column -->
                <div class="order-2 lg:order-1 lg:col-span-3">

                    <!-- Share Section -->
                    <div class="bg-base-100 p-6 rounded-2xl border border-gray-200 shadow-md">
                        <div class="flex items-center gap-2 mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="1.5" stroke="blue"
                                class="size-6 text-primary" fill="blue">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                            </svg>
                            <h2 class="text-xl font-bold">Share This Event</h2>
                        </div>

                        <div v-if="isDraftEvent"
                            class="mt-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3 rounded-xl border border-base-300 bg-base-200 px-4 py-3">
                            <div>
                                <h3 class="font-bold">Event Status</h3>
                                <p class="text-sm opacity-70">
                                    Publish this event to enable sharing and registration.
                                </p>
                            </div>
                            <span class="badge badge-lg rounded-full px-4 badge-warning text-warning-content">
                                Draft
                            </span>
                        </div>

                        <div class="flex flex-col md:flex-row justify-between items-center
                        p-4 rounded-xl gap-3 mt-4 border-gray-300 border bg-slate-100">

                            <div>
                                <h3 class="font-bold">Participant Restrictions</h3>
                                <p class="text-sm opacity-70">
                                    Limit max sessions per participant
                                </p>
                            </div>

                            <div v-if="event.max_sessions_per_user"
                                class="badge rounded-full p-4 bg-indigo-100 text-indigo-900 font-bold">
                                Limit: {{ event.max_sessions_per_user }} sessions per person
                            </div>
                            <div v-else class="badge rounded-full p-4">
                                No session limit
                            </div>
                        </div>

                        <div class="mt-5">
                            <h3 class="mb-2 font-semibold">Share Link</h3>

                            <p v-if="isDraftEvent" class="text-sm text-warning mb-2">
                                Share link is unavailable while event is in draft.
                            </p>

                            <div class="join w-full">
                                <input class="input join-item input-bordered w-full bg-slate-100 border-gray-300"
                                    readonly :disabled="isDraftEvent" :value="isDraftEvent ? '' : shareLink"
                                    :placeholder="isDraftEvent ? 'No share link for draft event' : ''" />

                                <button class="border border-gray-300 btn-outline btn join-item"
                                    :disabled="isDraftEvent" @click="copyLink">
                                    {{ copied ? 'Copied!' : 'Copy' }}
                                </button>
                            </div>
                        </div>

                    </div>

                    <!-- Sessions -->
                    <div id="event-sessions-section" class="mt-8">

                        <div class="flex items-center justify-between mb-5 flex-wrap">
                            <h2 class="text-xl font-bold">Session Details <span
                                    class="badge badge-sm badge-soft">Timezone:
                                    {{
                                        timezone
                                    }}</span></h2>
                            <div class="badge badge-outline">{{ sessions.length }} sessions</div>
                        </div>

                        <div v-if="isInitialSessionsLoading" class="flex justify-center py-6">
                            <LoadingSpinner />
                        </div>

                        <TransitionGroup name="session-grid" tag="div"
                            class="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
                            <SessionCard v-for="session in sessions" :key="session.uuid" :session="session"
                                :timezone="timezone" :is-current-user-host="isCurrentUserHost"
                                @open-registered-users="openRegisteredUsersModal" />
                        </TransitionGroup>

                    </div>

                    <!-- Pagination -->
                    <div v-if="nextCursor" class="flex justify-center mt-6">
                        <button class="btn btn-outline btn-neutral flex items-center gap-2" :disabled="isLoadingMore"
                            @click="loadMore">
                            <span v-if="!isLoadingMore">Load More</span>
                            <span v-else class="loading loading-dots loading-md"></span>
                        </button>
                    </div>
                </div>
            </div>

        </div>

        <!-- Edit Event / Register button -->
        <div class="fixed bottom-0 left-0 right-0 bg-base-100/95 backdrop-blur border-t border-base-300 shadow-lg p-4">
            <div class="mx-auto max-w-7xl flex justify-end gap-3">
                <button v-if="isCurrentUserHost" class="btn btn-sm btn-outline btn-neutral" @click="goToEditEvent">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                    </svg>
                    Edit Event
                </button>
                <button v-if="isCurrentUserHost" class="btn btn-sm btn-outline btn-error"
                    :disabled="!isCurrentUserHost || deletingEvent" @click="onDeleteEvent">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-5">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.166L18.16 19.673A2.25 2.25 0 0 1 15.916 21.75H8.084a2.25 2.25 0 0 1-2.245-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                    {{ deletingEvent ? 'Deleting...' : 'Delete Event' }}
                </button>
                <button class="btn btn-sm btn-primary" :disabled="isDraftEvent || !user" @click="goToRegister">
                    {{ !user ? 'Login before register' : 'Register' }}
                </button>
            </div>
        </div>

        <RegisteredUsersModal v-if="isShowRegisteredUser && selectedSessionUuid"
            :is-show-registered-user="isShowRegisteredUser" :is-current-user-host="isCurrentUserHost"
            :session-uuid="selectedSessionUuid" :is-past-session="isPastSession" @close="closeRegisteredUsersModal"
            @user-unregistered="handleUserUnregistered" />
    </div>
</template>

<script setup>
import { computed, ref, watch, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SessionCard from '../components/session/SessionCard.vue'
import RegisteredUsersModal from '../components/session/RegisteredUsersModal.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { deleteEvent, getEvent, getSessions } from '../services/event'
import { getSessionByUuid } from '../services/session'
import { useAuthStore } from '../store/authStore'

const route = useRoute()
const router = useRouter()

/* ---------------- STATE ---------------- */

const authStore = useAuthStore()
const user = computed(() => authStore.user)
const timezone = computed(() => user.value?.timezone || "Europe/London") // user's timezone preference

const event = ref({}) // main event details and sessions list
const sessions = ref([])

const eventLoading = ref(false) // loading state for LoadingSpinner Component
const sessionsLoading = ref(false)

// pagination
const nextCursor = ref(null)
const selectedSessionUuid = ref(null)
const isShowRegisteredUser = ref(false)
const isPastSession = ref(false)
const deletingEvent = ref(false)

const error = ref(null)
const copied = ref(false) // copy share link state
const isCurrentUserHost = computed(() => {
    const hostId = event.value?.host?.id
    const currentUserId = user.value?.id

    if (hostId == null || currentUserId == null) return false
    return hostId === currentUserId
})

const isDraftEvent = computed(() => Boolean(event.value?.is_draft))
const isInitialSessionsLoading = computed(() => sessionsLoading.value && sessions.value.length === 0)
const isLoadingMore = computed(() => sessionsLoading.value && sessions.value.length > 0)

/* ---------------- SHARE LINK ---------------- */

const shareLink = computed(() => {
    const resolved = router.resolve({
        name: 'EventOverview',
        params: { event_uuid: route.params.event_uuid }
    })
    return window.location.origin + resolved.href
})

function copyLink() {
    if (isDraftEvent.value) return
    navigator.clipboard.writeText(shareLink.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
}

function goToEditEvent() {
    if (!isCurrentUserHost.value) return
    router.push({ name: 'EditEvent', params: { event_uuid: route.params.event_uuid } })
}

async function onDeleteEvent() {
    if (!isCurrentUserHost.value || deletingEvent.value) return

    const confirmed = window.confirm('Delete this event? This action cannot be undone.')
    if (!confirmed) return

    deletingEvent.value = true
    error.value = null
    try {
        await deleteEvent(route.params.event_uuid)
        router.replace({ name: 'AllEvents' })
    } catch (err) {
        error.value = 'Failed to delete event.'
    } finally {
        deletingEvent.value = false
    }
}

function goToRegister() {
    if (isDraftEvent.value) return
    if (!user.value) return

    router.push({ name: 'EventRegistration' })
}

function openRegisteredUsersModal(sessionUuid, isPast) {
    if (!isCurrentUserHost.value) return
    if (!sessionUuid) return
    selectedSessionUuid.value = sessionUuid
    isShowRegisteredUser.value = true
    isPastSession.value = isPast
}

function closeRegisteredUsersModal() {
    isShowRegisteredUser.value = false
    selectedSessionUuid.value = null
}

async function handleUserUnregistered(payload) {
    const sessionUuid = payload?.sessionUuid
    if (!sessionUuid) return

    const sessionIndex = sessions.value.findIndex((session) => session.uuid === sessionUuid)
    if (sessionIndex === -1) return

    try {
        const updatedSession = await getSessionByUuid(sessionUuid)
        sessions.value.splice(sessionIndex, 1, updatedSession)
    } catch (err) {
        error.value = 'Failed to refresh session card.'
    }
}

/* ---------------- FETCH EVENT ---------------- */

async function fetchEvent(uuid) {
    eventLoading.value = true
    error.value = null
    try {
        const data = await getEvent(uuid);
        event.value = data;
    } catch (err) {
        const status = err.response?.status

        if (status === 404 || status === 422) {
            router.replace({ name: 'NotFound' })
            return
        }

        error.value = 'Failed to load event details.'
    } finally {
        eventLoading.value = false
    }
}

/* ---------------- FETCH SESSIONS ---------------- */

async function fetchSessions(uuid, cursor = null, size = 6) {
    sessionsLoading.value = true
    try {
        if (!cursor) {
            sessions.value = []
            nextCursor.value = null
        }
        const data = await getSessions(uuid, cursor, size);

        sessions.value.push(...data.items)
        nextCursor.value = data.next_page

    } catch (err) {
        const status = err.response?.status
        if (status === 404 || status === 422) {
            router.replace({ name: 'NotFound' })
            return
        }

        error.value = 'Failed to load sessions.'
    } finally {
        sessionsLoading.value = false
    }
}

/* ---------------- PAGINATION ---------------- */

async function loadMore() {
    if (!nextCursor.value) return
    await fetchSessions(route.params.event_uuid, nextCursor.value)
    await nextTick()

    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    })
}

/* ---------------- ROUTE WATCH ---------------- */

watch(
    () => route.params.event_uuid,
    (uuid) => {
        if (!uuid) return
        fetchEvent(uuid)
        fetchSessions(uuid)
    },
    { immediate: true }
)

onMounted(async () => {
    if (!user.value) {
        await authStore.updateUser()
    }
})
</script>

<style scoped>
.session-grid-enter-active,
.session-grid-leave-active {
    transition: all 0.5s ease;
}

.session-grid-enter-from,
.session-grid-leave-to {
    opacity: 0;
    transform: translateY(10px);
}
</style>