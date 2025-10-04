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
import AdminManageStudentsView from '../views/admin/AdminManageStudentsView.vue';
import AdminManageNotificationsView from '../views/admin/AdminManageNotificationsView.vue';
import AdminSurveyResultsView from '../views/admin/AdminSurveyResultsView.vue'; // New Import

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/writer/:date?',
    name: 'Writer',
    component: WriterView,
    props: true,
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
  {
    path: '/admin/manage-students',
    name: 'AdminManageStudents',
    component: AdminManageStudentsView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/manage-notifications',
    name: 'AdminManageNotifications',
    component: AdminManageNotificationsView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  // --- NEW SURVEY RESULTS ROUTE ---
  {
    path: '/admin/notification/:id/results',
    name: 'AdminSurveyResults',
    component: AdminSurveyResultsView,
    meta: { requiresAuth: true, requiresAdmin: true },
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser();
  }

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
  
  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (requiresAdmin && !authStore.isAdmin) {
    next('/');
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/');
  }
  else {
    next();
  }
});

export default router;

