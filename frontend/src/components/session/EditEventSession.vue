<template>
  <!-- Session List -->
  <div class="space-y-3">
    <div v-if="sessions.length === 0" class="text-center py-10 bg-base-200/50 rounded-xl border border-dashed border-base-300">
      <p class="text-base-content/60 font-medium">No sessions added yet.</p>
      <p class="text-xs text-base-content/40 mt-1">Add at least one session so users can register.</p>
    </div>

    <!-- DIVIDER -->
    <div v-if="newlyAddedSessions.length > 0 && existingSessions.length > 0" class="divider my-6 font-semibold text-primary">Newly Added Sessions</div>

    <!-- Sessions List -->
    <div class="flex flex-col gap-4">
      <!-- NEWLY ADDED SESSIONS -->
      <div v-if="newlyAddedSessions.length > 0" class="space-y-4">
        <div v-for="(s, index) in displayedNewSessions" :key="'new-' + getAbsoluteNewIndex(index)"
        class="group relative flex flex-col sm:flex-row items-center gap-4 p-4 rounded-lg border border-base-300 bg-base-200 hover:border-primary/50 transition-colors"
        :class="isSessionEnded(s.end) ? 'opacity-60 grayscale' : ''">

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
              <span>{{ formatDate(s.start) }}, {{ formatTime(s.start) }} – {{ formatDate(s.end) }}, {{ formatTime(s.end) }}</span>
            </div>

            <!-- LOCATION -->
            <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm opacity-60">
              <span v-if="s.location || eventLocation" class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                </svg>

                {{ s.location || eventLocation }}
              </span>
              <span v-if="(s.location || eventLocation) && s.capacity != null" class="opacity-40">|</span>

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
            <template v-if="activeCopyIndex === getAbsoluteNewIndex(index)">
              <input v-if="activeCopyIndex === getAbsoluteNewIndex(index)" ref="copyInput" type="number" v-model.number="duplicateCount"
                min="1" class="input input-bordered w-20" />
              <button v-if="activeCopyIndex === getAbsoluteNewIndex(index)" class="btn btn-sm btn-primary" @click="confirmDuplicateInline">Duplicate</button>
            </template>
            <svg v-if="!isSessionEnded(s.end)" xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-blue-500"
              @click="handleCopyClick(s, getAbsoluteNewIndex(index))" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
            </svg>
          </div>

          <svg v-if="!isSessionEnded(s.end)" xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-blue-500"
            @click="openEditModal(s, getAbsoluteNewIndex(index))" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
          </svg>

          <svg v-if="!isSessionEnded(s.end)" xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-red-500"
            @click="removeSession(getAbsoluteNewIndex(index))" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
          </svg>

        </div>
      </div>

      <!-- Pagination for Newly Added Sessions -->
      <div v-if="shouldShowNewPagination" class="flex justify-between items-center bg-base-100 border border-base-200 p-2 rounded-xl mt-4">
        <button class="btn btn-sm btn-ghost" @click="localPageIndexNew > 0 && localPageIndexNew--" :disabled="isNewPrevDisabled">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 mr-1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>
          Prev
        </button>
        <span class="text-sm font-semibold text-base-content/70">Page {{ displayedNewPageNumber }}</span>
        <button class="btn btn-sm btn-ghost" @click="localPageIndexNew < newSessionsPageSize - 1 && localPageIndexNew++" :disabled="isNewNextDisabled">
          Next
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 ml-1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Add New Session Button (Triggers Modal) -->
    <button @click="openAddModal" class="btn btn-outline btn-block border-dashed border-2 hover:bg-base-200 hover:text-base-content mt-4 h-auto py-4">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <span class="text-lg">Add New Session</span>
    </button>

    <!-- DIVIDER -->
    <div v-if="newlyAddedSessions.length > 0 && existingSessions.length > 0" class="divider my-6 font-semibold text-primary">Existing Sessions</div>

    <!-- EXISTING SESSIONS -->
    <div v-if="existingSessions.length > 0" class="space-y-4">
      <div v-for="(s, index) in displayedExistingSessions" :key="'existing-' + s.uuid"
        class="group relative flex flex-col sm:flex-row items-center gap-4 p-4 rounded-lg border border-base-300 bg-base-200 hover:border-primary/50 transition-colors"
        :class="isSessionEnded(s.end) ? 'opacity-60 grayscale' : ''">

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
              <span>{{ formatDate(s.start) }}, {{ formatTime(s.start) }} – {{ formatDate(s.end) }}, {{ formatTime(s.end) }}</span>
            </div>

            <!-- LOCATION -->
            <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm opacity-60">
              <span v-if="s.location || eventLocation" class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                </svg>

                {{ s.location || eventLocation }}
              </span>
              <span v-if="(s.location || eventLocation) && s.capacity != null" class="opacity-40">|</span>

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
            <template v-if="activeCopyIndex === getAbsoluteExistingIndex(index)">
              <input v-if="activeCopyIndex === getAbsoluteExistingIndex(index)" ref="copyInput" type="number" v-model.number="duplicateCount"
                min="1" class="input input-bordered w-20" />
              <button v-if="activeCopyIndex === getAbsoluteExistingIndex(index)" class="btn btn-sm btn-primary" @click="confirmDuplicateInline">Duplicate</button>
            </template>
            <svg v-if="!isSessionEnded(s.end)" xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-blue-500"
              @click="handleCopyClick(s, getAbsoluteExistingIndex(index))" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
            </svg>
          </div>

          <svg v-if="!isSessionEnded(s.end)" xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-blue-500"
            @click="openEditModal(s, getAbsoluteExistingIndex(index))" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
          </svg>

          <svg v-if="!isSessionEnded(s.end)" xmlns="http://www.w3.org/2000/svg" class="size-6 cursor-pointer hover:text-red-500"
            @click="removeSession(getAbsoluteExistingIndex(index))" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>

          </div>
        </div>
      </div>

      <!-- Pagination for Existing Sessions -->
      <div v-if="shouldShowExistingPagination" class="flex justify-between items-center bg-base-100 border border-base-200 p-2 rounded-xl mt-4">
        <button class="btn btn-sm btn-ghost" @click="goPrev" :disabled="isExistingPrevDisabled">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 mr-1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>
          Prev
        </button>
        <span class="text-sm font-semibold text-base-content/70">Page {{ displayedExistingPageNumber }}</span>
        <button class="btn btn-sm btn-ghost" @click="goNext" :disabled="isExistingNextDisabled">
          Next
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4 ml-1">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </button>
      </div>
    </div>
    
  </div>

  <!-- ========================================== -->
  <!-- SESSION MODAL                              -->
  <!-- ========================================== -->
  <dialog id="session_modal" class="modal" ref="sessionModalRef">
    <div class="modal-box w-11/12 max-w-2xl bg-base-100 p-0 overflow-hidden">
      
      <!-- Modal Header -->
      <div class="bg-base-200 px-6 py-4 border-b border-base-300 flex justify-between items-center">
        <h3 class="font-bold text-lg flex items-center gap-2">
          {{ isEditing ? 'Edit Session' : 'Add New Session' }}
        </h3>
        <button @click="closeSessionModal" class="btn btn-sm btn-circle btn-ghost">✕</button>
      </div>
      
      <!-- Modal Body -->
      <div class="p-6 space-y-5">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Start -->
          <div>
            <label class="label pt-0 pb-1"><span class="label-text font-semibold">Start Time ({{ userTimezone }})</span></label>
            <input type="datetime-local" v-model="newSession.start" class="input input-bordered w-full focus:input-primary" />
          </div>

          <!-- End -->
          <div>
            <label class="label pt-0 pb-1"><span class="label-text font-semibold">End Time ({{ userTimezone }})</span></label>
            <input type="datetime-local" v-model="newSession.end" class="input input-bordered w-full focus:input-primary" />
          </div>

          <!-- Capacity -->
          <div>
            <label class="label pt-0 pb-1"><span class="label-text font-semibold">Seat Capacity</span></label>
            <input 
              type="number" 
              v-model="newSession.capacity" 
              placeholder="Unlimited if empty" 
              min="1" 
              @input="newSession.capacity = $event.target.value === '' ? null : Math.max(1, Number($event.target.value))" 
              class="input input-bordered w-full focus:input-primary" 
            />
          </div>

          <!-- Location -->
          <div>
            <label class="label pt-0 pb-1"><span class="label-text font-semibold">Location <span class="opacity-60 font-normal">(optional)</span></span></label>
            <input type="text" v-model="newSession.location" placeholder="Specific room/link" class="input input-bordered w-full focus:input-primary" />
          </div>
        </div>

        <!-- Repeat Settings (Hidden if Editing to prevent complex logic clashes, optional to show) -->
        <div v-if="!isEditing" class="bg-base-200/50 rounded-xl p-4 border border-base-200 mt-4">
          <h4 class="font-bold text-sm mb-3 flex items-center gap-1">
            Repeat Setup
          </h4>
          
          <div class="grid sm:grid-cols-2 gap-4">
            <select class="select select-bordered w-full" v-model="repeatsChoose.type">
              <option value="Does not repeat">Does not repeat</option>
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Monthly">Monthly</option>
              <option value="Yearly">Yearly</option>
            </select>

            <input 
              type="number" 
              min="1" 
              v-model="repeatsChoose.interval" 
              :placeholder="repeatsChoose.type !== 'Does not repeat' ? `Every X ${repeatsChoose.type.toLowerCase()}` : 'Every X'" 
              class="input input-bordered w-full"
              :disabled="repeatsChoose.type === 'Does not repeat'" 
            />
          </div>

          <div v-if="repeatsChoose.type !== 'Does not repeat'" class="mt-4 pt-4 border-t border-base-300">
            <h4 class="font-semibold text-sm mb-3">End Limit <span class="text-error">*</span></h4>

            <div class="grid sm:grid-cols-2 gap-4 bg-base-100 p-3 rounded-lg border border-base-200">
              <div class="space-y-2">
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="date" v-model="repeatEnd.type" class="radio radio-primary radio-sm" /> Until Date
                </label>
                <label class="flex items-center gap-2 text-sm cursor-pointer">
                  <input type="radio" value="count" v-model="repeatEnd.type" class="radio radio-primary radio-sm" /> Number of times
                </label>
              </div>
              
              <div class="flex items-center">
                <input v-if="repeatEnd.type === 'date'" type="date" v-model="repeatEnd.date" class="input input-bordered input-sm w-full" />
                <input v-if="repeatEnd.type === 'count'" type="number" min="1" v-model="repeatEnd.count" placeholder="Ex: 5 times" class="input input-bordered input-sm w-full" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="bg-base-200 px-6 py-4 border-t border-base-300 flex justify-end gap-3 rounded-b-xl">
        <button class="btn btn-ghost" @click="closeSessionModal">Cancel</button>
        <button class="btn btn-primary px-8" @click="isEditing ? saveEdit() : addSession()">
          {{ isEditing ? "Save Session" : "Add Session" }}
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click="closeSessionModal">close</button>
    </form>
  </dialog>

  <!-- ========================================== -->
  <!-- DUPLICATE SESSION MODAL                    -->
  <!-- ========================================== -->
  <dialog id="duplicate_modal" class="modal" ref="duplicateModalRef">
    <div class="modal-box max-w-sm">
      <form method="dialog">
        <button @click="closeDuplicateModal" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
      </form>
      <h3 class="font-bold text-lg mb-4">Duplicate Session</h3>
      <p class="text-sm text-base-content/70 mb-4">How many copies of this session would you like to create?</p>
      <div class="form-control mb-4">
        <input type="number" v-model="duplicateCount" min="1" max="50" class="input input-bordered w-full" />
      </div>
      <div class="modal-action">
        <button class="btn btn-ghost" @click="closeDuplicateModal">Cancel</button>
        <button class="btn btn-primary" @click="confirmDuplicate">Duplicate</button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click="closeDuplicateModal">close</button>
    </form>
  </dialog>
