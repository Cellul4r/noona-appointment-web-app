<template>
  <main class="flex-1 overflow-y-auto bg-base-200 p-4 md:p-12 scroll-smooth">
    <div v-if="isSuccess" role="alert" class="alert alert-success mb-4">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 shrink-0 stroke-current"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <span>Changes saved successfully!</span>
    </div>
    <div class="max-w-[800px] mx-auto flex flex-col gap-8 pb-20">
      <div class="header">
        <h1 class="text-3xl font-black tracking-tight text-base-content">
          Account Setting
        </h1>
        <p class="text-base-content/60">
          Manage your profile information and preferences here.
        </p>
      </div>

      <!-- Profile Picture -->
      <section
        class="bg-base-100 rounded-xl border border-base-300 p-6 shadow-sm flex flex-col gap-6"
      >
        <div class="flex flex-col gap-1 border-b border-base-300 pb-4">
          <h3 class="text-base-content text-lg font-bold">Profile Picture</h3>
        </div>
        <div class="flex flex-col sm:flex-row items-center gap-6">
          <div
            class="avatar cursor-pointer group"
            @click="avatar_modal.showModal()"
          >
            <dialog id="avatar_modal" class="modal">
              <div
                class="modal-box w-auto max-w-3xl p-0 overflow-hidden bg-transparent shadow-none"
              >
                <form method="dialog">
                  <button
                    class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                  >
                    ✕
                  </button>
                </form>
                <img
                  :src="getAvatar()"
                  alt="Profile picture"
                  class="w-full h-full object-contain max-h-[90vh] rounded-xl"
                />
              </div>
            </dialog>
            <div
              class="w-24 rounded-full ring-4 ring-base-200 shadow-md relative"
            >
              <img :src="getAvatar()" alt="Profile picture" />
              <div
                class="absolute inset-0 flex items-center justify-center rounded-full bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <span class="material-symbols-outlined text-white">View</span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-center sm:items-start flex-1 gap-2">
            <p class="text-base-content/60 text-sm mb-1">
              Supports JPG or PNG only.
            </p>
            <div class="flex gap-3">
              <input
                type="file"
                ref="fileInput"
                class="hidden"
                accept="image/png, image/jpeg"
                @change="handleFileUpload"
              />
              <button
                class="btn btn-sm btn-outline"
                @click="$refs.fileInput.click()"
                :disabled="uploadingAvatar"
              >
                <span
                  v-if="uploadingAvatar"
                  class="loading loading-spinner text-secondary"
                ></span>
                Upload New
              </button>
              <button
                class="btn btn-sm btn-error btn-outline"
                @click="removeAvatar"
              >
                Remove
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Personal Information -->
      <section
        class="bg-base-100 rounded-xl border border-base-300 p-6 shadow-sm flex flex-col gap-6"
      >
        <h3
          class="text-base-content text-lg font-bold border-b border-base-300 pb-4"
        >
          Personal Information
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="form-control gap-1 md:col-span-2">
            <label class="label py-0"
              ><span class="label-text font-semibold">Email</span></label
            >
            <input
              class="input input-bordered w-full opacity-50 cursor-not-allowed"
              disabled
              type="email"
              :value="formData.email"
            />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="form-control gap-1 md:col-span-2">
              <label class="label py-0"
                ><span class="label-text font-semibold">Full Name</span></label
              >
              <input
                class="input input-bordered w-full"
                v-model="formData.full_name"
                type="text"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="form-control gap-1 md:col-span-2">
              <div class="flex justify-between items-end">
                <label class="label py-0">
                  <span class="label-text font-semibold">
                    {{ passwordVerified ? "New Password" : "Password" }}
                  </span>
                </label>
                <button
                  v-if="!passwordVerified"
                  type="button"
                  @click="$refs.passwordModal.showModal()"
                  class="text-sm font-semibold text-primary hover:underline mb-1"
                >
                  Change password
                </button>
                <dialog id="my_modal_3" ref="passwordModal" class="modal">
                  <div class="modal-box flex flex-col gap-6">
                    <form method="dialog">
                      <button
                        class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                      >
                        ✕
                      </button>
                    </form>

                    <div class="flex flex-col items-center gap-4 text-center">
                      <div class="flex flex-col gap-1">
                        <h3 class="text-xl font-bold">Verify Identity</h3>
                        <p class="text-sm text-base-content/60">
                          For your security, please enter your current password
                          to continue.
                        </p>
                      </div>
                    </div>

                    <div class="flex flex-col gap-2">
                      <label class="text-sm font-semibold"
                        >Current Password</label
                      >
                      <div class="relative group">
                        <input
                          v-model="current_password"
                          type="password"
                          class="w-full input"
                          placeholder="Enter your current password"
                          required
                        />
                      </div>
                    </div>

                    <button
                      type="button"
                      class="btn btn-primary"
                      @click="verifyPassword"
                    >
                      Verify
                    </button>
                  </div>
                </dialog>
              </div>

              <!-- Locked state -->
              <input
                v-if="!passwordVerified"
                type="password"
                placeholder="••••••••"
                class="input input-bordered w-full opacity-50 cursor-not-allowed"
                disabled
              />

              <!-- Unlocked: new password fields -->
              <template v-else>
                <input
                  v-model="formData.new_password"
                  type="password"
                  class="input input-bordered w-full"
                  placeholder="Enter new password"
                  minlength="8"
                />
                <div class="form-control gap-1 mt-3">
                  <label class="label py-0"
                    ><span class="label-text font-semibold"
                      >Confirm New Password</span
                    ></label
                  >
                  <input
                    v-model="formData.confirm_password"
                    type="password"
                    class="input input-bordered w-full"
                    placeholder="Confirm new password"
                  />
                </div>
                <p class="text-xs text-base-content/50 mt-1">
                  New password will be saved when you click Save Changes.
                </p>
              </template>
            </div>
          </div>
        </div>
      </section>

      <!-- Preferences -->
      <section
        class="bg-base-100 rounded-xl border border-base-300 p-6 shadow-sm flex flex-col gap-6"
      >
        <h3
          class="text-base-content text-lg font-bold border-b border-base-300 pb-4"
        >
          Preferences
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Timezone -->
          <div class="form-control w-full gap-1 md:col-span-2">
            <label class="label py-0"
              ><span class="label-text font-semibold">Time Zone</span></label
            >
            <label
              class="input input-bordered relative w-full flex items-center"
            >
              <select
                v-model="formData.timezone"
                class="w-full bg-transparent outline-none"
              >
                <option value="GMT">
                  (GMT+00:00) London - Greenwich Mean Time
                </option>
                <option value="EST">
                  (GMT-05:00) New York - Eastern Standard Time
                </option>
                <option value="PST">
                  (GMT-08:00) Los Angeles - Pacific Standard Time
                </option>
                <option value="CET">
                  (GMT+01:00) Paris - Central European Time
                </option>
              </select>
            </label>
          </div>

          <!-- Language -->
          <div class="form-control gap-1">
            <label class="label py-0"
              ><span class="label-text font-semibold">Language</span></label
            >
            <label
              class="input input-bordered flex relative w-full items-center gap-2"
            >
              <select class="grow bg-transparent outline-none">
                <option value="en">English (US)</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
              </select>
            </label>
          </div>

          <div class="form-control gap-1">
            <label class="label py-0"
              ><span class="label-text font-semibold">Theme</span></label
            >
            <label
              class="input input-bordered relative w-full items-center gap-2"
            >
              <input
                type="text"
                v-model="theme"
                list="theme-options"
                @input="updateTheme"
                placeholder="Select theme..."
                class="grow bg-transparent outline-none"
              />

              <datalist id="theme-options">
                <option v-for="t in themes" :key="t" :value="t"></option>
              </datalist>
            </label>
          </div>

          <!-- Email Notifications -->
          <div class="form-control gap-1 md:col-span-2">
            <label class="label py-1">
              <span class="label-text font-semibold">Notification</span>
            </label>
            <div
              class="flex items-center justify-between p-4 rounded-lg border border-base-300 bg-base-200 gap-4"
            >
              <div class="flex flex-col gap-0.5">
                <span class="text-sm font-semibold text-base-content"
                  >Email Notifications</span
                >
                <span class="text-xs text-base-content/60"
                  >Enable to receive updates about your scheduled sessions and
                  reminders.</span
                >
              </div>
              <input
                type="checkbox"
                class="toggle toggle-primary"
                v-model="formData.email_notifications"
              />
            </div>
          </div>
        </div>
      </section>

      <section
        class="bg-base-100 rounded-xl border border-base-300 p-6 shadow-sm flex flex-col gap-6"
      >
        <h3
          class="text-base-content text-lg font-bold border-b border-base-300 pb-4"
        >
          Linked Accounts
        </h3>
        <div class="flex flex-col gap-4">
          <!-- Google -->
          <div
            class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-lg border border-base-300 bg-base-200 gap-4"
          >
            <div class="flex items-center gap-4">
              <div class="avatar">
                <div
                  class="w-10 rounded-full bg-base-100 border border-base-300"
                >
                  <img
                    class="w-5 h-5 mx-auto mt-2"
                    src="https://img.icons8.com/?size=100&id=17949&format=png&color=000000"
                  />
                </div>
              </div>

              <div class="flex flex-col">
                <span class="text-sm font-bold text-base-content">
                  Google
                </span>
                <span class="text-xs text-success font-medium">
                  Connected as {{ formData.email }}
                </span>
              </div>
            </div>

            <button
              v-if="isLinked('google')"
              class="btn btn-sm btn-outline btn-error"
              @click="unlinkAccount('google')"
            >
              Disconnect
            </button>
            <button
              v-else
              class="btn btn-sm btn-primary"
              @click="linkAccount('google')"
            >
              Connect
            </button>
          </div>

          <!-- GitHub -->
          <div
            class="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-lg border border-base-300 bg-base-200 gap-4"
          >
            <div class="flex items-center gap-4">
              <div class="avatar">
                <div
                  class="w-10 rounded-full bg-base-100 border border-base-300 flex items-center justify-center"
                >
                  <svg
                    class="w-5 h-5 text-base-content"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      d="M12 .5C5.73.5.5 5.73.5 12a11.5 11.5 0 008 10.94c.59.11.8-.26.8-.58v-2.02c-3.26.7-3.95-1.57-3.95-1.57-.53-1.35-1.3-1.71-1.3-1.71-1.06-.72.08-.71.08-.71 1.18.08 1.8 1.22 1.8 1.22 1.04 1.79 2.73 1.27 3.4.97.1-.76.41-1.27.75-1.56-2.6-.3-5.34-1.3-5.34-5.78 0-1.28.46-2.33 1.21-3.15-.12-.3-.52-1.52.11-3.18 0 0 .99-.32 3.25 1.2a11.2 11.2 0 015.92 0c2.26-1.52 3.25-1.2 3.25-1.2.63 1.66.23 2.88.11 3.18.75.82 1.21 1.87 1.21 3.15 0 4.49-2.74 5.47-5.35 5.77.42.36.8 1.09.8 2.2v3.26c0 .32.21.7.81.58A11.5 11.5 0 0023.5 12C23.5 5.73 18.27.5 12 .5z"
                    />
                  </svg>
                </div>
              </div>

              <div class="flex flex-col">
                <span class="text-sm font-bold text-base-content">
                  GitHub
                </span>
                <span class="text-xs text-base-content/60">
                  Not connected
                </span>
              </div>
            </div>

            <button
              v-if="isLinked('github')"
              class="btn btn-sm btn-outline btn-error"
              @click="unlinkAccount('github')"
            >
              Disconnect
            </button>

            <button
              v-else
              class="btn btn-sm btn-primary"
              @click="linkAccount('github')"
            >
              Connect
            </button>
          </div>
        </div>
      </section>
      <!-- Footer Actions -->
      <div class="fixed bottom-0 left-0 w-full z-20 pointer-events-none">
        <div
          class="bg-base-100 border-t border-base-300 p-4 pointer-events-auto flex justify-end gap-3 px-10 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]"
        >
          <button class="btn" @click="fetchUserData">Cancel</button>
          <button class="btn btn-primary" @click="submitForm">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from "axios";
