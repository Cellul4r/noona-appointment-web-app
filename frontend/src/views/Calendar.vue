<template>
    <div class="bg-base-100 h-screen flex flex-col">
        <!-- Main Content -->
        <div class="flex flex-col md:flex-row flex-1 min-h-0 overflow-hidden bg-base-300/75">
            <!-- Calendar Section -->
            <div class="flex-1 flex flex-col min-h-0 overflow-hidden p-4 md:p-6">
                <div class="calendar-custom-header mb-3">
                    <div>
                        <div class="join-item inline-block">
                            <button class="btn btn-base join items-center text-xl rounded-l-lg" @click="goPrev"
                                aria-label="Previous period">‹</button>
                            <button class="btn btn-base join items-center text-xl rounded-r-lg" @click="goNext"
                                aria-label="Next period">›</button>
                        </div>
                        <h2 class="inline items-center text-2xl font-bold ml-5">{{ currentViewTitle ||
                            'Calendar'
                        }}
                        </h2>
                    </div>

                    <div class="flex flex-wrap items-center gap-2">
                        <div
                            class="flex items-center gap-2 bg-base-100 border border-gray-300 rounded-lg pl-3 py-1.5 shadow-sm">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-4 shrink-0">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
                            </svg>
                            <select v-model="scope"
                                class="select select-xs border-0 font-semibold p-0 pl-2 w-36 shadow-none outline-0 focus:outline-none">
                                <option value="all">All sessions</option>
                                <option value="hosted">Hosted sessions</option>
                                <option value="joined">Registered sessions</option>
                            </select>
                        </div>

                        <div class="bg-slate-200 rounded-lg p-1">
                            <button class="btn bg-inherit border-0 mr-2 py-0 rounded-lg text-xs font-semibold"
                                :class="(currentViewType === 'timeGridWeek') ? 'bg-white text-indigo-600 hover:text-indigo-600' : 'text-slate-600 hover:text-black'"
                                @click="switchView('timeGridWeek')">Week</button>
                            <button
                                class="btn bg-inherit hover:text-black border-0 py-0 rounded-lg text-xs font-semibold"
                                :class="(currentViewType === 'dayGridMonth') ? 'bg-white text-indigo-600 hover:text-indigo-600' : 'text-slate-600 hover:text-black'"
                                @click="switchView('dayGridMonth')">Month</button>
                        </div>
                    </div>
                </div>
                <div class="calendar-shell flex-1 min-h-0 overflow-y-auto bg-base-100 rounded-2xl shadow-sm">
                    <FullCalendar ref="calendarRef" :options="calendarOptions" class="h-full" />
                </div>
            </div>

            <!-- Sessions Panel -->
            <div
                class="w-full md:w-80 bg-base-100 flex flex-col min-h-0 order-2 overflow-hidden shadow-sm border-l border-l-gray-300">
                <div class=" flex-1 overflow-y-auto flex flex-col min-h-0">
                    <div class="p-4 md:p-5 border-b border-base-200 shrink-0">
                        <h2 class="text-lg font-bold">{{ formattedSelectedDate }}</h2>
                        <p class="text-xs text-base-content/60 mt-1">{{ selectedSessions.length }} session(s)</p>
                    </div>
                    <div v-if="selectedSessions.length === 0" class="flex-1 flex items-center justify-center p-4">
                        <p class="text-base-content/50 text-center text-sm">Select a date to view sessions</p>
                    </div>
                    <div v-else
                        class="flex flex-row md:flex-col gap-2 p-3 md:p-4 overflow-x-auto md:overflow-y-auto md:overflow-x-hidden">
                        <SessionWithEventCard v-for="session in selectedSessions" :key="session.id" :session="session"
                            class="min-w-72 md:min-w-0 shrink-0 mb-0" />
                    </div>
                </div>
            </div>
        </div>

        <SessionDetailsModal :is-open="isSessionDetailsModalOpen" :session="selectedEventSession"
            :timezone="calendarTimezone" @close="closeSessionDetailsModal" />

        <footer class="fixed bottom-0 left-0 right-0 bg-base-100 border-t border-base-200 px-4 md:px-6 py-2">
            <p class="text-xs text-base-content/60 text-center md:text-right">Timezone: {{ calendarTimezone }}</p>
        </footer>
    </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import momentTimezonePlugin from '@fullcalendar/moment-timezone';