</template>

<script setup>
import { ref, computed } from "vue"
import { getSessions } from '@/services/event.js'
import { format, addDays, addWeeks, addMonths, addYears } from "date-fns"
import { TZDate } from "@date-fns/tz"

const props = defineProps({
  eventId: String,
  eventLocation: String,
  userTimezone: String,
  sessions: Array,
  modelValue: Object,
})

const emit = defineEmits(['update:modelValue', 'sessionsChange'])

const sessionModalRef = ref(null)
const duplicateModalRef = ref(null)

const pageSize = 10
const localPageIndexNew = ref(0)
const localPageIndexExisting = ref(0)

// Server Pagination State
const currentCursorIndex = ref(0)
const nextCursor = ref(null)
const prevCursor = ref(null)
const hasUnsavedSessionChanges = ref(false)

// Computed to separate new from existing sessions
const newlyAddedSessions = computed(() => props.sessions.filter(s => !s.uuid && s.action !== "delete"))
const existingSessions = computed(() => props.sessions.filter(s => s.uuid && s.action !== "delete"))

const isUsingLocalPagination = computed(() => hasUnsavedSessionChanges.value)

// Pagination for newly added sessions
const displayedNewSessions = computed(() => {
  if (newlyAddedSessions.value.length === 0) return []
  const start = localPageIndexNew.value * pageSize
  const end = start + pageSize
  return newlyAddedSessions.value.slice(start, end)
})

