<template>
  <div class="min-h-screen bg-base-200">
    <nav class="sticky top-0 z-50 bg-white shadow px-6">
      <div class="flex justify-between items-center h-16">
        <button onclick="my_modal_3.showModal()" class="flex items-center gap-2 text-xl hover:opacity-80">

          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>

          <span class="font-bold text-lg">Create New Event</span>
        </button>
        <dialog id="my_modal_3" class="modal">
          <div class="modal-box">
            <form method="dialog">
              <button class="btn btn-lg btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <h3 class="text-lg font-bold">Leave this page?</h3>
            <p class="py-4">You have unsaved changes. What would you like to do?</p>
            <div class="flex gap-4">
              <button type="button" class="btn btn-primary flex-1 p-4" @click="saveDraftAndLeave">
                Save as draft & leave
              </button>

              <button type="button" @click="goToDashboard" class="btn flex-1">
                Leave without saving
              </button>
            </div>
          </div>
        </dialog>

      </div>
    </nav>

    <div class="max-w-4xl mx-auto p-2 space-y-6 pb-24">
      <div class="card bg-base-100 shadow">
        <div class="card-body">
          <h2 class="card-title">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
            </svg>
            Event Details
          </h2>

          <div class="grid md:grid-cols-2 gap-4">

            <div class="md:col-span-2">
              <span>Event Title</span>
              <span class="text-red-500"> *</span>
              <input ref="titleInput" v-model="event.title" type="text" class="input input-bordered w-full" required />
              <p v-if="submitted && !event.title.trim()" class="text-red-500 text-sm mt-1">
                Event title is required.
              </p>
            </div>

            <div class="md:col-span-2">
              <span>Location</span>
              <span class="opacity-60"> (optional)</span>
              <input v-model="event.location" type="text" class="input input-bordered w-full" />
            </div>

            <div class="md:col-span-2">
              <span>Description</span>
              <span class="opacity-60"> (optional)</span>
              <textarea v-model="event.description" class="textarea textarea-bordered w-full"></textarea>
            </div>

          </div>
        </div>
      </div>

      <!-- Session -->
      <div ref="sessionManagementRef" class="bg-base-100 shadow p-6 rounded-lg">
        <div class="flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-5 inline">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <span class="text-lg font-semibold inline">Session Management</span>

          </div>

          <div class="flex items-center gap-3 px-3 py-1.5 rounded-lg border border-base-300">
            <input type="checkbox" v-model="limitEnabled" class="toggle toggle-primary" />
            <span class="text-md font-normal flex-1">
              Max sessions per participant
              <span class="text-sm opacity-40 font-normal">(optional)</span>
            </span>
            <div class="flex flex-wrap items-center gap-x-1">
              <div class="w-px h-8 bg-base-300"></div>
              <div class="flex items-center gap-2">
                <input type="number" pattern="[0-9]*" inputmode="numeric" v-model="limit"
                  :min="limitEnabled ? 1 : undefined" :disabled="!limitEnabled" @input="onLimitInput"
                  class="input input-bordered w-14 validator" />
              </div>
            </div>
          </div>
        </div>


        <!-- Timezone -->
        <div class="flex items-center justify-center p-1 rounded-lg mt-4
            bg-blue-50 dark:bg-blue-900/20
            text-blue-700 dark:text-blue-300
            border border-blue-100 dark:border-blue-800
            text-xs font-medium">
          <span class="text-xs mr-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="size-5">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
            </svg>

          </span>
          All times are in {{ timezoneLabel }}
        </div>

        <div class="p-0 mt-3">

          <!-- Add session -->
          <div class="border border-dashed p-6 rounded-xl space-y-3">
            <h2 class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>

              Add New Session
            </h2>

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">

              <!-- Start -->
              <div class="flex flex-col">
                <label class="text-sm ">Start</label>
                <input type="datetime-local" v-model="newSession.start" :min="minStartDateTime"
                  class="input input-bordered w-full" />
              </div>

              <!-- End -->
              <div class="flex flex-col">
                <label class="text-sm">End</label>
                <input type="datetime-local" v-model="newSession.end" :min="newSession.start"
                  class="input input-bordered w-full" />
              </div>


              <!-- Capacity -->
              <div>
                <span class="text-sm">Seat capacity</span>
                <span class="text-sm opacity-60"> (optional)</span>
                <input type="number" v-model="newSession.capacity" placeholder="e.g. 30" min="1" @input="newSession.capacity = $event.target.value === ''
                  ? null
                  : Math.max(1, Number($event.target.value))" class="input input-bordered w-full validator" />
              </div>
            </div>
            <!-- Location -->
            <div>
              <span class="text-sm">Location</span>
              <span class="text-sm opacity-60"> (optional)</span>
              <input type="text" v-model="newSession.location" placeholder="e.g. Room 101"
                class="input input-bordered w-full" />
            </div>




            <div class="card bg-base-100 shadow p-4 space-y-4">
              <h2 class="card-title flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>

                Repeat session
              </h2>

              <p v-if="isEditing" class="text-xs opacity-60">
                Repeat settings are locked while editing a session.
              </p>

              <fieldset :disabled="isEditing" class="space-y-4">

              <!-- content -->
              <div class="grid md:grid-cols-3 gap-3">
                <div>
                  <select class="select select-bordered w-full" v-model="repeatsChoose.type">
                    <option value="Does not repeat">Does not repeat</option>
                    <option value="Daily">Daily</option>
                    <option value="Weekly">Weekly</option>
                    <option value="Monthly">Monthly</option>
                    <option value="Yearly">Yearly</option>
                  </select>
                </div>
                <div>
                  <input type="number" min="1" v-model="repeatsChoose.interval" :placeholder="repeatsChoose.type === 'Does not repeat' || !repeatsChoose.type
                    ? 'Repeat interval if repeat session'
                    : repeatsChoose.type === 'Daily' ? 'Every N day(s)'
                      : repeatsChoose.type === 'Weekly' ? 'Every N week(s)'
                        : repeatsChoose.type === 'Monthly' ? 'Every N month(s)'
                          : repeatsChoose.type === 'Yearly' ? 'Every N year(s)'
                            : 'Interval'" class="input input-bordered w-full"
                    :disabled="!repeatsChoose.type || repeatsChoose.type === 'Does not repeat'" />
                </div>
                <div class="text-sm p-2">
                  <!-- เปิด/ปิด -->
                  <label class="flex items-center gap-2">
                    <input type="checkbox" v-model="repeatEndEnabled"
                      :disabled="!repeatsChoose.type || repeatsChoose.type === 'Does not repeat'"
                      class="checkbox checkbox-success checkbox-sm" />
                    <span class="font-semibold">Repeat until</span>
                  </label>

                  <!-- โผล่เมื่อเปิด -->
                  <div v-if="repeatEndEnabled" class="mt-3 space-y-3">

                    <!-- เลือก type -->
                    <div class="flex gap-4 items-center">
                      <label class="flex items-center gap-2">
                        <input type="radio" value="date" v-model="repeatEnd.type" />
                        <span>Until date</span>
                      </label>
                    </div>
                    <div>
                      <label class="flex items-center gap-2">
                        <input type="radio" value="count" v-model="repeatEnd.type" />
                        <span>Number of times</span>
                      </label>
                    </div>

                    <!-- input ตาม type -->
                    <input v-if="repeatEnd.type === 'date'" type="date" v-model="repeatEnd.date"
                      class="input input-bordered w-full" />

                    <input v-if="repeatEnd.type === 'count'" type="number" min="1" max="100" v-model.number="repeatEnd.count"
                      placeholder="Number of times" pattern="[0-9]*" class="input input-bordered w-full validator" />
                    <p v-if="repeatCountError" class="text-error text-xs mt-1">
                      {{ repeatCountError }}
                    </p>
                  </div>
                </div>
              </div>
              </fieldset>
            </div>

            <div class="flex gap-2">
              <button v-if="isEditing" class="btn flex-1" @click="cancelEdit">
                Cancel
              </button>

              <button class="btn btn-primary flex-1" @click="isEditing ? saveEdit() : addSession()">
                {{ isEditing ? "Save Edit" : "Add Session" }}
              </button>
            </div>
          </div>

          <!-- Divider -->
          <div v-if="sessions.length" class="mt-4">
            <div class="relative py-2">
              <div aria-hidden="true" class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-slate-200 dark:border-slate-800"></div>
              </div>
              <div class="relative flex justify-center">
                <span class="bg-base-100 px-3 text-sm font-medium opacity-60">
                  Added Sessions ({{ sessions.length }})
                </span>
              </div>
            </div>
            <div class="flex flex-col gap-4">
              <div v-for="(s, index) in paginatedSessions" :key="(currentPage - 1) * pageSize + index"
                class="group relative flex flex-col sm:flex-row items-center gap-4 p-4 rounded-lg border border-base-300 bg-base-200 hover:border-primary/50 transition-colors">

                <!-- LEFT -->
                <div class="flex-1 min-w-0 w-full">
                  <div class="flex flex-col gap-2">


                    <!-- TIME -->
                    <div class="flex items-center gap-2 text-base font-semibold">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                          d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                      </svg>
                      <span>{{ formatDate(s.start) }}, {{ formatTime(s.start) }} – {{ formatDate(s.end) }} ,{{
                        formatTime(s.end) }}</span>
                    </div>

                    <!-- LOCATION -->
                    <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm opacity-60">
                      <span v-if="getEffectiveSessionLocation(s)" class="flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                        </svg>

                        {{ getEffectiveSessionLocation(s) }}
                      </span>
                      <span v-if="getEffectiveSessionLocation(s) && s.capacity != null" class="opacity-40">|</span>

                      <!-- SEATS -->
                      <span v-if="s.capacity != null" class="flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                          stroke="currentColor" class="size-6">
                          <path stroke-linecap="round" stroke-linejoin="round"
                            d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                        </svg>
                        {{ s.capacity }} seats
                      </span>


                    </div>

                  </div>
                </div>

                <!-- RIGHT -->
                <div class="flex items-center gap-2 self-end sm:self-center shrink-0">
                  <div class="flex items-center gap-2">
                    <template v-if="activeCopyIndex === (currentPage - 1) * pageSize + index">
                      <input v-if="activeCopyIndex === (currentPage - 1) * pageSize + index" ref="copyInput"
                        type="number" v-model.number="copyCount" min="1" class="input input-bordered w-20" />
                      <button v-if="activeCopyIndex === (currentPage - 1) * pageSize + index"
                        class="btn btn-sm btn-primary" @click="confirmCopy(s)">
                        Duplicate
                      </button>
                    </template>
                    <svg xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-blue-500"
                      @click="handleCopyClick(s, (currentPage - 1) * pageSize + index)" fill="none" viewBox="0 0 24 24"
                      stroke-width="1.5" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                    </svg>
                  </div>

                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6" @click="editSession(s, (currentPage - 1) * pageSize + index)">
                    <path stroke-linecap=" round" stroke-linejoin="round"
                      d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                  </svg>

                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6" @click="removeSession((currentPage - 1) * pageSize + index)">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                  </svg>

                </div>
              </div>
            </div>
            <div v-if="pageCount > 1" class="mt-4 flex items-center justify-between w-full">
                <button class="btn btn-sm btn-ghost" @click="prev" :disabled="isFirstPage">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-4 mr-1">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                  </svg>
                  Prev
                </button>
                <button class="btn btn-sm btn-ghost" @click="next" :disabled="isLastPage">
                  Next
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-4 ml-1">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                  </svg>
                </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="fixed bottom-0 left-0 w-full z-20">
      <div
        class="bg-base-100 border-t border-base-300 p-4 pointer-events-auto flex justify-end gap-3 px-10 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <button @click="showDiscardModal = true" class="btn">
          Discard changes
        </button>
        <!-- Discard Modal -->
        <div v-if="showDiscardModal"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/20 backdrop-blur-[2px]"
          @click.self="showDiscardModal = false">
          <div class="bg-base-100 rounded-2xl shadow-xl w-full max-w-sm overflow-hidden border border-base-300">
            <div class="p-8 flex flex-col items-center text-center">

              <!-- Icon -->
              <div class="w-12 h-12 rounded-full bg-warning/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6 text-warning">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
                </svg>
              </div>

              <h3 class="text-xl font-bold mb-2">Discard Changes?</h3>
              <p class="text-sm opacity-60 mb-8 leading-relaxed">
                Are you sure you want to discard your changes? All unsaved information will be lost.
              </p>

              <div class="flex gap-3 w-full">
                <button class="flex-1 btn btn-outline rounded-full" @click="showDiscardModal = false">
                  Keep Editing
                </button>
                <button class="flex-1 btn rounded-full bg-red-400 hover:bg-red-500 text-white border-none"
                  @click="discardChanges">
                  Discard
                </button>
              </div>
            </div>
          </div>
        </div>

        <button @click="submit" class="btn btn-primary">
          Create Event
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed, onMounted } from "vue"
import { useRouter } from 'vue-router'
import { createEvent } from "@/services/event"
import { TZDate } from '@date-fns/tz'
import { useAuthStore } from "@/store/authStore"
import { format } from "date-fns"
import { RRule } from "rrule"
import { useOffsetPagination } from '@vueuse/core'

