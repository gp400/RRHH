import { Language } from '@/dto/Language';
import apiClient from '@/utils/apiClient';

const route: String = "language";

export function useLanguage() {
  
  const getAll = async (): Promise<Language[]> => {
    const { data } = await apiClient.get<Language[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<Language> => {
    const { data } = await apiClient.get<Language>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (language: Language): Promise<Language> => {
    const { data } = await apiClient.post<Language>(`/${route}/create`, { ...language });
    return data;
  }

  const update = async (language: Language): Promise<Language> => {
    const { data } = await apiClient.put<Language>(`/${route}/update`, { ...language });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}