const newSessionsPageSize = computed(() => Math.max(1, Math.ceil(newlyAddedSessions.value.length / pageSize)))
const shouldShowNewPagination = computed(() => newlyAddedSessions.value.length > pageSize)

// Pagination for existing sessions (from server)
const displayedExistingSessions = computed(() => {
  if (!isUsingLocalPagination.value) return existingSessions.value
  const start = localPageIndexExisting.value * pageSize
  const end = start + pageSize
  return existingSessions.value.slice(start, end)
})

const existingSessionsPageSize = computed(() => Math.max(1, Math.ceil(existingSessions.value.length / pageSize)))
const shouldShowExistingPagination = computed(() => {
  if (isUsingLocalPagination.value) {
    return existingSessions.value.length > pageSize || !!prevCursor.value || !!nextCursor.value
  }
  return !!prevCursor.value || !!nextCursor.value
})

const isNewPrevDisabled = computed(() => localPageIndexNew.value === 0)
const isNewNextDisabled = computed(() => localPageIndexNew.value >= newSessionsPageSize.value - 1)
const displayedNewPageNumber = computed(() => localPageIndexNew.value + 1)

const isExistingPrevDisabled = computed(() => {
  if (isUsingLocalPagination.value) {
    return localPageIndexExisting.value === 0 && !prevCursor.value
  }
  return !prevCursor.value
})