const router = useRouter()
const isEditing = ref(false)
const editingIndex = ref(null)
const submitted = ref(false)
const titleInput = ref(null)
const showDiscardModal = ref(false)
const authStore = useAuthStore()
const sessions = ref([])

onMounted(() => {
  if (!authStore.user) {
    authStore.updateUser()
  }
})

const pageSize = 10

const {
  currentPage,
  pageCount,
  isFirstPage,
  isLastPage,
  prev,
  next,
} = useOffsetPagination({
  total: computed(() => sessions.value.length),
  page: 1,
  pageSize,
})

// Reset to page 1 whenever sessions list changes length
watch(() => sessions.value.length, () => {
  // If current page is now beyond available pages, clamp to last page
  if (currentPage.value > pageCount.value && pageCount.value > 0) {
    currentPage.value = pageCount.value
  }
})

const paginatedSessions = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return sessions.value.slice(start, start + pageSize)
})

const timezoneLabel = computed(() =>
  authStore.user?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone
)
const eventTimezone = computed(() => timezoneLabel.value)


const minStartDateTime = computed(() => {
  const nowTz = new TZDate(new Date(), eventTimezone.value)

  const pad = (n) => String(n).padStart(2, "0")

  return `${nowTz.getFullYear()}-${pad(nowTz.getMonth() + 1)}-${pad(nowTz.getDate())}T${pad(nowTz.getHours())}:${pad(nowTz.getMinutes())}`
})


