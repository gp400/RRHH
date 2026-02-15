import type { Competence } from "./Competence";

export class WorkerCompetence {
    id: number | null = null;
    worker_id: number | null = null;
    competence_id: number | null = null;
    state: boolean = true;

    competence: Competence | null = null;
}