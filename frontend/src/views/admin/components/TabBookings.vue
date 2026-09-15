<template>
  <table class="table table-striped align-middle">
    <thead>
      <tr>
        <th>Booking ID</th>
        <th>Trekker Username</th>
        <th>Target Destination Trail</th>
        <th>Booking Status</th>
        <th>Payment Matrix</th>
        <th class="text-end">Download Report</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="b in bookings" :key="b.id">
        <td>#{{ b.id }}</td>
        <td>{{ b.user?.username || 'N/A' }}</td>
        <td>{{ b.trek?.name || 'N/A' }}</td>
        <td><span class="badge bg-secondary">{{ b.booking_status }}</span></td>
        <td><span class="badge bg-info text-dark">{{ b.payment_status }}</span></td>
        <td class="text-end">
          <button 
            v-if="b.trek && b.trek.id"
            @click="downloadPdfReport(b.trek.id)" 
            class="btn btn-sm btn-primary"
          >
            Download PDF Report
          </button>
        </td>
      </tr>
      <tr v-if="bookings.length === 0">
        <td colspan="6" class="text-center text-muted py-3">
          No booking historical tracking records found in current database.
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
import { api } from '@/services/api.js';

defineProps({
  bookings: { type: Array, required: true }
});

const downloadPdfReport = async (trekId) => {
  if (!trekId) return;
  
  try {
    const blob = await api.admin.downloadReport(trekId);
    
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `trek_${trekId}_report.pdf`;
    document.body.appendChild(link);
    link.click();
    
    // Cleanup
    setTimeout(() => {
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    }, 100);
  } catch (error) {
    console.error("Download failed:", error);
    alert("Could not download report. Verify authorization.");
  }
};
</script>