function toTZDate(value) {
  if (!value) return null

  try {
    if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(value)) {
      return parseDatetimeLocal(value, eventTimezone.value)
    }
    if (value instanceof Date) {
      return new TZDate(value, eventTimezone.value)
    }

    return null
  } catch {
    return null
  }
}


const formatLocalDateTime = (value) => {
  if (typeof value === "string" && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(value)) {
    return parseDatetimeLocal(value, eventTimezone.value).toISOString()
  }

  const tzDate = toTZDate(value)
  return tzDate ? tzDate.toISOString() : null
}

const trimFields = () => {
  if (event.value.title != null) {
    event.value.title = event.value.title.trim()
  }
  if (event.value.location != null) {
    event.value.location = event.value.location.trim()
  }
  if (event.value.description != null) {
    event.value.description = event.value.description.trim()
  }
}

const isBlank = (value) => typeof value === "string" && value.trim().length === 0

const getEffectiveSessionLocation = (session) => {
  const sessionLocation = typeof session?.location === "string" ? session.location.trim() : ""
  if (sessionLocation) return sessionLocation

  return typeof event.value?.location === "string" ? event.value.location.trim() : ""
}


const handleCancel = () => {
  event.value = {
    title: "",
    location: "",
    description: ""
  }

  // reset limit
  limitEnabled.value = false
  limit.value = null

  // reset sessions
  sessions.value = []

  // reset form session
  newSession.value = {
    start: "",
    end: "",
    capacity: "",
    location: "",
    description: ""
  }

  // reset repeat
  repeatEndEnabled.value = false
  repeatEnd.value = {
    type: "never",
    date: "",
    count: null
  }

  repeatsChoose.value = {
    type: "Does not repeat",
    interval: ""
  }

  editingIndex.value = null
}