import { getCalendar } from '../services/calendar'
import SessionWithEventCard from '../components/session/SessionWithEventCard.vue'
import SessionDetailsModal from '../components/session/SessionDetailsModal.vue'
import { useAuthStore } from '../store/authStore'
import { TZDate } from '@date-fns/tz'
import { addDays, format } from 'date-fns'

const calendarEvents = ref([]);

const sessions = ref([]);
const start_date = ref(null); // scope for fetching sessions, in ISO format string in the calendar
const end_date = ref(null);
const scope = ref("all"); // all, joined, hosted

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

const calendarTimezone = computed(() => {
    const timezone = user.value?.timezone
    if (!timezone) return 'Europe/London' // default to UTC+0 timezone

    return timezone
});

const selectedDate = ref(null); // show on sessions panel
const selectedEventSession = ref(null);
const isSessionDetailsModalOpen = ref(false);
const calendarRef = ref(null);
const currentViewTitle = ref('');
const currentViewType = ref('dayGridMonth');

const getCalendarApi = () => calendarRef.value?.getApi?.() ?? null; // function to get FullCalendar API custom

const syncHeaderFromApi = (arg = null) => {
    const view = arg?.view || getCalendarApi()?.view;
    if (!view) return;

    currentViewTitle.value = view.title;
    currentViewType.value = view.type;
};

const goPrev = () => {
    const api = getCalendarApi();
    if (!api) return;
    api.prev();
    syncHeaderFromApi();
};

const goNext = () => {
    const api = getCalendarApi();
    if (!api) return;
    api.next();
    syncHeaderFromApi();
};

const switchView = (viewName) => {
    const api = getCalendarApi();
    if (!api) return;
    api.changeView(viewName);
    syncHeaderFromApi();
};

const normalizeToDateOnly = (value) => {
    if (!value) return null;

    const date = new TZDate(value, calendarTimezone.value);
    return format(date, 'yyyy-MM-dd');
};

// format selected date for output in frontend
const formattedSelectedDate = computed(() => {
    if (!selectedDate.value) return 'Select a date';
    try {
        const date = new TZDate(selectedDate.value, calendarTimezone.value);
        return format(date, 'EEEE, MMMM d, yyyy');
    } catch (e) {
        return selectedDate.value;
    }
});

const isSameSelectedDate = (value) => {
    if (!selectedDate.value || !value) return false;
    const normalized = normalizeToDateOnly(value);
    return normalized === normalizeToDateOnly(selectedDate.value);
};

const getDayCellClasses = (arg) => {
    return isSameSelectedDate(arg.date) ? ['fc-day-selected'] : [];
};

const getEventStatusColor = (registrationStatus) => {
    if (registrationStatus === 'confirmed') return 'event-confirmed';
    if (registrationStatus === 'waitlist') return 'event-waitlist';
    if (registrationStatus === 'available') return 'event-available';
    return 'event-normal';
};

const getEventPalette = (registrationStatus) => {
    if (registrationStatus === 'confirmed') {
        return {
            backgroundColor: 'var(--color-success)',
            borderColor: 'var(--color-success)',
            textColor: 'var(--color-success-content)'
        };
    }

    if (registrationStatus === 'waitlist') {
        return {
            backgroundColor: 'var(--color-warning)',
            borderColor: 'var(--color-warning)',
            textColor: 'var(--color-warning-content)'
        };
    }

    if (registrationStatus === 'available') {
        return {
            backgroundColor: 'var(--color-primary)',
            borderColor: 'var(--color-primary)',
            textColor: 'var(--color-primary-content)'
        };
    }

    return {
        backgroundColor: 'var(--color-base-300)',
        borderColor: 'var(--color-base-300)',
        textColor: 'var(--color-base-content)'
    };
};

