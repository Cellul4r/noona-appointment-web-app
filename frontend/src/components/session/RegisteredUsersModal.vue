<template>
    <dialog class="modal transition-all duration-500" :open="isShowRegisteredUser">
        <div class="modal-box relative">
            <select v-model="registrationStatus" class="absolute right-4 select select-sm select-primary w-fit">
                <option value="confirmed">Confirmed</option>
                <option value="waitlist">Waitlist</option>
                <option value="available">Available</option>
            </select>
            <h3 class="font-bold text-lg mt-0">Registered Users - {{ registrationStatus }}</h3>
            <div v-if="isInitialLoading" class="flex justify-center py-6">
                <LoadingSpinner />
            </div>
            <!-- Note for Past Session -->
            <div v-if="isPastSession" class="badge badge-info mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-4 inline-block mr-2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                </svg>
                This session has ended.
            </div>
            <div class="py-4">
                <div v-if="!isInitialLoading && hasLoadedOnce && registeredUsers.length === 0"
                    class="text-center py-10">
                    No registered users found.
                </div>
                <TransitionGroup v-else name="list" tag="ul">
                    <li v-for="user in registeredUsers" :key="user.id" class="py-2 list-item">
                        <div class="flex justify-between items-center">
                            <div>
                                <img :src="user.profile_image" class="w-6 h-6 rounded-full inline"> {{ user.full_name }}
                                ({{ user.email }})
                            </div>
                            <button v-if="!isPastSession" @click="unregisterUserByHost(user.id)"
                                :disabled="unregisteringUserId === user.id || isInitialLoading"
                                class="btn btn-ghost btn-circle btn-xs hover:border-red-500" title="Delete Participant"
                                aria-label="Delete Participant from session">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="size-5 hover:text-red-500">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                </svg>
                            </button>
                        </div>
                    </li>
                </TransitionGroup>
            </div>
            <button v-if="hasMore && !isInitialLoading" class="btn btn-sm btn-outline w-fit mt-4"
                :disabled="isLoadingMore" @click="fetchRegisteredUsers">
                {{ isLoadingMore ? 'Loading...' : 'Load More' }}
            </button>
            <div class="modal-action">
                <form method="dialog">
                    <!-- if there is a button in form, it will close the modal -->
                    <button class="btn" @click="emit('close')">Close</button>
                </form>
            </div>

        </div>
        <form method="dialog" class="modal-backdrop">
            <button @click="emit('close')">close</button>
        </form>
    </dialog>
</template>
<script setup>
import { computed, ref, watch } from 'vue';
import { getRegisteredUsers, unregisterUserByHost as unregisterUserByHostService } from '../../services/session';
import LoadingSpinner from '../LoadingSpinner.vue';

const emit = defineEmits(['close', 'user-unregistered'])

const props = defineProps({
    sessionUuid: {
        type: [String, Number],
        required: true
    },
    isShowRegisteredUser: {
        type: Boolean,
        required: true
    },
    isCurrentUserHost: {
        type: Boolean,
        required: false
    },
    isPastSession: {
        type: Boolean,
        required: false
    },
})

const registeredUsers = ref([]);
const registrationStatus = ref("confirmed"); // confirmed, waitlist, available
const isInitialLoading = ref(false);
const isLoadingMore = ref(false);
const unregisteringUserId = ref(null);
const hasLoadedOnce = ref(false);
// pagination
const nextCursor = ref(null);

const hasMore = computed(() => {
    return nextCursor.value !== null;
})

const fetchRegisteredUsers = async () => {
    if (!props.isCurrentUserHost) {
        emit('close')
        return
    }
    const shouldShowInitialLoading = registeredUsers.value.length === 0 && !nextCursor.value;

    if (shouldShowInitialLoading) {
        isInitialLoading.value = true;
    } else {
        isLoadingMore.value = true;
    }

    try {
        const data = await getRegisteredUsers(props.sessionUuid, registrationStatus.value, nextCursor.value);
        registeredUsers.value.push(...data.items);
        nextCursor.value = data.next_page;
        hasLoadedOnce.value = true;
    } catch (err) {
        alert("Failed to load registered users.");
    } finally {
        isInitialLoading.value = false;
        isLoadingMore.value = false;
    }

}

const unregisterUserByHost = async (userId) => {
    if (!props.isCurrentUserHost) {
        emit('close')
        return
    }
    const confirm = window.confirm("Are you sure you want to unregister this user? This action cannot be undone.");
    if (!confirm) return
    if (!userId) return
    unregisteringUserId.value = userId;
    try {
        await unregisterUserByHostService(props.sessionUuid, userId);
        // Remove the user from the registeredUsers list
        registeredUsers.value = registeredUsers.value.filter(user => user.id !== userId);
        emit('user-unregistered', {
            sessionUuid: props.sessionUuid,
            userId,
            registrationStatus: registrationStatus.value
        })
    } catch (err) {
        console.error(err);
        alert("Failed to unregister user. Please try again.");
        fetchRegisteredUsers(); // Refresh the list to ensure data consistency
    } finally {
        unregisteringUserId.value = null;
    }
}

watch(registrationStatus, () => {
    if (!props.isShowRegisteredUser) return
    isInitialLoading.value = true;
    registeredUsers.value = [];
    nextCursor.value = null;
    hasLoadedOnce.value = false;
    fetchRegisteredUsers();
});

watch(() => props.isShowRegisteredUser, () => {
    if (!props.isShowRegisteredUser) {
        isInitialLoading.value = false;
        isLoadingMore.value = false;
        unregisteringUserId.value = null;
        hasLoadedOnce.value = false;
        registeredUsers.value = [];
        nextCursor.value = null;
    } else {
        if (!props.isCurrentUserHost) {
            emit('close')
            return
        }
        isInitialLoading.value = true;
        hasLoadedOnce.value = false;
        fetchRegisteredUsers();
    }

}, { immediate: true })
</script>

<style scoped>
.list-item {
    transition: background-color 0.2s ease;
}

.list-move {
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.list-enter-active,
.list-leave-active {
    transition: opacity 0.25s ease, transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.list-leave-active {
    position: absolute;
    width: calc(100% - 2rem);
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateY(8px) scale(0.98);
}

.list-enter-to,
.list-leave-from {
    opacity: 1;
    transform: translateY(0) scale(1);
}
</style>