const goToDashboard = () => {
  router.push("/dashboard")
}

const discardChanges = () => {
  handleCancel()
  resetForm()
  showDiscardModal.value = false
}


const event = ref({
  title: "",
  location: "",
  description: ""
})

const limitEnabled = ref(false)
const limit = ref(null)
watch(limitEnabled, (val) => {
  if (val) {
    limit.value = 1
  } else {
    limit.value = null
  }
})

const newSession = ref({
  start: "",
  end: "",
  capacity: null,
  location: "",
  desc: ""
})

const repeatEndEnabled = ref(false)

const repeatEnd = ref({
  type: "never",
  date: "",
  count: null
})

const repeatCountError = computed(() => {
  if (!repeatEndEnabled.value || repeatEnd.value.type !== "count") return ""

  const rawCount = repeatEnd.value.count
  const parsedCount = Number(rawCount)

  if (rawCount === null || rawCount === "" || Number.isNaN(parsedCount)) {
    return "Please enter number of times."
  }
  if (!Number.isInteger(parsedCount) || parsedCount < 1) {
    return "Number of times must be at least 1."
  }
  if (parsedCount > 100) {
    return "You can only repeat up to 100 sessions at a time."
  }

  return ""
})

const repeatsChoose = ref({
  type: "Does not repeat",
  interval: "",
})