const calendarOptions = ref({
    handleWindowResize: true,
    plugins: [
        dayGridPlugin,
        timeGridPlugin,
        interactionPlugin,
        momentTimezonePlugin,
    ],
    initialView: 'dayGridMonth',
    headerToolbar: false,
    dayCellClassNames: getDayCellClasses,
    eventDisplay: 'block',
    timeZone: calendarTimezone.value,
    events: calendarEvents.value,
    datesSet(arg) {
        syncHeaderFromApi(arg);
        start_date.value = new TZDate(arg.start, calendarTimezone.value);
        end_date.value = new TZDate(arg.end, calendarTimezone.value);

        fetchSessions();
    },
    dateClick(info) {
        selectedDate.value = new TZDate(info.date, calendarTimezone.value);
    },
    eventClick(info) {
        const session = info.event.extendedProps.session;
        if (!session) return;
        selectedEventSession.value = session;
        isSessionDetailsModalOpen.value = true;
    }
})

const closeSessionDetailsModal = () => {
    isSessionDetailsModalOpen.value = false;
};

watch(calendarTimezone, (newTimezone) => {
    calendarOptions.value.timeZone = newTimezone;
});

watch(selectedDate, () => {
    calendarOptions.value = { ...calendarOptions.value };
});

const selectedSessions = computed(() => {
    if (!selectedDate.value) return [];

    // beware of timezone issues here - we want naive timezone
    const dayStart = new TZDate(selectedDate.value, calendarTimezone.value);
    const dayEnd = addDays(dayStart, 1);

    return sessions.value.filter(session => {
        const sessionStart = new TZDate(session.start_datetime, calendarTimezone.value);
        const sessionEnd = new TZDate(session.end_datetime, calendarTimezone.value);
        return sessionStart < dayEnd && sessionEnd > dayStart;
    });
});

const fetchSessions = async () => {
    if (!start_date.value || !end_date.value) return;

    const data = await getCalendar(start_date.value, end_date.value, scope.value);
    sessions.value = data;
    setCalendarEvents();

}

const setCalendarEvents = () => {
    calendarEvents.value = sessions.value.map(session => ({
        ...getEventPalette(session.registration_status),
        title: session.event.title,
        start: session.start_datetime,
        end: session.end_datetime,
        classNames: [getEventStatusColor(session.registration_status)],
        extendedProps: { // extension properties to show in event details modal
            session: session,
            registration_status: session.registration_status,
            seat_taken: session.seat_taken,
            seat_capacity: session.seat_capacity
        }
    }));
    calendarOptions.value.events = calendarEvents.value;
};

watch(scope, () => {
    fetchSessions();
})

onMounted(async () => {
    await nextTick();
    syncHeaderFromApi();
});
</script>
<style scoped>
.calendar-custom-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}

.calendar-title {
    font-size: 1.6rem;
    line-height: 1.1;
    font-weight: 800;
    color: var(--color-base-content);
}

/* .calendar-nav-btn {
    width: 48px;
    height: 48px;
    border: 1px solid var(--color-base-300);
    background: color-mix(in oklab, var(--color-base-100) 94%, white);
    color: color-mix(in oklab, var(--color-base-content) 62%, white);
    font-size: 2rem;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.14), 0 1px 2px rgba(15, 23, 42, 0.1);
}
 */

.calendar-view-switch {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 5px;
    border-radius: 12px;
    border: 1px solid color-mix(in oklab, var(--color-base-300) 88%, white);
    background: color-mix(in oklab, var(--color-base-100) 92%, white);
}


.fc {
    font-family: inherit;
}

.calendar-shell {
    border: 1px solid var(--color-base-300);
    overflow: hidden;
}

.fc-theme-standard {
    border: none;
    border-radius: 0;
    overflow: hidden;
    box-shadow: none;
}

.fc .fc-col-header-cell {
    background-color: color-mix(in oklab, var(--color-base-200) 82%, white);
    color: color-mix(in oklab, var(--color-base-content) 52%, white);
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.82rem;
    padding: 16px 4px !important;
    border-bottom: 1px solid var(--color-base-300);
}

