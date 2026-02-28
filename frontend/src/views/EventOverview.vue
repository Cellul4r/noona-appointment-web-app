<template>
    <div class="mx-auto p-6 bg-base-200 min-h-screen pb-28">

        <!-- Global Error Toast -->
        <div v-if="error" class="toast toast-center toast-top">
            <div class="alert alert-error">
                <span>{{ error }}</span>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">

            <!-- Right Column (Event Details) -->
            <div class="order-1 lg:order-2 lg:col-span-1">

                <div v-if="eventLoading" class="flex justify-center py-10">
                    <LoadingSpinner />
                </div>

                <div v-else class="card bg-base-100 shadow-md rounded-xl wrap-break-word">
                    <div class="card-body">

                        <h2 class="card-title text-xl wrap-break-word">
                            {{ event.title }}
                        </h2>

                        <div class="space-y-2 text-base">
                            <p>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-6 inline">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                                </svg> {{ event.location }}
                            </p>

                            <div>
                                <img :src="event?.host?.profile_image" class="w-6 h-6 rounded-full inline mr-2">
                                <div v-if="!isCurrentUserHost" class="inline">{{
                                    event?.host?.full_name }}</div>
                                <div v-else class="inline">{{ event?.host?.full_name }} (You)</div>
                            </div>
                        </div>

                        <div class="divider my-0"></div>

                        <div class="text-base wrap-break-word">
                            <h3 class="font-semibold mb-2">Event Description</h3>
                            <p class="opacity-80">
                                {{ event.description }}
                            </p>
                        </div>

                    </div>
                </div>
            </div>

            <!-- Left Column -->
            <div class="order-2 lg:order-1 lg:col-span-3">

                <!-- Share Section -->
                <div class="bg-base-100 p-6 rounded-xl shadow-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                        class="size-6 inline">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M7.217 10.907a2.25 2.25 0 1 0 0 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186 9.566-5.314m-9.566 7.5 9.566 5.314m0 0a2.25 2.25 0 1 0 3.935 2.186 2.25 2.25 0 0 0-3.935-2.186Zm0-12.814a2.25 2.25 0 1 0 3.933-2.185 2.25 2.25 0 0 0-3.933 2.185Z" />
                    </svg>
                    <h2 class="text-xl font-bold mb-4 inline"> Share This Event</h2>

                    <div class="flex flex-col md:flex-row justify-between items-center
                      bg-base-200 p-4 rounded-xl gap-3 mt-4">

                        <div>
                            <h3 class="font-bold">Participant Restrictions</h3>
                            <p class="text-sm opacity-70">
                                Limit max sessions per participant
                            </p>
                        </div>

                        <div v-if="event.max_sessions_per_user" class="badge badge-info rounded-full p-4">
                            Limit: {{ event.max_sessions_per_user }} sessions per person
                        </div>
                        <div v-else class="badge badge-info rounded-full p-4">
                            No session limit
                        </div>
                    </div>

                    <div class="mt-4">
                        <h3 class="mb-2 font-semibold">Share Link</h3>

                        <div class="join w-full">
                            <input class="input join-item" readonly :value="shareLink" />

                            <button class="btn btn-info join-item" @click="copyLink">
                                {{ copied ? 'Copied!' : 'Copy' }}
                            </button>
                        </div>
                    </div>

                </div>

                <!-- Sessions -->
                <div class="mt-6">

                    <div v-if="sessionsLoading" class="flex justify-center py-6">
                        <LoadingSpinner />
                    </div>
                    <h2 class="text-xl font-bold mb-5">Session Details</h2>
                    <div class="grid gap-3 grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
                        <SessionCard v-for="session in sessions" :key="session.id" :session="session"
                            :is-current-user-host="isCurrentUserHost" />
                    </div>

                </div>

                <!-- Pagination -->
                <div v-if="nextCursor" class="flex justify-center mt-4">
                    <button class="btn btn-soft" :disabled="sessionsLoading" @click="loadMore">
                        {{ sessionsLoading ? "Loading..." : "Load More" }}
                    </button>
                </div>

            </div>

        </div>

        <!-- Edit Event / Register button -->
        <div class="fixed bottom-0 left-0 right-0 bg-base-100 border-t shadow-md p-4">
            <div class="flex justify-end">
                <button class="btn btn-soft btn-secondary">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6 inline">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                    </svg>Edit Event
                </button>
                <button class="btn btn-primary ml-3" @click="goToRegister">
                    Register
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import SessionCard from '../components/session/SessionCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { getEvent, getSessions } from '../services/event'
import { useAuthStore } from '../store/authStore'

const route = useRoute()
const router = useRouter()

/* ---------------- STATE ---------------- */

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const event = ref({})
const sessions = ref([])

const eventLoading = ref(false)
const sessionsLoading = ref(false)

const nextCursor = ref(null)

const error = ref(null)
const copied = ref(false)
const isCurrentUserHost = computed(() => {
    const hostId = event.value?.host?.id
    const currentUserId = user.value?.id

    if (hostId == null || currentUserId == null) return false
    return String(hostId) === String(currentUserId)
})

/* ---------------- SHARE LINK ---------------- */

const shareLink = computed(() => {
    const resolved = router.resolve({
        name: 'EventOverview',
        params: { event_uuid: route.params.event_uuid }
    })
    return window.location.origin + resolved.href
})

function copyLink() {
    navigator.clipboard.writeText(shareLink.value)
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
}

/* ---------------- FETCH EVENT ---------------- */

async function fetchEvent(uuid) {
    eventLoading.value = true
    try {
        const data = await getEvent(uuid);
        event.value = data;
    } catch (err) {
        error.value = 'Failed to load event details.'
    } finally {
        eventLoading.value = false
    }
}

/* ---------------- FETCH SESSIONS ---------------- */

async function fetchSessions(uuid, cursor = null, size = 5) {
    sessionsLoading.value = true
    try {
        const data = await getSessions(uuid, cursor, size);

        sessions.value.push(...data.items)
        nextCursor.value = data.next_page

    } catch (err) {
        error.value = 'Failed to load sessions.'
    } finally {
        sessionsLoading.value = false
    }
}

/* ---------------- PAGINATION ---------------- */

async function loadMore() {
    if (!nextCursor.value) return
    await fetchSessions(route.params.event_uuid, nextCursor.value)
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