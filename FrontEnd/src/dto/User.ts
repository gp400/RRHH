import { Worker } from './Worker'

export class User {
    id: number | null = null;
    email: string = ''
    password: string = ''
    worker_id: number | null = 0;
    state: boolean = true

    worker: Worker | null = null
}