.fc .fc-daygrid-day {
    background-color: var(--color-base-100) !important;
    border: 1px solid var(--color-base-200) !important;
    transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.fc .fc-daygrid-day:hover {
    background-color: var(--color-base-200) !important;
}

.fc .fc-daygrid-day.fc-day-other {
    background-color: var(--color-base-100/50) !important;
    opacity: 0.6;
}

.fc .fc-daygrid-day-number {
    padding: 8px 10px;
    font-weight: 500;
    font-size: 0.95rem;
    color: var(--color-base-content);
}

.fc .fc-day-other .fc-daygrid-day-number {
    color: color-mix(in oklab, var(--color-base-content) 35%, white);
}

.fc .fc-daygrid-day-top {
    justify-content: flex-end;
}

.fc .fc-daygrid-day.fc-day-selected {
    box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--color-primary) 35%, white);
    background-color: color-mix(in oklab, var(--color-primary) 6%, var(--color-base-100)) !important;
}

.fc .fc-daygrid-day.fc-day-selected .fc-daygrid-day-number {
    width: 34px;
    height: 34px;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-primary);
    color: var(--color-primary-content);
}

.fc .fc-daygrid-day-frame {
    min-height: 136px;
}

.fc .fc-daygrid-day-events {
    margin: 8px 8px;
}

.fc .fc-header-toolbar {
    background-color: color-mix(in oklab, var(--color-base-100) 96%, white) !important;
    border-bottom: 1px solid var(--color-base-300) !important;
    padding: 0 !important;
    margin: 0 !important;
    min-height: 92px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-inline: 24px !important;
}

.fc .fc-toolbar-chunk {
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

.fc .fc-toolbar-title {
    font-size: 2.6rem;
    font-weight: 900;
    color: var(--color-base-content);
    line-height: 1.1;
}

.fc .fc-button {
    background-color: color-mix(in oklab, var(--color-base-200) 78%, white) !important;
    border: 1px solid var(--color-base-300) !important;
    color: color-mix(in oklab, var(--color-base-content) 78%, white) !important;
    text-transform: capitalize;
    padding: 8px 16px !important;
    font-weight: 600;
    border-radius: 12px !important;
    box-shadow: none !important;
}

.fc .fc-button:hover {
    background-color: color-mix(in oklab, var(--color-base-200) 90%, white) !important;
}

.fc .fc-button-active {
    background-color: var(--color-base-100) !important;
    border-color: color-mix(in oklab, var(--color-primary) 30%, white) !important;
    color: var(--color-primary) !important;
}

.fc .fc-button-group {
    gap: 4px;
    background: color-mix(in oklab, var(--color-base-200) 88%, white);
    padding: 5px;
    border-radius: 14px;
    border: 1px solid color-mix(in oklab, var(--color-base-300) 88%, white);
}

.fc .fc-button-group .fc-button {
    border: none !important;
    background: transparent !important;
    min-width: 78px;
    border-radius: 10px !important;
    font-weight: 700;
    color: color-mix(in oklab, var(--color-base-content) 70%, white) !important;
}

.fc .fc-button-group .fc-button-active {
    background-color: var(--color-base-100) !important;
    color: var(--color-primary) !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.12) !important;
}

.fc .fc-prev-button,
.fc .fc-next-button {
    width: 52px;
    height: 52px;
    padding: 0 !important;
    border-radius: 12px !important;
    background-color: color-mix(in oklab, var(--color-base-200) 88%, white) !important;
    border: 1px solid var(--color-base-300) !important;
    color: color-mix(in oklab, var(--color-base-content) 70%, white) !important;
}

.fc-view {
    background-color: transparent !important;
}

.fc-view-harness {
    border: none !important;
}

.fc .fc-event {
    padding: 7px 12px !important;
    border-radius: 7px !important;
    border: none !important;
    border-left-width: 0 !important;
    cursor: pointer;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease;
}

.fc .fc-event:hover {
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.12);
    transform: translateY(-0.5px);
}

