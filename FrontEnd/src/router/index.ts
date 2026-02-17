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
      ]
    }
  ],
})

export default router
