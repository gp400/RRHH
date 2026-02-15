import type { Worker } from '@/dto/Worker';
import type { WorkerType } from '@/enum/workerType';
import apiClient from '@/utils/apiClient';

const route: String = "worker";

export function useWorker() {
  
  const getAll = async (workerType: WorkerType): Promise<Worker[]> => {
    const { data } = await apiClient.get<Worker[]>(`/${route}/get_all/${workerType}`);
    return data;
  } 

  const getById = async (id: number): Promise<Worker> => {
    const { data } = await apiClient.get<Worker>(`/${route}/get_by_id/${id}`);
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