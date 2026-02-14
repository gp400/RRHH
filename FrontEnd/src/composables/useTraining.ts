import { Training } from '@/dto/Training';
import apiClient from '@/utils/apiClient';
import { parseTrainingLevel } from '@/utils/parseTrainingLevel';

const route: String = "training";

export function useTraining() {
  
  const getAll = async (): Promise<Training[]> => {
    const { data } = await apiClient.get<Training[]>(`/${route}/get_all`);
    data.forEach(train => {
      train.levelText = parseTrainingLevel(train.level!);
    })
    return data;
  } 

  const getById = async (id: number): Promise<Training> => {
    const { data } = await apiClient.get<Training>(`/${route}/get_by_id/${id}`);
    data.levelText = parseTrainingLevel(data.level!);
    return data;
  }

  const create = async (training: Training): Promise<Training> => {
    const { data } = await apiClient.post<Training>(`/${route}/create`, { ...training });
    return data;
  }

  const update = async (training: Training): Promise<Training> => {
    const { data } = await apiClient.put<Training>(`/${route}/update`, { ...training });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}