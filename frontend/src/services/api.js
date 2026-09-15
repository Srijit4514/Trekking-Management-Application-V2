const BASE_URL = 'http://127.0.0.1:5001';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('authToken');
  
  // Setup headers dynamically
  const headers = {
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Handle standard JSON payloads safely
  if (options.body && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }

  const config = {
    ...options,
    headers
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, config);
  
  if (response.status === 401 || response.status === 403) {
    console.error("Authentication mapping or role authorization mismatch.");
  }

  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/pdf')) {
    return response.blob(); 
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || data.message || `HTTP Error: ${response.status}`);
  }
  
  return data;
}
export const api = {
  auth: {
    register: (userData) => request('/auth/register', { method: 'POST', body: userData }),
    login: (credentials) => request('/auth/login', { method: 'POST', body: credentials }),
  },

  admin: {
    getDashboard: (searchQuery = '') => {
      const url = searchQuery 
        ? `/admin/dashboard?search=${encodeURIComponent(searchQuery)}` 
        : '/admin/dashboard';
      return request(url, { method: 'GET' });
    },
    addStaff: (staffData) => request('/admin/staff/add', { method: 'POST', body: staffData }),
    toggleUserStatus: (userId) => request(`/admin/user/toggle_status/${userId}`, { method: 'POST' }),
    addTrek: (trekData) => request('/admin/trek/add', { method: 'POST', body: trekData }),
    editTrek: (trekId, trekData) => request(`/admin/trek/edit/${trekId}`, { method: 'PUT', body: trekData }),
    assignStaff: (assignmentData) => request('/admin/trek/assign_staff', { method: 'POST', body: assignmentData }),
    deleteTrek: (trekId) => request(`/admin/trek/delete/${trekId}`, { method: 'DELETE' }),
    downloadReport: (trekId) => request(`/admin/trek/${trekId}/booking_report`, { method: 'GET' }),
  },

  staff: {
    // getAssignedTreks: () => request('/staff/my-treks'),
    getDashboard: () => request("/staff/dashboard", {method: 'GET'}),

    updateTrek: (trekId, updateData) => request(`/staff/trek/update/${trekId}`,{
      method: 'POST',
      body: updateData
    }),

    logout: () => request("/staff/logout", {method: 'POST'})
  },

  user: {
    getDashboard: (filters = {}) => {
      const params = new URLSearchParams();
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.location) params.append('location', filters.location);
      if (filters.duration) params.append('duration', filters.duration);

      const url = params.toString() ? `/user/dashboard?${params.toString()}` : '/user/dashboard';
      return request(url, {method: 'GET'});
    },

    bookTrek: (trekId) => request(`/user/trek/book/${trekId}`, { method: 'POST' }),

    updateProfile: (profileData) => request('/user/profile/update', { method: 'POST', body: profileData })
  }
};