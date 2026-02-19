<template>
  <v-snackbar
    v-model="showSnackbar"
    :timeout="5000"
    color="yellow"
    location="top right"
  >
  <div class="d-flex">
    <v-icon
      color="black"
      icon="mdi-alert-circle"
    ></v-icon>
    <div style="margin-left: 5px;">
      {{ snackbarText }}
    </div>
  </div>
  </v-snackbar>
  <v-app>
    <v-main class="fill-heigh bg-primary">
      <v-container
        fluid
        class="d-flex justify-center align-center fill-height"
      >
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <div class="bg-white pa-4 rounded">
                <h5 class="text-h5 text-center font-weight-bold">Iniciar Sesion</h5>
                <v-form ref="formRef" @submit.prevent>
                    <v-text-field
                        class="mt-2"
                        v-model="formData.email"
                        label="Email"
                        :rules="[ ...requiredRule, ...emailRule]"
                    />
                    <v-text-field
                        class="mt-2"
                        v-model="formData.password"
                        label="Contraseña"
                        type="password"
                        :rules="requiredRule"
                    />
                    <v-btn block class="text-none mt-2" color="primary" @click="submit">
                        Enviar
                    </v-btn>
                </v-form>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>


<script setup lang="ts">
import { useUser } from '@/composables/useUser';
import { User } from '@/dto/User';
import { emailRule, requiredRule } from '@/utils/Validations';
import { AxiosError } from 'axios';
import { ref } from 'vue';
import { VForm } from 'vuetify/components';
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';

const { 
    login
} = useUser()

const router = useRouter()
const authStore = useAuthStore()

const formData = ref(new User());
const formRef = ref<InstanceType<typeof VForm> | null>(null);

const showSnackbar = ref<boolean>(false);
const snackbarText = ref<string>('');

const submit = async (): Promise<void> => {

  let { valid } = await formRef.value!.validate();

  if (valid) {
      try {
          let jwt: string = await login(formData.value);
          authStore.setJWT(jwt)
          router.push('/')
      } catch({ response: { data: { detail } } }: AxiosError) {
          console.log(detail)
          showSnackbar.value = true;
          snackbarText.value = detail
      }
  }
};

</script>