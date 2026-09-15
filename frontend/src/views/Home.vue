<template>
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm border">
        <div class="container-fluid py-5 text-center">
            <h1 class="display-5 fw-bold text-dark">Explore the Unexplored</h1>
            <p class="col-md-8 mx-auto fs-5 text-muted">
                Welcome to the Trekking Portal. Join our community of outdoor enthusiasts, map your trails, and manage assignments flawlessly. Register an account today to begin your journey.
            </p>
            <div class="d-grid gap-2 d-sm-flex justify-content-sm-center mt-4">
                <router-link to="/register" class="btn btn-primary btn-lg px-4 gap-3">
                    Get Started
                </router-link>
                <router-link to="/login" class="btn btn-outline-secondary btn-lg px-4">
                    Account Login
                </router-link>
            </div> 
        </div>
    </div>
</template>
