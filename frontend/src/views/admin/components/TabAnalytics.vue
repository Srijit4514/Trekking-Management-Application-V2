<template>
  <div class="p-3">
    <div class="row g-4">
      <div class="col-md-6">
        <div class="card shadow-sm p-3">
          <h6 class="fw-bold text-dark mb-3">Revenue Generative Metrics ($)</h6>
          <div style="height: 300px; position: relative;">
            <Bar :data="revenueChartData" :options="chartOptions" />
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow-sm p-3">
          <h6 class="fw-bold text-dark mb-3">Booking Distribution Breakdown</h6>
          <div style="height: 300px; position: relative;">
            <Pie :data="bookingsChartData" :options="chartOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

const props = defineProps({
  analytics: { type: Array, required: true }
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
};

const revenueChartData = computed(() => ({
  labels: props.analytics.map(item => item.trek_name),
  datasets: [{
    label: 'Revenue Generated',
    backgroundColor: '#0d6efd',
    data: props.analytics.map(item => item.revenue)
  }]
}));

const bookingsChartData = computed(() => ({
  labels: props.analytics.map(item => item.trek_name),
  datasets: [{
    backgroundColor: ['#198754', '#ffc107', '#dc3545', '#0dcaf0', '#6c757d', '#6f42c1', '#fd7e14'],
    data: props.analytics.map(item => item.total_bookings)
  }]
}));
</script>