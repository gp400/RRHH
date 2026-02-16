import type { Worker } from '@/dto/Worker';
import type { WorkerType } from '@/enum/workerType';
import apiClient from '@/utils/apiClient';
import { parseTrainingLevel } from '@/utils/parseTrainingLevel';
import { salaryFormatter } from '@/utils/salaryFormatter';

const route: String = "worker";

export function useWorker() {
  
  const getAll = async (workerType: WorkerType): Promise<Worker[]> => {
    const { data } = await apiClient.get<Worker[]>(`/${route}/get_all/${workerType}`);
    data.forEach(worker => {
      worker.wage_text = salaryFormatter(worker.wage!)
      worker.worker_trainings.forEach(wt => {
        wt.training!.level_text = parseTrainingLevel(wt.training!.level!);
      })
    })
    return data;
  } 

  const getById = async (id: number): Promise<Worker> => {
    const { data } = await apiClient.get<Worker>(`/${route}/get_by_id/${id}`);
    data.wage_text = salaryFormatter(data.wage!)
    data.worker_trainings.forEach(wt => {
      wt.training!.level_text = parseTrainingLevel(wt.training!.level!);
    })
    return data;
  }

  const create = async (worker: Worker): Promise<Worker> => {
    const { data } = await apiClient.post<Worker>(`/${route}/create`, { ...worker });
    return data;
  }

  const update = async (worker: Worker): Promise<Worker> => {
    const { data } = await apiClient.put<Worker>(`/${route}/update`, { ...worker });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}