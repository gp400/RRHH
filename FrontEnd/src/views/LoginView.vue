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
        <div class="bg-white pa-4 rounded w-50">
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

const { 
    login
} = useUser()

const formData = ref(new User());
const formRef = ref<InstanceType<typeof VForm> | null>(null);

const showSnackbar = ref<boolean>(false);
const snackbarText = ref<string>('');

const submit = async (): Promise<void> => {
    let { valid } = await formRef.value!.validate();

    if (valid) {
        try {
            await login(formData.value)
        } catch({ response: { data: { detail } } }: AxiosError) {
            console.log(detail)
            showSnackbar.value = true;
            snackbarText.value = detail
        }
    }
};

</script>