const isExistingNextDisabled = computed(() => {
  if (isUsingLocalPagination.value) {
    return localPageIndexExisting.value >= existingSessionsPageSize.value - 1 && !nextCursor.value
  }
  return !nextCursor.value
})

const displayedExistingPageNumber = computed(() => {
  if (isUsingLocalPagination.value) {
    // If on first local page but navigating server pages, show server page number
    if (localPageIndexExisting.value === 0 && currentCursorIndex.value > 0) {
      return currentCursorIndex.value + 1
    }
    return localPageIndexExisting.value + 1
  }
  return currentCursorIndex.value + 1
})

const getAbsoluteNewIndex = (visibleIndex) => {
  return localPageIndexNew.value * pageSize + visibleIndex
}

const getAbsoluteExistingIndex = (visibleIndex) => {
  if (!isUsingLocalPagination.value) return visibleIndex
  return localPageIndexExisting.value * pageSize + visibleIndex
}

// Duplicate State
const sessionToDuplicate = ref(null)
const duplicateCount = ref(1)
const activeCopyIndex = ref(null)
const copyInput = ref(null)

// Form state for modal
const isEditing = ref(false)
const editingIndex = ref(null)
const backupSession = ref(null)

const newSession = ref({
  start: "",
  end: "",
  capacity: null,
  location: "",
  description: ""
})