const copyCount = ref(1)
const activeCopyIndex = ref(null)
const copyInput = ref(null)
const sessionManagementRef = ref(null)

const handleCopyClick = async (session, index) => {
  if (activeCopyIndex.value === index) {
    activeCopyIndex.value = null
    return
  }

  activeCopyIndex.value = index
  copyCount.value = 1

  await nextTick()
  const inputElement = Array.isArray(copyInput.value) ? copyInput.value[0] : copyInput.value
  inputElement?.focus()
}

const confirmCopy = (session) => {
  if (!copyCount.value || copyCount.value < 1) return

  for (let i = 0; i < copyCount.value; i++) {
    sessions.value.push({ ...session })
  }

  activeCopyIndex.value = null
}

function saveEdit() {
  if (editingIndex.value == null || editingIndex.value < 0 || editingIndex.value >= sessions.value.length) {
    resetForm()
    return
  }

  if (!newSession.value.start || !newSession.value.end) {
    alert("Please provide both start and end times.")
    return
  }
  if (newSession.value.start >= newSession.value.end) {
    alert("End time must be after start time.")
    return
  }

  const startDate = parseDatetimeLocal(newSession.value.start, eventTimezone.value)
  const endDate = parseDatetimeLocal(newSession.value.end, eventTimezone.value)

  sessions.value.splice(editingIndex.value, 1, {
    ...sessions.value[editingIndex.value],
    ...newSession.value,
    start: startDate,
    end: endDate,
  })

  resetForm()
}

function cancelEdit() {

  resetForm()
}

async function editSession(s, index) {
  newSession.value = {
    ...s,
    start: formatForDateTimeLocalInput(s.start),
    end: formatForDateTimeLocalInput(s.end)
  }
  isEditing.value = true
  editingIndex.value = index

  await nextTick()
  sessionManagementRef.value?.scrollIntoView({
    behavior: "smooth",
    block: "start"
  })
}


// --- SESSION ACTIONS ---
function addSession() {
  if (!newSession.value.start || !newSession.value.end) {
    alert("Please provide both start and end times.")
    return
  }
  if (newSession.value.start >= newSession.value.end) {
    alert("End time must be after start time.")
    return
  }

  // Parse the local datetime strings strictly into TZDate objects
  const startDate = parseDatetimeLocal(newSession.value.start, eventTimezone.value)
  const endDate = parseDatetimeLocal(newSession.value.end, eventTimezone.value)

  // Safe validation using exact object comparison
  const now = parseDatetimeLocal(format(new Date(), "yyyy-MM-dd'T'HH:mm"), eventTimezone.value)
  if (startDate < now) {
    alert("A new session's start time cannot be before the current time.")
    return
  }

  const type = repeatsChoose.value.type
  const interval = Number(repeatsChoose.value.interval) || 1

  if (type !== "Does not repeat" && repeatEndEnabled.value) {
    if (!["date", "count"].includes(repeatEnd.value.type)) {
      alert("Please choose Repeat until option: Until date or Number of times.")
      return
    }

    if (repeatEnd.value.type === "count" && repeatCountError.value) {
      alert(repeatCountError.value)
      return
    }

    if (repeatEnd.value.type === "date" && !repeatEnd.value.date) {
      alert("Please select an until date for repeat session.")
      return
    }
  }

  if (type === "Does not repeat") {
    sessions.value.push({
      ...newSession.value,
      start: startDate,
      end: endDate,
    })
  } else {
    const freqMap = {
      Daily: RRule.DAILY,
      Weekly: RRule.WEEKLY,
      Monthly: RRule.MONTHLY,
      Yearly: RRule.YEARLY,
    }

    const ruleOptions = {
      freq: freqMap[type],
      interval,
      dtstart: new Date(startDate),
    }

    const effectiveRepeatEndType = repeatEndEnabled.value ? repeatEnd.value.type : "never"

    if (effectiveRepeatEndType === "count") {
      ruleOptions.count = Number(repeatEnd.value.count)
    } else if (effectiveRepeatEndType === "date" && repeatEnd.value.date) {
      ruleOptions.until = new Date(parseDatetimeLocal(`${repeatEnd.value.date}T23:59`, eventTimezone.value))
    } else {
      ruleOptions.count = 100
    }

    const toDateTimeLocalString = (dateObj) => {
      const pad = (n) => String(n).padStart(2, "0")
      return `${dateObj.getUTCFullYear()}-${pad(dateObj.getUTCMonth() + 1)}-${pad(dateObj.getUTCDate())}T${pad(dateObj.getUTCHours())}:${pad(dateObj.getUTCMinutes())}`
    }

    const toLocalDateString = (dateObj) => {
      const pad = (n) => String(n).padStart(2, "0")
      return `${dateObj.getUTCFullYear()}-${pad(dateObj.getUTCMonth() + 1)}-${pad(dateObj.getUTCDate())}`
    }

    const rule = new RRule(ruleOptions)
    const occurrenceStarts = rule.all()
    const boundedOccurrenceStarts = occurrenceStarts.filter((occurrenceStart) => {
      if (!(effectiveRepeatEndType === "date" && repeatEnd.value.date)) return true
      return toLocalDateString(occurrenceStart) <= repeatEnd.value.date
    })
    const durationMs = endDate.getTime() - startDate.getTime()

    boundedOccurrenceStarts.forEach((occurrenceStart) => {
      const occurrenceStartTz = parseDatetimeLocal(toDateTimeLocalString(occurrenceStart), eventTimezone.value)
      sessions.value.push({
        ...newSession.value,
        start: occurrenceStartTz,
        end: new Date(occurrenceStartTz.getTime() + durationMs),
        recurring: type
      })
    })
  }

  resetForm()
}

