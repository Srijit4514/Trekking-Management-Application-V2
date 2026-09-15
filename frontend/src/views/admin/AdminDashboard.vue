<template>
  <div class="container-fluid my-4">
    <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4">
      <div>
        <h2>Admin Master Dashboard</h2>
        <p class="text-muted">Welcome, Admin. System tracking parameters are listed below.</p>
      </div>
      <form class="d-flex gap-2" @submit.prevent="handleSearch">
        <input 
          type="text" 
          class="form-control" 
          placeholder="Search by ID or Name..." 
          v-model="searchQuery"
        >
        <button type="submit" class="btn btn-dark">Search</button>
        <button 
          v-if="searchQuery" 
          type="button" 
          class="btn btn-secondary" 
          @click="clearSearch"
        >
          Clear
        </button>
      </form>
    </div>

    <DashboardMetrics :metrics="metrics" />

    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <FormCreateTrek @create="handleCreateTrek" />
      </div>

      <div class="col-md-4">
        <FormAddStaff @add="handleAddStaff" />
      </div>
      
      <div class="col-md-4">
        <FormAssignStaff 
          :treks="treks" 
          :active-staff="activeStaff" 
          @assign="handleAssignStaff" 
        />
      </div>
    </div>

    <div class="card shadow-sm mb-4">
      <div class="card-header bg-dark text-white">
        <strong>System Routes, Trekkers, and Assignment Lists</strong>
      </div>
      <div class="card-body p-0">
        <ul class="nav nav-tabs" id="adminTabs" role="tablist">
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'treks' }" @click="activeTab = 'treks'" type="button">Treks</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'trekkers' }" @click="activeTab = 'trekkers'" type="button">Trekkers</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'staff' }" @click="activeTab = 'staff'" type="button">Staff Directory</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'bookings' }" @click="activeTab = 'bookings'" type="button">Booking History</button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'analytics' }" @click="activeTab = 'analytics'" type="button">Statistics</button>
          </li>
        </ul>

        <div class="tab-content p-3">
          <TabTreks 
            v-if="activeTab === 'treks'" 
            :treks="filteredTreks" 
            @remove="handleRemoveTrek"
            @edit="openEditModal" 
          />
          
          <TabTrekkers 
            v-if="activeTab === 'trekkers'" 
            :users="filteredUsers" 
            @toggle-status="toggleUserStatus" 
          />
          
          <TabStaff 
            v-if="activeTab === 'staff'" 
            :pending-staff="pendingStaff" 
            :active-staff="activeStaff" 
            @toggle-status="toggleUserStatus" 
          />
          
          <TabBookings 
            v-if="activeTab === 'bookings'" 
            :bookings="bookings" 
          />
          
          <TabAnalytics 
            v-if="activeTab === 'analytics'" 
            :analytics="analyticsData" 
          />
        </div>
      </div>
    </div>

    <div v-if="editingTrek" class="modal fade show d-block" style="background: rgba(0,0,0,0.55); z-index: 1060;" role="dialog">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content shadow-lg border-0">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title fw-bold">Edit Trek Parameters</h5>
            <button type="button" class="btn-close btn-close-white" @click="editingTrek = null"></button>
          </div>
          <form @submit.prevent="handleUpdateTrek">
            <div class="modal-body p-4">
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">Trek Name</label>
                <input type="text" v-model="editingTrek.name" class="form-control" required>
              </div>
              <div class="row g-3 mb-3">
                <div class="col-6">
                  <label class="form-label small fw-bold text-secondary">Difficulty Level</label>
                  <input type="text" v-model="editingTrek.difficulty" class="form-control" placeholder="Easy / Moderate / Hard" required>
                </div>
                <div class="col-6">
                  <label class="form-label small fw-bold text-secondary">Total Available Slots</label>
                  <input type="number" v-model="editingTrek.slots" class="form-control" min="1" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-secondary">Trek Location</label>
                <input type="text" v-model="editingTrek.location" class="form-control" required>
              </div>
              <div class="row g-3 mb-3">
                <div class="col-6">
                  <label class="form-label small fw-bold text-secondary">Start Date</label>
                  <input type="date" v-model="editingTrek.start_date" class="form-control" required>
                </div>
                <div class="col-6">
                  <label class="form-label small fw-bold text-secondary">End Date</label>
                  <input type="date" v-model="editingTrek.end_date" class="form-control" required>
                </div>
              </div>
              <div class="mb-2">
                <label class="form-label small fw-bold text-secondary">Base Price ($)</label>
                <input type="number" v-model="editingTrek.price" class="form-control" min="0" step="0.01" required>
              </div>
            </div>
            <div class="modal-footer bg-light border-top-0">
              <button type="button" class="btn btn-secondary btn-sm px-3" @click="editingTrek = null">Dismiss</button>
              <button type="submit" class="btn btn-primary btn-sm px-4">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { api } from '../../services/api.js';