const repeatEnd = ref({ type: "never", date: "", count: null })
const repeatsChoose = ref({ type: "Does not repeat", interval: "" })

// --- SERVER PAGINATION LOGIC ---
const loadSessions = async (cursor, isNavigation = false) => {
  const sessionsRes = await getSessions(props.eventId, cursor, 10) 
  const sessionsData = sessionsRes.items || [];

  const mappedSessions = sessionsData.map(s => {
    const startObj = s.start_datetime ? new TZDate(s.start_datetime, props.userTimezone) : null;
    const endObj = s.end_datetime ? new TZDate(s.end_datetime, props.userTimezone) : null;

    return {
      id: s.id,
      uuid: s.uuid,
      start: startObj,
      end: endObj,
      capacity: s.seat_capacity,
      taken: s.seat_taken,
      action: null,
      location: s.location || "",
      description: s.description || ""
    }
  });

  // Preserve newly added sessions (those without UUID) and merge with server data
  const newlyAdded = props.sessions.filter(s => !s.uuid);
  const allSessions = [...newlyAdded, ...mappedSessions];
  
  emit('sessionsChange', allSessions);
  
  nextCursor.value = sessionsRes.next_page;
  prevCursor.value = sessionsRes.prev_page ?? sessionsRes.previous_page ?? null;
  hasUnsavedSessionChanges.value = newlyAdded.length > 0; // Keep true only if we have unsaved new sessions
  
  // Only reset on initial load, not on navigation
  if (!isNavigation) {
    localPageIndexNew.value = 0;
    localPageIndexExisting.value = 0;
  }
}

const goNext = async () => {
  if (isUsingLocalPagination.value) {
    if (localPageIndexExisting.value < existingSessionsPageSize.value - 1) {
      localPageIndexExisting.value++;
      return;
    }
    if (nextCursor.value) {
      currentCursorIndex.value++;
      await loadSessions(nextCursor.value, true);
    }
    return;
  }
  if (!nextCursor.value) return;
  
  currentCursorIndex.value++;
  await loadSessions(nextCursor.value, true);
}

const goPrev = async () => {
  if (isUsingLocalPagination.value) {
    if (localPageIndexExisting.value > 0) {
      localPageIndexExisting.value--;
      return;
    }
    if (prevCursor.value) {
      currentCursorIndex.value--;
      await loadSessions(prevCursor.value, true);
    }
    return;
  }
  if (!prevCursor.value) return;
  
  currentCursorIndex.value--;
  await loadSessions(prevCursor.value, true);
}

// --- MODAL CONTROLS ---
const openAddModal = () => {
  resetForm()
  isEditing.value = false
  sessionModalRef.value.showModal()
}

const openEditModal = (s, index) => {
  newSession.value = { 
    ...s, 
    start: s.start ? format(s.start, "yyyy-MM-dd'T'HH:mm") : "",
    end: s.end ? format(s.end, "yyyy-MM-dd'T'HH:mm") : ""
  }
  isEditing.value = true
  editingIndex.value = index
  backupSession.value = { ...s }
  
  props.sessions.splice(index, 1)
  emit('sessionsChange', [...props.sessions])
  sessionModalRef.value.showModal()
}

