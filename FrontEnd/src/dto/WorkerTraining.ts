import type { Training } from "./Training";

export class WorkerTraining {
    id: number | null = null;
    worker_id: number | null = null;
    training_id: number | null = null;
    state: boolean = true;

    training: Training | null = null
}