.fc-event.event-confirmed {
    background-color: color-mix(in oklab, var(--color-success) 20%, white) !important;
    border: 1px solid color-mix(in oklab, var(--color-success) 34%, white) !important;
    color: color-mix(in oklab, var(--color-success) 72%, black) !important;
}

.fc-event.event-confirmed .fc-event-title {
    color: color-mix(in oklab, var(--color-success) 72%, black) !important;
}

.fc-event.event-waitlist {
    background-color: color-mix(in oklab, var(--color-warning) 22%, white) !important;
    border: 1px solid color-mix(in oklab, var(--color-warning) 36%, white) !important;
    color: color-mix(in oklab, var(--color-warning) 74%, black) !important;
}

.fc-event.event-waitlist .fc-event-title {
    color: color-mix(in oklab, var(--color-warning) 74%, black) !important;
}

.fc-event.event-available {
    background-color: color-mix(in oklab, var(--color-primary) 16%, white) !important;
    border: 1px solid color-mix(in oklab, var(--color-primary) 32%, white) !important;
    color: color-mix(in oklab, var(--color-primary) 82%, black) !important;
}

.fc-event.event-available .fc-event-title {
    color: color-mix(in oklab, var(--color-primary) 82%, black) !important;
}

.fc-event.event-normal {
    background-color: color-mix(in oklab, var(--color-base-300) 65%, white) !important;
    border: 1px solid var(--color-base-300) !important;
    color: var(--color-base-content) !important;
}

.fc-event.event-normal .fc-event-title {
    color: var(--color-base-content) !important;
}

.fc .fc-event .fc-event-main,
.fc .fc-event .fc-event-time,
.fc .fc-event .fc-event-title {
    color: inherit !important;
}

.fc .fc-daygrid-dot-event {
    border: none !important;
    background-color: inherit !important;
    border-radius: 6px !important;
}

.fc .fc-daygrid-dot-event .fc-event-dot {
    display: none !important;
}

.fc .fc-event-title {
    white-space: nowrap !important;
    word-wrap: normal !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.2;
}

.fc .fc-daygrid-event-harness {
    padding: 0;
    margin: 5px 0;
}

.fc .fc-daygrid-event .fc-event-main,
.fc .fc-daygrid-event .fc-event-main-frame {
    padding: 5px 8px;
}

.fc .fc-timegrid-event .fc-event-main,
.fc .fc-timegrid-event .fc-event-main-frame {
    padding: 6px 8px;
}

.fc .fc-daygrid-event {
    margin: 0 !important;
}

.fc .fc-timegrid-event {
    border-radius: 8px !important;
}

.fc .fc-timegrid-event-harness {
    margin: 0 6px;
}

@media screen and (max-width: 768px) {
    .calendar-title {
        font-size: 1.2rem;
    }

    .calendar-nav-btn {
        width: 42px;
        height: 42px;
        font-size: 1.6rem;
    }

    .calendar-view-btn {
        min-width: 72px;
        height: 36px;
    }

    .fc .fc-toolbar-title {
        font-size: 1.6rem;
    }

    .fc .fc-button {
        padding: 4px 8px !important;
        font-size: 12px !important;
    }

    .fc .fc-header-toolbar {
        min-height: 74px;
        padding-inline: 10px !important;
    }

    .fc .fc-toolbar-chunk {
        gap: 6px;
    }

    .fc .fc-daygrid-day-frame {
        min-height: 92px;
    }

    .fc .fc-daygrid-day-number {
        padding: 4px;
        font-size: 0.82rem;
    }

    .fc .fc-event {
        font-size: 0.68rem !important;
    }

    .fc .fc-col-header-cell {
        padding: 8px 2px !important;
        font-size: 12px;
    }
}

:deep(.fc .fc-daygrid-day) {
    transition: background-color 0.18s ease, box-shadow 0.18s ease;
    cursor: pointer;
}

:deep(.fc .fc-daygrid-day:hover) {
    background-color: color-mix(in oklab, var(--color-primary) 8%, var(--color-base-100)) !important;
}