const closeSessionModal = () => {
  if (isEditing.value && backupSession.value) {
    props.sessions.splice(editingIndex.value, 0, backupSession.value)
    emit('sessionsChange', [...props.sessions])
  }
  sessionModalRef.value.close()
  resetForm()
}

// --- DUPLICATE LOGIC ---
const handleCopyClick = (session, index) => {
  if (activeCopyIndex.value === index) {
    activeCopyIndex.value = null
    return
  }
  activeCopyIndex.value = index
  duplicateCount.value = 1
}

const confirmDuplicateInline = () => {
  if (duplicateCount.value < 1) return
  
  for (let i = 0; i < duplicateCount.value; i++) {
    const lastSession = props.sessions[props.sessions.length - 1]
    const clone = { ...lastSession, id: undefined, uuid: undefined }
    props.sessions.push(clone)
  }
  
  emit('sessionsChange', [...props.sessions])
  hasUnsavedSessionChanges.value = true;
  localPageIndexNew.value = newSessionsPageSize.value - 1;
  localPageIndexExisting.value = 0;
  activeCopyIndex.value = null
}

const confirmDuplicate = () => {
  if (!sessionToDuplicate.value || duplicateCount.value < 1) return
  
  for (let i = 0; i < duplicateCount.value; i++) {
    const s = sessionToDuplicate.value
    const clone = { ...s, id: undefined, uuid: undefined }
    props.sessions.push(clone)
  }
  
  emit('sessionsChange', [...props.sessions])
  hasUnsavedSessionChanges.value = true;
  localPageIndexNew.value = newSessionsPageSize.value - 1;
  localPageIndexExisting.value = 0;
  closeDuplicateModal()
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

  const startDate = parseDatetimeLocal(newSession.value.start, props.userTimezone)
  const endDate = parseDatetimeLocal(newSession.value.end, props.userTimezone)
  
  const now = parseDatetimeLocal(format(new Date(), "yyyy-MM-dd'T'HH:mm"), props.userTimezone)
  if (startDate < now) {
    alert("A new session's start time cannot be before the current time.")
    return
  }

  const type = repeatsChoose.value.type
  const interval = Number(repeatsChoose.value.interval) || 1

  const addByType = (dateStr) => {
    const [datePart, timePart] = dateStr.split("T")
    const [year, month, day] = datePart.split("-").map(Number)
    const [hour, minute] = timePart.split(":").map(Number)

    const d = new Date(Date.UTC(year, month - 1, day, hour, minute))

    let next;
    if (type === "Daily") next = addDays(d, interval)
    else if (type === "Weekly") next = addWeeks(d, interval)
    else if (type === "Monthly") next = addMonths(d, interval)
    else if (type === "Yearly") next = addYears(d, interval)
    else next = d;

    const pad = (n) => String(n).padStart(2, '0')
    return `${next.getUTCFullYear()}-${pad(next.getUTCMonth() + 1)}-${pad(next.getUTCDate())}T${pad(next.getUTCHours())}:${pad(next.getUTCMinutes())}`
  }

  if (type === "Does not repeat") {
    props.sessions.push({
      ...newSession.value,
      start: startDate,
      end: endDate,
      action: "create"
    })
  } else {
    let currentStartStr = newSession.value.start
    let currentEndStr = newSession.value.end
    let i = 0

    while (true) {
      const currentStart = parseDatetimeLocal(currentStartStr, props.userTimezone)
      const currentEnd = parseDatetimeLocal(currentEndStr, props.userTimezone)

      props.sessions.push({
        ...newSession.value,
        start: currentStart,
        end: currentEnd,
        recurring: type,
        action: "create"
      })
      i++

      if (repeatEnd.value.type === "count") {
        if (repeatEnd.value.count && i >= repeatEnd.value.count) break
      }
      if (repeatEnd.value.type === "date" && repeatEnd.value.date) {
        const limitDate = parseDatetimeLocal(repeatEnd.value.date + "T23:59", props.userTimezone)
        if (currentStart >= limitDate) break
      }
      if (i > 100) break 
      
      currentStartStr = addByType(currentStartStr)
      currentEndStr = addByType(currentEndStr)
    }
  }
  
  emit('sessionsChange', [...props.sessions])
  hasUnsavedSessionChanges.value = true;
  localPageIndexNew.value = newSessionsPageSize.value - 1;
  localPageIndexExisting.value = 0;
  sessionModalRef.value.close()
  resetForm()
}

