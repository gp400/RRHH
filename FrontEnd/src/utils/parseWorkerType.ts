import { WorkerType } from "@/enum/workerType";

export const parseWorkerType = (workerType: WorkerType): string => {
    switch (workerType) {
        case WorkerType.candidate:
            return "Candidato";
        case WorkerType.employee:
            return "Empleado";
        default:
            throw new Error("Tipo desconocida");
    }
}