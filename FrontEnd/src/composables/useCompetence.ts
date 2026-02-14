import { Competence } from '@/dto/Competence';
import apiClient from '@/utils/apiClient';

const route: String = "competence";

export function useCompetence() {
  
  const getAll = async (): Promise<Competence[]> => {
    const { data } = await apiClient.get<Competence[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<Competence> => {
    const { data } = await apiClient.get<Competence>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (competence: Competence): Promise<Competence> => {
    const { data } = await apiClient.post<Competence>(`/${route}/create`, { ...competence });
    return data;
  }

  const update = async (competence: Competence): Promise<Competence> => {
    const { data } = await apiClient.put<Competence>(`/${route}/update`, { ...competence });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}