function parseDatetimeLocal(dateStr, timezone) {
  const [datePart, timePart] = dateStr.split("T")
  const [year, month, day] = datePart.split("-").map(Number)
  const [hour, minute] = timePart.split(":").map(Number)

  return new TZDate(year, month - 1, day, hour, minute, 0, timezone)
}

function formatForDateTimeLocalInput(value) {
  const tzDate = toTZDate(value)
  if (!tzDate) return ""

  return format(tzDate, "yyyy-MM-dd'T'HH:mm")
}


function formatDate(dateObj) {
  if (!dateObj) return '';
  return format(dateObj, 'MMM d, yyyy');
}
function formatTime(dateObj) {
  if (!dateObj) return '';
  return format(dateObj, 'hh:mm a');
}

const saveDraftAndLeave = async () => {
  trimFields()

  const payload = {
    title: event.value.title,
    location: event.value.location,
    description: event.value.description,
    max_sessions_per_user: limitEnabled.value ? limit.value : null,
    is_draft: true,
    sessions: sessions.value.map(s => ({
      start_datetime: formatLocalDateTime(s.start),
      end_datetime: formatLocalDateTime(s.end),
      timezone: eventTimezone.value,
      location: getEffectiveSessionLocation(s),
      seat_capacity: s.capacity ? Number(s.capacity) : null
    }))
  }

  try {
    await createEvent(payload)

    const modal = document.getElementById("my_modal_3")
    modal?.close()

    router.push('/events')
  } catch (err) {
    console.error("Save draft failed:", err)
  }
}

function resetForm() {
  newSession.value = {
    start: "",
    end: "",
    capacity: null,
    location: "",
    desc: ""
  }

  repeatsChoose.value = {
    type: "Does not repeat",
    interval: ""
  }

  repeatEnd.value = {
    type: "never",
    date: "",
    count: null
  }

  repeatEndEnabled.value = false

  isEditing.value = false
  editingIndex.value = null
}

function removeSession(index) {
  sessions.value.splice(index, 1)
}

const submit = async () => {
  submitted.value = true
  trimFields()
  if (!event.value.title || isBlank(event.value.title)) {
    titleInput.value?.scrollIntoView({ behavior: 'smooth', block: 'center' })
    titleInput.value?.focus()
    return
  }
  const payload = {
    title: event.value.title,
    location: event.value.location,
    description: event.value.description,
    max_sessions_per_user: limitEnabled.value ? limit.value : null,
    is_draft: false,
    sessions: sessions.value.map(s => ({
      start_datetime: formatLocalDateTime(s.start),
      end_datetime: formatLocalDateTime(s.end),
      timezone: eventTimezone.value,
      location: getEffectiveSessionLocation(s),
      seat_capacity: s.capacity ? Number(s.capacity) : null
    }))
  }

  console.log("Payload:", payload)

  try {
    const createdEvent = await createEvent(payload)
    const eventUuid = createdEvent?.share_uuid || createdEvent?.uuid || createdEvent?.event_uuid

    if (eventUuid) {
      router.push(`/event/overview/${eventUuid}`)
    } else {
      router.push('/events')
    }
  } catch (err) {
    console.error("Create event failed:", err)
  }
}




</script>