import { computed } from "vue";
import { useAuthStore } from "@/store/authStore";
import { useRouter } from "vue-router";

const DefaultAvatar =
  "https://img.icons8.com/?size=100&id=z-JBA_KtSkxG&format=png&color=000000";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const user = computed(() => authStore.user);

    return { authStore, router, user };
  },

  data() {
    return {
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
      avatarPreview: null,
      uploadingAvatar: false,

      current_password: "", // In password verification modal
      passwordVerified: false,
      showPasswordModal: false,

      theme: localStorage.getItem("app-theme") || "light",
      themes: [
        "light",
        "dark",
        "cupcake",
        "bumblebee",
        "emerald",
        "corporate",
        "synthwave",
        "retro",
        "cyberpunk",
        "valentine",
        "halloween",
        "garden",
        "forest",
        "aqua",
        "lofi",
        "pastel",
        "fantasy",
        "wireframe",
        "black",
        "luxury",
        "dracula",
        "cmyk",
        "autumn",
        "business",
        "acid",
        "lemonade",
        "night",
        "coffee",
        "winter",
        "dim",
        "nord",
        "sunset",
      ],

      isSuccess: false,

      formData: {
        email: "",
        full_name: "",
        profile_image: null,
        timezone: "UTC",
        email_notifications: false,
        password: null, // new password field, only sent if user verified current password
      },

      oauthAccounts: [],
    };
  },

  async mounted() {
    await this.fetchUserData();
  },

  methods: {
    async fetchUserData() {
      try {
        console.log("Fetching user data from API...");

        //  Make API request (Axios sends JWT automatically via cookies)
        const res = await axios.get(`${this.apiBaseUrl}/users/settings`);

        console.log("API Response Object:", res);

        if (!res.data) {
          throw new Error("No data received from API");
        }

        console.log("Parsed Data:", res.data);
        this.formData.email = res.data.email;
        this.formData.full_name = res.data.full_name;
        this.formData.profile_image = res.data.profile_image;
        this.formData.timezone = res.data.timezone;
        this.formData.email_notifications = res.data.email_notifications;

        this.oauthAccounts = res.data.oauth_accounts || [];
      } catch (error) {
        console.error("Error fetching data:", error);
        this.response = `Error: ${error.message}`;
      }
    },
    async submitForm() {
      try {
        const data = {
          full_name: this.formData.full_name,
          profile_image: this.formData.profile_image,
          timezone: this.formData.timezone,
          email_notifications: this.formData.email_notifications,
        };

        // Only send password if verified
        if (this.passwordVerified && this.formData.new_password) {
          if (this.formData.new_password !== this.formData.confirm_password) {
            alert("Passwords do not match");
            return;
          }

          data.password = this.formData.new_password;
        }

        await axios.patch(`${this.apiBaseUrl}/users/me`, data);

        // Reset password UI
        this.passwordVerified = false;
        this.current_password = "";
        this.formData.new_password = "";
        this.formData.confirm_password = "";

        this.isSuccess = true;
        setTimeout(() => {
          this.isSuccess = false;
        }, 5000);
      } catch (error) {
        console.error("Error updating profile:", error);
      }
    },
    async verifyPassword() {
      try {
        await axios.post(`${this.apiBaseUrl}/users/verify-password`, {
          password: this.current_password,
        });

        this.passwordVerified = true;
        this.$refs.passwordModal.close();
      } catch {
        alert("Incorrect password");
      }
    },
    updateTheme() {
      document.documentElement.setAttribute("data-theme", this.theme);
      localStorage.setItem("app-theme", this.theme);
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.avatarPreview = e.target.result;
        this.formData.profile_image = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    removeAvatar() {
      this.avatarPreview = null;
      this.formData.profile_image = null;
    },

    getAvatar() {
      return this.avatarPreview || this.formData.profile_image || DefaultAvatar;
    },
    viewAvatar() {
      document.getElementById("avatar_modal").showModal();
    },
    isLinked(provider) {
      return this.oauthAccounts.some((acc) => acc.provider === provider);
    },

    linkAccount(provider) {
      window.location.href = `${this.apiBaseUrl}/auth/${provider}/login?link=true`;
    },

    async unlinkAccount(provider) {
      try {
        await axios.delete(
          `${this.apiBaseUrl}/users/unlink-accounts/${provider}`,
        );
        this.oauthAccounts = this.oauthAccounts.filter(
          (acc) => acc.provider !== provider,
        );
      } catch (err) {
        console.error("Unlink failed:", err);
      }
    },
  },
};
</script>