:deep(.fc .fc-daygrid-day.fc-day-selected) {
    background-color: color-mix(in oklab, var(--color-primary) 12%, var(--color-base-100)) !important;
    box-shadow: inset 0 0 0 2px color-mix(in oklab, var(--color-primary) 50%, white) !important;
}

:deep(.fc .fc-daygrid-day.fc-day-selected .fc-daygrid-day-number) {
    background-color: var(--color-primary) !important;
    color: var(--color-primary-content) !important;
    border-radius: 9999px;
}

:deep(.fc .fc-event) {
    border-radius: 10px !important;
    border-width: 1px !important;
    border-style: solid !important;
    box-shadow: none !important;
    cursor: pointer !important;
}

:deep(.fc .fc-event.event-confirmed) {
    background-color: color-mix(in oklab, var(--color-success) 20%, white) !important;
    border-color: color-mix(in oklab, var(--color-success) 34%, white) !important;
    color: color-mix(in oklab, var(--color-success) 72%, black) !important;
}

:deep(.fc .fc-event.event-waitlist) {
    background-color: color-mix(in oklab, var(--color-warning) 22%, white) !important;
    border-color: color-mix(in oklab, var(--color-warning) 36%, white) !important;
    color: color-mix(in oklab, var(--color-warning) 74%, black) !important;
}

:deep(.fc .fc-event.event-available) {
    background-color: color-mix(in oklab, var(--color-primary) 16%, white) !important;
    border-color: color-mix(in oklab, var(--color-primary) 32%, white) !important;
    color: color-mix(in oklab, var(--color-primary) 82%, black) !important;
}

:deep(.fc .fc-event.event-normal) {
    background-color: color-mix(in oklab, var(--color-base-300) 65%, white) !important;
    border-color: var(--color-base-300) !important;
    color: var(--color-base-content) !important;
}

:deep(.fc .fc-event .fc-event-title),
:deep(.fc .fc-event .fc-event-time),
:deep(.fc .fc-event .fc-event-main) {
    color: inherit !important;
}

:deep(.fc .fc-col-header-cell) {
    background-color: color-mix(in oklab, var(--color-base-200) 82%, white) !important;
    color: color-mix(in oklab, var(--color-base-content) 52%, white) !important;
    border-bottom: 1px solid var(--color-base-300) !important;
}

:deep(.fc .fc-col-header-cell-cushion) {
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: color-mix(in oklab, var(--color-base-content) 52%, white) !important;
}

:deep(.fc .fc-daygrid-day-number) {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--color-base-content) !important;
}

:deep(.fc .fc-daygrid-day-top) {
    justify-content: flex-end !important;
}

:deep(.fc .fc-header-toolbar) {
    background-color: color-mix(in oklab, var(--color-base-100) 96%, white) !important;
    border-bottom: 1px solid var(--color-base-300) !important;
}

:deep(.fc .fc-button) {
    background-color: color-mix(in oklab, var(--color-base-200) 88%, white) !important;
    border: 1px solid var(--color-base-300) !important;
    color: color-mix(in oklab, var(--color-base-content) 78%, white) !important;
}

:deep(.fc .fc-button:hover) {
    background-color: color-mix(in oklab, var(--color-base-200) 94%, white) !important;
}

:deep(.fc .fc-button-group) {
    background: color-mix(in oklab, var(--color-base-200) 90%, white) !important;
    border: 1px solid color-mix(in oklab, var(--color-base-300) 88%, white) !important;
}

:deep(.fc .fc-button-group .fc-button-active) {
    background-color: var(--color-base-100) !important;
    color: var(--color-primary) !important;
    border-color: color-mix(in oklab, var(--color-primary) 30%, white) !important;
}

:deep(.fc .fc-prev-button),
:deep(.fc .fc-next-button) {
    background-color: color-mix(in oklab, var(--color-base-200) 90%, white) !important;
    color: color-mix(in oklab, var(--color-base-content) 70%, white) !important;
    border: 1px solid var(--color-base-300) !important;
}
</style>