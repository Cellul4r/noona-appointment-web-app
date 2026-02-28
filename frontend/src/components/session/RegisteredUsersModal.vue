<template>
    <dialog class="modal" :open="isShowRegisteredUser">
        <div class="modal-box relative">
            <select v-model="registrationStatus" class="absolute right-4 select select-sm select-primary w-fit">
                <option value="confirmed">Confirmed</option>
                <option value="waitlist">Waitlist</option>
                <option value="available">Available</option>
            </select>
            <h3 class="font-bold text-lg mt-0">Registered Users - {{ registrationStatus }}</h3>
            <div v-if="loading" class="flex justify-center py-6">
                <LoadingSpinner />
            </div>
            <div class="py-4">
                <div v-if="!loading && registeredUsers.length === 0" class="text-center py-10">
                    No registered users found.
                </div>
                <ul v-else>
                    <li v-for="user in registeredUsers" :key="user.id" class="py-2">
                        <img :src="user.profile_image" class="w-6 h-6 rounded-full inline"> {{ user.full_name }} ({{
                            user.email }})
                    </li>
                </ul>
            </div>
            <button v-if="hasMore && !loading" class="btn btn-sm btn-outline w-fit mt-4" @click="fetchRegisteredUsers">
                Load More
            </button>
            <div class="modal-action">
                <form method="dialog">
                    <!-- if there is a button in form, it will close the modal -->
                    <button class="btn">Close</button>
                </form>
            </div>

        </div>
        <form method="dialog" class="modal-backdrop">
            <button>close</button>
        </form>
    </dialog>
</template>
<script setup>
import { computed, ref, watch } from 'vue';
import { getRegisteredUsers } from '../../services/session';
import LoadingSpinner from '../LoadingSpinner.vue';

const props = defineProps({
    sessionId: {
        type: Number,
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
})

const registeredUsers = ref([]);
const registrationStatus = ref("confirmed"); // confirmed, waitlist, available
const loading = ref(false);
// pagination
const nextCursor = ref(null);

const hasMore = computed(() => {
    return nextCursor.value !== null;
})

const fetchRegisteredUsers = async () => {
    loading.value = true;
    try {
        const data = await getRegisteredUsers(props.sessionId, registrationStatus.value, nextCursor.value);
        registeredUsers.value.push(...data.items);
        nextCursor.value = data.next_page;
    } catch (err) {
        alert("Failed to load registered users.");
    } finally {
        // Any clean up it need
        loading.value = false;
    }

}

watch(registrationStatus, () => {
    if (!props.isShowRegisteredUser) return
    registeredUsers.value = [];
    nextCursor.value = null;
    fetchRegisteredUsers();
});

watch(() => props.isShowRegisteredUser, () => {
    if (!props.isShowRegisteredUser) {
        registeredUsers.value = [];
        nextCursor.value = null;
    } else {
        fetchRegisteredUsers();
    }

})
</script>