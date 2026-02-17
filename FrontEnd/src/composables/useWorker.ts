import type { Worker } from '@/dto/Worker';
import type { WorkerType } from '@/enum/workerType';
import apiClient from '@/utils/apiClient';
import { parseTrainingLevel } from '@/utils/parseTrainingLevel';
import { salaryFormatter } from '@/utils/salaryFormatter';

const route: String = "worker";

interface AllParams {
  worker_type: WorkerType;
  position_id: number | null;
  competence_id: number | null;
  training_id: number | null;
  initial_date: Date | null;
  end_date: Date | null;
}

export function useWorker() {
  
  const getAll = async ({ worker_type, position_id, competence_id, training_id, initial_date, end_date }: AllParams): Promise<Worker[]> => {
    const { data } = await apiClient.get<Worker[]>(`/${route}/get_all/${worker_type}`, {
      params: {
        position_id,
        competence_id,
        training_id,
        initial_date,
        end_date
      }
    });
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