import type { User } from "@/dto/User";
import apiClient from "@/utils/apiClient";

const route: String = "user";

export function useUser() {
  
  const login = async (user: User): Promise<string> => {
    const { data } = await apiClient.post<string>(`/${route}/login`, { ...user });
    return data;
  } 

  return {
    login
  }
}