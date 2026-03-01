<template>
    <div class="border border-base-300 border-l-4 shadow-md hover:shadow-xl transition-all mb-3 rounded-xl cursor-pointer"
        :class="cardAccentClass">
        <div class="p-4 flex flex-col gap-4">
            <div class="flex items-start justify-between gap-2">
                <h3 class="font-semibold text-base-content leading-tight line-clamp-3">
                    {{ session?.event?.title || 'Untitled Event' }}
                </h3>
                <div class="flex items-center gap-1">
                    <span class="badge badge-sm whitespace-nowrap" :class="registrationStatusClass">
                        {{ registrationStatusLabel }}
                    </span>
                    <div class="dropdown dropdown-end">
                        <button tabindex="0" class="btn btn-ghost btn-xs btn-circle" aria-label="Session actions">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                                class="size-4">
                                <path fill-rule="evenodd"
                                    d="M10.5 6a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Zm0 6a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Zm0 6a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0Z"
                                    clip-rule="evenodd" />
                            </svg>
                        </button>
                        <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-10 w-36 p-2 shadow">
                            <li>
                                <button :disabled="!eventUuid" @click="goToEventOverview">View Details</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="text-sm space-y-2 text-base-content/80">
                <template v-if="isDifferentDateInUserTimezone">
                    <p class="mb-1"><span class="font-semibold">Start:</span> {{ differentDayStartLine }}</p>
                    <p class="mb-1"><span class="font-semibold">End:</span> {{ differentDayEndLine }}</p>
                </template>
                <template v-else>
                    <p class="mb-1"><span class="font-semibold">Date:</span> {{ sessionDateLabel }}</p>
                    <p class="mb-1"><span class="font-semibold">Time:</span> {{ sessionTimeRange }}</p>
                </template>
                <p class="mb-1"><span class="font-semibold">Location:</span> {{ sessionLocation }}</p>
            </div>

            <div class="flex items-center gap-2 text-sm text-base-content/80">
                <img v-if="hostImage" :src="hostImage" alt="host profile" class="w-6 h-6 rounded-full object-cover">
                <div v-else class="w-6 h-6 rounded-full bg-base-300"></div>
                <p>{{ hostDisplayName }}</p>
            </div>

            <div class="space-y-1">
                <div class="flex items-center justify-between text-xs text-base-content/70">
                    <span>Seats</span>
                    <span>{{ seatDisplay }}</span>
                </div>
                <progress v-if="seatCapacity !== null" class="progress w-full h-2" :class="capacityClass"
                    :value="capacityPercent" max="100"></progress>
            </div>
        </div>
    </div>
</template>
<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../../store/authStore';
import { TZDate } from '@date-fns/tz';
import { format } from 'date-fns';


const props = defineProps({
    session: {
        type: Object,
        required: true
    },
})

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);
const router = useRouter();

const session = computed(() => props.session || {});

const host = computed(() => session.value.event?.host || null);

const hostImage = computed(() => session.value.event?.host?.profile_image || null);

const eventUuid = computed(() => session.value.event?.share_uuid || session.value.event?.uuid || null);

const goToEventOverview = () => {
    if (!eventUuid.value) return;
    router.push({
        name: 'EventOverview',
        params: { event_uuid: eventUuid.value }
    });
};

const hostDisplayName = computed(() => {
    const baseName = host.value?.full_name || 'Unknown host';
    const currentUserId = user.value?.id;
    const hostId = host.value?.id;

    if (currentUserId == null || hostId == null) return baseName;
    if (String(currentUserId) === String(hostId)) return `${baseName} (You)`;
    return baseName;
});

const userTimezone = computed(() => {
    const timezone = user.value?.timezone;
    if (!timezone) return 'Europe/London';

    return timezone;
});

const startDate = computed(() => {
    if (!session.value.start_datetime) return null;
    return new TZDate(session.value.start_datetime, userTimezone.value);
});

const endDate = computed(() => {
    if (!session.value.end_datetime) return null;
    return new TZDate(session.value.end_datetime, userTimezone.value);
});