import axios from 'axios'; 

import DashboardMetrics from './components/DashboardMetrics.vue';
import FormCreateTrek from './components/FormCreateTrek.vue';
import FormAddStaff from './components/FormAddStaff.vue';
import FormAssignStaff from './components/FormAssignStaff.vue';
import TabTreks from './components/TabTreks.vue';
import TabTrekkers from './components/TabTrekkers.vue';
import TabStaff from './components/TabStaff.vue';
import TabBookings from './components/TabBookings.vue';
import TabAnalytics from './components/TabAnalytics.vue';

const activeTab = ref('treks');
const searchQuery = ref('');
const analyticsData = ref([]);
const editingTrek = ref(null);

const metrics = ref({
  totalTreks: 0,
  totalUsers: 0,
  totalStaff: 0,
  totalBookings: 0
});

const treks = ref([]);
const users = ref([]);
const staff = ref([]);
const bookings = ref([]);

const activeStaff = computed(() => staff.value.filter(s => s.is_active));
const pendingStaff = computed(() => staff.value.filter(s => !s.is_active));

const filteredTreks = computed(() => treks.value);
const filteredUsers = computed(() => users.value);


async function fetchDashboardData() {
  try {
    const data = await api.admin.getDashboard(searchQuery.value);
    const normalizedUsers = Array.isArray(data.users) ? data.users : [];
    const normalizedStaff = Array.isArray(data.staff) ? data.staff : [];
    const normalizedTreks = Array.isArray(data.treks) ? data.treks : [];
    const normalizedBookings = Array.isArray(data.bookings) ? data.bookings : [];
    analyticsData.value = Array.isArray(data.analytics) ? data.analytics : [];

    metrics.value = {
      ...(data.metrics || {}),
      totalUsers: normalizedUsers.length || data.metrics?.totalUsers || 0,
      totalStaff: normalizedStaff.length || data.metrics?.totalStaff || 0,
      totalTreks: normalizedTreks.length || data.metrics?.totalTreks || 0,
      totalBookings: normalizedBookings.length || data.metrics?.totalBookings || 0,
      totalRevenue: data.metrics?.totalRevenue || 0
    };
    treks.value = normalizedTreks;
    users.value = normalizedUsers;
    staff.value = normalizedStaff;
    bookings.value = normalizedBookings;
  } catch (error) {
    console.error("Dashboard Fetch Failed:", error);
    alert(`Could not load dashboard data: ${error.message}`);
  }
}

onMounted(() => {
  fetchDashboardData();
});

const handleSearch = () => {
  fetchDashboardData();
};

const clearSearch = () => {
  searchQuery.value = '';
  fetchDashboardData();
};

const handleCreateTrek = async (trekData) => {
  try {
    const data = await api.admin.addTrek(trekData);
    alert(data.message);
    fetchDashboardData(); 
  } catch (error) {
    alert(`Failed to add trek: ${error.message}`);
  }
};

const openEditModal = (targetTrek) => {
  editingTrek.value = { ...targetTrek };
};

const handleUpdateTrek = async () => {
  try {
    const data = await api.admin.editTrek(editingTrek.value.id, editingTrek.value);
    alert(data.message || "Trek updated successfully.");
    editingTrek.value = null;
    fetchDashboardData();    
  } catch (error) {
    alert(`Failed to save trek adjustments: ${error.message}`);
  }
};


const handleAddStaff = async (staffData) => {
  try {
    const data = await api.admin.addStaff(staffData);
    alert(data.message);
    fetchDashboardData(); 
  } catch (error) {
    alert(`Failed to add staff: ${error.message}`);
  }
};

const handleAssignStaff = async (assignmentData) => {
  try {
    const data = await api.admin.assignStaff(assignmentData);
    alert(data.message);
    fetchDashboardData(); 
  } catch (error) {
    alert(`Failed to update assignment: ${error.message}`);
  }
};

const toggleUserStatus = async (id) => {
  try {
    const data = await api.admin.toggleUserStatus(id);
    alert(data.message);
    fetchDashboardData(); 
  } catch (error) {
    alert(`Failed to change account status: ${error.message}`);
  }
};

const handleRemoveTrek = async (id) => {
  if (confirm("Are you completely sure you want to remove this trek listing? This action cannot be undone.")) {
    try {
      const data = await api.admin.deleteTrek(id);
      alert(data.message);
      fetchDashboardData(); 
    } catch (error) {
      alert(`Failed to remove trek: ${error.message}`);
    }
  }
};
</script>