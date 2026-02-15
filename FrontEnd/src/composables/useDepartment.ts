import type { Department } from '@/dto/Department';
import apiClient from '@/utils/apiClient';

const route: String = "department";

export function useDepartment() {
  
  const getAll = async (): Promise<Department[]> => {
    const { data } = await apiClient.get<Department[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<Department> => {
    const { data } = await apiClient.get<Department>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (department: Department): Promise<Department> => {
    const { data } = await apiClient.post<Department>(`/${route}/create`, { ...department });
    return data;
  }

  const update = async (department: Department): Promise<Department> => {
    const { data } = await apiClient.put<Department>(`/${route}/update`, { ...department });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}