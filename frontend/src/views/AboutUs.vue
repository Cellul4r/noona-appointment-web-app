<template>
    <main class="flex-1 w-full max-w-7xl mx-auto flex flex-col items-center px-4">

        <!-- Hero -->
        <section class="w-full py-20 text-center max-w-4xl mx-auto">
            <div
                class="badge badge-outline text-primary border-primary/30 bg-primary/5 mb-6 py-3 px-4 text-xs font-semibold uppercase tracking-wider">
                누나 - Noona
            </div>
            <h1 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">
                More Than Scheduling
                <span class="text-primary relative inline-block">
                    It's Structured Freedom
                    <svg class="absolute w-full h-3 -bottom-1 left-0 text-primary/20" preserveAspectRatio="none"
                        viewBox="0 0 100 10">
                        <path d="M0 5 Q 50 10 100 5" fill="none" stroke="currentColor" stroke-width="8" />
                    </svg>
                </span>
            </h1>
            <p class="text-lg md:text-xl text-base-content/60 leading-relaxed max-w-2xl mx-auto">
                Everything you need to manage appointments, coordinate with your team, and deliver a seamless experience
                for your users.
            </p>
        </section>

        <!-- Feature Cards -->
        <section class="w-full mb-24">
            <div class="grid md:grid-cols-2 gap-6">
                <div v-for="feature in features" :key="feature.title"
                    class="card bg-base-100 border border-base-200 hover:border-primary/30 shadow-sm hover:shadow-md transition-all duration-300">
                    <div class="card-body">
                        <div :class="`w-14 h-14 rounded-xl ${feature.iconBg} flex items-center justify-center mb-2`">
                            <span :class="`${feature.iconColor}`" v-html="feature.icon"></span>
                        </div>
                        <h3 class="card-title text-lg">{{ feature.title }}</h3>
                        <p class="text-base-content/60 text-sm leading-relaxed">{{ feature.description }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Banner -->
        <section class="w-full mb-24">
            <div
                class="card bg-gradient-to-br from-primary/10 via-base-100 to-secondary/10 border border-base-200 shadow-xl">
                <div class="card-body items-center text-center py-16 px-8">
                    <h2 class="card-title text-3xl md:text-4xl font-bold mb-4">Ready to simplify your scheduling?</h2>
                    <p class="text-base-content/60 mb-8 text-lg max-w-xl">
                        Join thousands of teams who trust Noona to handle their most important appointments with
                        precision and ease.
                    </p>
                    <button class="btn btn-primary btn-lg px-10" @click="$router.push('/verify-email')">
                        Get Started for Free
                    </button>
                </div>
            </div>
        </section>

        <!-- Why Noona -->
        <section class="w-full mb-24">
            <div class="text-center mb-12">
                <h2 class="text-3xl font-bold mb-3">Why choose Noona?</h2>
                <p class="text-base-content/60 max-w-xl mx-auto">
                    We believe scheduling should feel supportive — like an older sister who keeps everything in place
                    and makes it effortless for you.
                </p>
            </div>
            <div class="grid md:grid-cols-3 gap-6">
                <div v-for="value in values" :key="value.title"
                    class="card bg-base-100 border border-base-200 shadow-sm hover:-translate-y-1 transition-transform duration-300 text-center">
                    <div class="card-body items-center">
                        <div :class="`w-16 h-16 rounded-2xl ${value.iconBg} flex items-center justify-center mb-2`">
                            <span :class="`${value.iconColor}`" v-html="value.icon"></span>
                        </div>
                        <h3 class="card-title">{{ value.title }}</h3>
                        <p class="text-base-content/60 text-sm leading-relaxed">{{ value.description }}</p>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <footer class="bg-base-200 border-t border-base-300">
        <div class="w-full max-w-7xl mx-auto px-6 py-12 flex items-center justify-between">
            <div>
                <div class="flex items-center gap-2 mb-4">
                    <img src="/src/assets/Noona.png" class="h-8 w-auto" alt="Noona logo" />
                    <span class="font-bold text-xl">Noona</span>
                </div>
                <p class="text-sm text-base-content/50">
                    Your reliable older sister in the world of scheduling. <br>
                    Simple, supportive, and stress-free.
                </p>
            </div>
            <p class="text-sm text-base-content/40 shrink-0">
                © CMU 204212 Project. All rights reserved.
            </p>
        </div>
    </footer>
</template>

<script setup>
const features = [
    {
        title: 'Session-Level Intelligence',
        description: 'Recurring schedules? Daily, weekly, monthly, yearly — you set it once, and Noona keeps it organized. Create structured sessions with seat limits, built-in recurrence, and simple individual sign-ups. No spreadsheets. No mess.',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="16" y1="2" x2="16" y2="6"/></svg>`,
        iconBg: 'bg-purple-50',
        iconColor: 'text-purple-600',
    },
    {
        title: 'Smart Waitlist System',
        description: 'Intelligent waitlists that automatically notify participants when a spot becomes available. Maximize attendance, reduce drop-offs, and keep your sessions fully optimized — effortlessly.',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>`,
        iconBg: 'bg-emerald-50',
        iconColor: 'text-emerald-600',
    },
    {
        title: 'Transparent Availability',
        description: "See exactly what's happening at a glance — which sessions are available, which are full, and what you've selected. Everything updates in real time, so there's no guessing and no second-guessing.",
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/></svg>`,
        iconBg: 'bg-amber-50',
        iconColor: 'text-amber-600',
    },
    {
        title: 'Automatic Email Notifications',
        description: "When session details change — email notifications are automatically sent to everyone involved. Participants stay informed beyond the platform, and hosts don't need to manually announce updates or follow up.",
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z"/></svg>`,
        iconBg: 'bg-blue-50',
        iconColor: 'text-blue-600',
    },
]

const values = [
    {
        title: 'Reliability',
        description: 'Like a big sister you can count on, Noona is always there. We prioritize stability and trust, ensuring your schedule is safe and your time is respected.',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
        iconBg: 'bg-indigo-50',
        iconColor: 'text-indigo-600',
    },
    {
        title: 'Simplicity',
        description: 'We remove the stress of "when are you free?" by offering a clean, clutter-free interface. We believe technology should get out of the way.',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>`,
        iconBg: 'bg-orange-50',
        iconColor: 'text-orange-500',
    },
    {
        title: 'Support',
        description: 'Whether you are a host organizing sessions or a participant booking time, Noona guides you gently. We facilitate meaningful connection.',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`,
        iconBg: 'bg-emerald-50',
        iconColor: 'text-emerald-500',
    },
]
</script>