import { createRouter, createWebHistory } from 'vue-router'
import LayoutComponent from '@/components/LayoutComponent.vue'
import CompetenceView from '@/views/CompetenceView.vue'
import LanguageView from '@/views/LanguageView.vue'
import TrainingView from '@/views/TrainingView.vue'
import PositionView from '@/views/PositionView.vue'
import DepartmentView from '@/views/DepartmentView.vue'
import CandidateView from '@/views/CandidateView.vue'
import EmployeeView from '@/views/EmployeeView.vue'
import ReportView from '@/views/ReportView.vue'
import LoginView from '@/views/LoginView.vue'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      component: LayoutComponent,
      children: [
        { path: "competence", name: 'competence', component: CompetenceView },
        { path: "language", name: 'language', component: LanguageView },
        { path: "training", name: 'training', component: TrainingView },
        { path: "position", name: 'position', component: PositionView },
        { path: "department", name: 'department', component: DepartmentView },
        { path: "candidate", name: 'candidate', component: CandidateView },
        { path: "employee", name: 'employee', component: EmployeeView },
        { path: "report", name: 'report', component: ReportView },
        { path: "", redirect: "competence" }
      ],
      meta: { requiresAuth: true }
    },
    { path: '/login', component: LoginView }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const redirectRoutes = ['/login']

  if (to.meta.requiresAuth && !authStore.JWT) {
    next("/login")
  } else if (authStore.JWT && redirectRoutes.includes(to.fullPath.toLocaleLowerCase())) {
    next('')
  } else {
    next()
  }
});

export default router
