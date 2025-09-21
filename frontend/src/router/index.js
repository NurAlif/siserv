import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import DashboardView from '../views/DashboardView.vue';
import WriterView from '../views/WriterView.vue';
import LoginView from '../views/LoginView.vue';
import SignupView from '../views/SignupView.vue';
import LearningHubView from '../views/LearningHubView.vue';
import TopicDetailView from '../views/TopicDetailView.vue';
import AdminDashboardView from '../views/admin/AdminDashboardView.vue';
import AdminStudentDetailView from '../views/admin/AdminStudentDetailView.vue';
import AdminJournalDetailView from '../views/admin/AdminJournalDetailView.vue';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/writer/:date?', // The date parameter is optional
    name: 'Writer',
    component: WriterView,
    props: true, // Pass route params as props to the component
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  { 
    path: '/signup', 
    name: 'Signup', 
    component: SignupView 
  },
  { 
    path: '/learning-hub', 
    name: 'LearningHub', 
    component: LearningHubView, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/learning-hub/topic/:topic_id', 
    name: 'TopicDetail', 
    component: TopicDetailView, 
    meta: { requiresAuth: true }, 
    props: true 
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboardView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/student/:id',
    name: 'AdminStudentDetail',
    component: AdminStudentDetailView,
    meta: { requiresAuth: true, requiresAdmin: true },
    props: true,
  },
  {
    path: '/admin/student/:studentId/journal/:journalDate',
    name: 'AdminJournalDetail',
    component: AdminJournalDetailView,
    meta: { requiresAuth: true, requiresAdmin: true },
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  // Try to fetch user on page load if token exists but user object is null
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser();
  }

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
  
  if (requiresAuth && !authStore.isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    next('/login');
  } else if (requiresAdmin && !authStore.isAdmin) {
    // If route requires admin and user is not admin, redirect to dashboard
    next('/');
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    // If user is authenticated and tries to visit login page, redirect to dashboard
    next('/');
  }
  else {
    // Otherwise, proceed
    next();
  }
});

export default router;
