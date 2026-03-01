<template>
    <dialog class="modal" :open="isOpen">
        <div class="modal-box max-w-lg">
            <div class="flex items-start justify-between gap-3">
                <h3 class="font-bold text-xl leading-tight">{{ sessionTitle }}</h3>
                <span class="badge text-sm whitespace-nowrap shrink-0" :class="statusClass">{{ statusLabel
                }}</span>
            </div>

            <div class="mt-4 space-y-2 text-base text-base-content/80">
                <template v-if="isDifferentDateInTimezone">
                    <p><span class="font-semibold">Start:</span> {{ startLine }}</p>
                    <p><span class="font-semibold">End:</span> {{ endLine }}</p>
                </template>
                <template v-else>
                    <p><span class="font-semibold">Date:</span> {{ dateLine }}</p>
                    <p><span class="font-semibold">Time:</span> {{ timeLine }}</p>
                </template>
                <p><span class="font-semibold">Location:</span> {{ locationLine }}</p>
                <p><span class="font-semibold">Seats:</span> {{ seatsLine }}</p>
            </div>

            <div class="mt-4 flex items-center gap-2 text-base text-base-content/80">
                <img v-if="hostImage" :src="hostImage" alt="host profile" class="w-7 h-7 rounded-full object-cover">
                <div v-else class="w-7 h-7 rounded-full bg-base-300"></div>
                <p>{{ hostName }} {{ sessionData?.event?.host?.id === user?.id ? '(You)' : '' }}</p>
            </div>

            <div class="modal-action">
                <button class="btn btn-outline" @click="emit('close')">Close</button>
                <button class="btn btn-primary" :disabled="!eventUuid" @click="goToEventOverview">View Details</button>
            </div>
        </div>

        <form method="dialog" class="modal-backdrop" @click.prevent="emit('close')">
            <button>close</button>
        </form>
    </dialog>
</template>

<script setup>
import { TZDate } from '@date-fns/tz';
import { format } from 'date-fns';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../store/authStore';
import { storeToRefs } from 'pinia';

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    },
    session: {
        type: Object,
        default: null
    },
    timezone: {
        type: String,
        default: 'Europe/London'
    }
});

const emit = defineEmits(['close']);
const router = useRouter();
const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const sessionData = computed(() => props.session || {});

const startDate = computed(() => {
    if (!sessionData.value?.start_datetime) return null;
    return new TZDate(sessionData.value.start_datetime, props.timezone);
});

const endDate = computed(() => {
    if (!sessionData.value?.end_datetime) return null;
    return new TZDate(sessionData.value.end_datetime, props.timezone);
});

const safeFormatInTimezone = (date, pattern) => {
    return format(new TZDate(date, props.timezone), pattern);
};

const isDifferentDateInTimezone = computed(() => {
    if (!startDate.value || !endDate.value) return false;

    return startDate.value.getDate() !== endDate.value.getDate() ||
        startDate.value.getMonth() !== endDate.value.getMonth() ||
        startDate.value.getFullYear() !== endDate.value.getFullYear();
});

const sessionTitle = computed(() => sessionData.value?.event?.title || 'Session');
const hostImage = computed(() => sessionData.value?.event?.host?.profile_image || null);
const hostName = computed(() => sessionData.value?.event?.host?.full_name || 'Unknown host');

const dateLine = computed(() => {
    if (!startDate.value) return 'Date not set';
    return safeFormatInTimezone(startDate.value, 'EEE, d MMM yyyy');
});

const timeLine = computed(() => {
    if (!startDate.value || !endDate.value) return 'Time not set';
    return `${safeFormatInTimezone(startDate.value, 'hh:mm a')} - ${safeFormatInTimezone(endDate.value, 'hh:mm a')}`;
});

const startLine = computed(() => {
    if (!startDate.value) return 'Not set';
    return safeFormatInTimezone(startDate.value, 'EEE, d MMM yyyy hh:mm a');
});

const endLine = computed(() => {
    if (!endDate.value) return 'Not set';
    return safeFormatInTimezone(endDate.value, 'EEE, d MMM yyyy hh:mm a');
});

const locationLine = computed(() => sessionData.value?.location || sessionData.value?.event?.location || 'Location not set');

const seatsLine = computed(() => {
    const taken = Number(sessionData.value?.seat_taken ?? 0);
    const capacity = sessionData.value?.seat_capacity;
    if (capacity === null || capacity === undefined) return `${taken} joined`;
    return `${taken}/${Number(capacity)}`;
});

const statusRaw = computed(() => sessionData.value?.registration_status || null);
const statusLabel = computed(() => {
    if (!statusRaw.value) return 'Not Registered';
    return String(statusRaw.value).charAt(0).toUpperCase() + String(statusRaw.value).slice(1);
});

const statusClass = computed(() => {
    if (statusRaw.value === 'confirmed') return 'badge-success';
    if (statusRaw.value === 'waitlist') return 'badge-warning';
    if (statusRaw.value === 'available') return 'badge-primary';
    return 'badge-ghost';
});

const eventUuid = computed(() => sessionData.value?.event?.share_uuid || sessionData.value?.event?.uuid || null);

const goToEventOverview = () => {
    if (!eventUuid.value) return;
    router.push({
        name: 'EventOverview',
        params: { event_uuid: eventUuid.value }
    });
    emit('close');
};
</script>
