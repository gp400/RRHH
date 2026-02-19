import { defineStore } from "pinia";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        JWT: ''
    }),

    persist: true,

    actions: {
        setJWT(JWT: string) {
            this.JWT = JWT
        },
        clear() {
            this.JWT = ''
        }
    }
})