const safeFormatInTimezone = (date, pattern) => {
    return format(new TZDate(date, userTimezone.value), pattern);
};

const isDifferentDateInUserTimezone = computed(() => {
    if (!startDate.value || !endDate.value) return false;

    return startDate.value.getDate() !== endDate.value.getDate() ||
        startDate.value.getMonth() !== endDate.value.getMonth() ||
        startDate.value.getFullYear() !== endDate.value.getFullYear();
});

const sessionDateLabel = computed(() => {
    if (!startDate.value) return 'Date not set';

    if (!endDate.value) {
        return safeFormatInTimezone(startDate.value, 'EEE, d MMM yyyy');
    }

    if (!isDifferentDateInUserTimezone.value) {
        return safeFormatInTimezone(startDate.value, 'EEE, d MMM yyyy');
    }

    return `${safeFormatInTimezone(startDate.value, 'EEE, d MMM yyyy')} → ${safeFormatInTimezone(endDate.value, 'EEE, d MMM yyyy')}`;
});

const sessionTimeRange = computed(() => {
    if (!startDate.value || !endDate.value) return 'Time not set';

    if (!isDifferentDateInUserTimezone.value) {
        const startTime = safeFormatInTimezone(startDate.value, 'hh:mm a');
        const endTime = safeFormatInTimezone(endDate.value, 'hh:mm a');
        return `${startTime} - ${endTime}`;
    }

    const startDateTime = safeFormatInTimezone(startDate.value, 'd MMM hh:mm a');
    const endDateTime = safeFormatInTimezone(endDate.value, 'd MMM hh:mm a');
    return `${startDateTime} → ${endDateTime}`;
});

const differentDayStartLine = computed(() => {
    if (!startDate.value || !isDifferentDateInUserTimezone.value) return '';
    return safeFormatInTimezone(startDate.value, 'EEE, d MMM yyyy hh:mm a');
});

const differentDayEndLine = computed(() => {
    if (!endDate.value || !isDifferentDateInUserTimezone.value) return '';
    return safeFormatInTimezone(endDate.value, 'EEE, d MMM yyyy hh:mm a');
});

const sessionLocation = computed(() => {
    return session.value.location || session.value.event?.location || 'Location not set';
});

const seatTaken = computed(() => Number(session.value.seat_taken ?? 0));
const seatCapacity = computed(() => {
    const cap = session.value.seat_capacity;
    if (cap === null || cap === undefined) return null;
    return Number(cap);
});

const seatDisplay = computed(() => {
    if (seatCapacity.value === null) return `${seatTaken.value} joined`;
    return `${seatTaken.value}/${seatCapacity.value}`;
});

const capacityPercent = computed(() => {
    if (seatCapacity.value === null || seatCapacity.value <= 0) return 0;
    return Math.min(100, Math.round((seatTaken.value / seatCapacity.value) * 100));
});

const capacityClass = computed(() => {
    if (seatCapacity.value === null) return 'progress-primary';
    if (capacityPercent.value >= 100) return 'progress-error';
    if (capacityPercent.value >= 75) return 'progress-warning';
    return 'progress-neutral';
});

const registrationStatusLabel = computed(() => {
    const status = session.value.registration_status;
    if (!status) return 'Not Registered';
    return status.charAt(0).toUpperCase() + status.slice(1);
});

const registrationStatusClass = computed(() => {
    const status = session.value.registration_status;
    if (status === 'confirmed') return 'badge-success';
    if (status === 'waitlist') return 'badge-warning';
    if (status === 'available') return 'badge-primary';
    return 'badge-ghost';
})

const cardAccentClass = computed(() => {
    const rawStatus = session.value.registration_status;
    const status = String(rawStatus || '').trim().toLowerCase();

    if (status === 'confirmed') return 'border-l-success';
    if (status === 'waitlist' || status === 'waiting' || status === 'queueing' || status === 'queued') return 'border-l-warning';
    if (status === 'available' || status === 'open') return 'border-l-primary';
    return 'border-l-base-300';
});

</script>