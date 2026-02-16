import type { Department } from "./Department"
import type { Experience } from "./Experience"
import type { Position } from "./Position"
import type { WorkerCompetence } from "./WorkerCompetence"
import type { WorkerTraining } from "./WorkerTraining"

export class Worker {
    id: number | null = null
    identification: string = ''
    name: string = ''
    position_id: number | null = null
    department_id: number | null = null
    recommended_id: number | null = null
    wage: number | null = null
    initial_date: Date | null = null
    type: WorkerType | null = null
    state: boolean = true
    wage_text: string = ''

    position: Position | null = null
    department: Department | null = null
    recommended: Worker | null = null

    worker_competences: WorkerCompetence[] = []
    worker_trainings: WorkerTraining[] = []
    experiences: Experience[] = []
    workers: Worker[] = []
}