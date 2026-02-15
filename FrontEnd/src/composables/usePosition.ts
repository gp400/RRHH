import { Position } from '@/dto/Position';
import apiClient from '@/utils/apiClient';
import { parsePositionRiskLevel } from '@/utils/parsePositionRiskLevel';
import { salaryFormatter } from '@/utils/salaryFormatter';

const route: String = "position";

export function usePosition() {
  
  const getAll = async (): Promise<Position[]> => {
    const { data } = await apiClient.get<Position[]>(`/${route}/get_all`);
    data.forEach(position => {
      position.risk_level_text = parsePositionRiskLevel(position.risk_level!);
      position.max_wage_text = salaryFormatter(position.max_wage!)
      position.min_wage_text = salaryFormatter(position.min_wage!)
    })
    return data;
  } 

  const getById = async (id: number): Promise<Position> => {
    const { data } = await apiClient.get<Position>(`/${route}/get_by_id/${id}`);
    data.risk_level_text = parsePositionRiskLevel(data.risk_level!);
    data.max_wage_text = salaryFormatter(data.max_wage!)
    data.min_wage_text = salaryFormatter(data.min_wage!)
    return data;
  }

  const create = async (position: Position): Promise<Position> => {
    const { data } = await apiClient.post<Position>(`/${route}/create`, { ...position });
    return data;
  }

  const update = async (position: Position): Promise<Position> => {
    const { data } = await apiClient.put<Position>(`/${route}/update`, { ...position });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}