function saveEdit() {
  if (!newSession.value.start || !newSession.value.end) return alert("Please provide both start and end times.")
  if (newSession.value.start >= newSession.value.end) return alert("End time must be after start time.")
  if (newSession.value.taken > newSession.value.capacity) return alert("Capacity cannot be less than the number of taken seats.")
  
  props.sessions.splice(editingIndex.value, 0, { 
    ...newSession.value,
    start: parseDatetimeLocal(newSession.value.start, props.userTimezone),
    end: parseDatetimeLocal(newSession.value.end, props.userTimezone)
  })
  
  // Mark as modified if it's an existing session
  markSessionAsModified(editingIndex.value)
  
  emit('sessionsChange', [...props.sessions])
  hasUnsavedSessionChanges.value = true;
  localPageIndexExisting.value = 0;
  if (localPageIndexNew.value >= newSessionsPageSize.value) {
    localPageIndexNew.value = newSessionsPageSize.value - 1
  }
  sessionModalRef.value.close()
  resetForm()
}

function parseDatetimeLocal(dateStr, timezone) {
  const [datePart, timePart] = dateStr.split("T")
  const [year, month, day] = datePart.split("-").map(Number)
  const [hour, minute] = timePart.split(":").map(Number)

  return new TZDate(year, month - 1, day, hour, minute, 0, timezone)
}

function removeSession(index) {
  if(confirm("Remove this session?")) {
    const session = props.sessions[index]
    if (session.uuid) {
      // Mark existing session as deleted
      session.action = "delete"
    } else {
      // Remove newly added session from array
      props.sessions.splice(index, 1)
    }
    emit('sessionsChange', [...props.sessions])
    hasUnsavedSessionChanges.value = true;
    if (newlyAddedSessions.value.length === 0) {
      localPageIndexNew.value = 0
    } else if (localPageIndexNew.value >= newSessionsPageSize.value) {
      localPageIndexNew.value = newSessionsPageSize.value - 1
    }
    if (existingSessions.value.length === 0) {
      localPageIndexExisting.value = 0
    } else if (localPageIndexExisting.value >= existingSessionsPageSize.value) {
      localPageIndexExisting.value = existingSessionsPageSize.value - 1
    }
  }
}

function resetForm() {
  newSession.value = { start: "", end: "", capacity: null, location: "", description: "" }
  repeatsChoose.value = { type: "Does not repeat", interval: "" }
  repeatEnd.value = { type: "never", date: "", count: null }
  isEditing.value = false
  editingIndex.value = null
  backupSession.value = null
}

function markSessionAsModified(index) {
  const session = props.sessions[index]
  if (session.uuid && session.action !== "update") {
    session.action = "update"
  }
}

const closeDuplicateModal = () => {
  duplicateModalRef.value.close()
  sessionToDuplicate.value = null
}

const isSessionEnded = (endObj) => {
  if (!endObj) return false;
  return endObj < new Date();
}

function formatDay(dateObj) { 
  if(!dateObj) return '';
  return format(dateObj, 'd');
}
function formatMonth(dateObj) { 
  if(!dateObj) return '';
  return format(dateObj, 'MMM').toUpperCase(); 
}
function formatTime(dateObj) { 
  if(!dateObj) return '';
  return format(dateObj, 'hh:mm a'); 
}
function formatDate(dateObj) {
  if(!dateObj) return '';
  return format(dateObj, 'MMM d, yyyy');
}

defineExpose({
  loadSessions
})
</script>
