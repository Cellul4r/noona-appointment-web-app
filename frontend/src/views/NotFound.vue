<template>
    <div class="min-h-screen bg-base-200 flex items-center justify-center px-4">
        <div class="card w-full max-w-xl bg-base-100 border border-base-300 shadow-lg">
            <div class="card-body items-center text-center gap-4">
                <div class="text-6xl font-bold text-primary">404</div>
                <h1 class="text-2xl font-bold">Page Not Found</h1>
                <p class="text-base-content/70">
                    The page you are looking for does not exist or may have been moved.
                </p>
                <div class="flex gap-3 mt-2">
                    <RouterLink to="/events" class="btn btn-primary">Go to Events</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
