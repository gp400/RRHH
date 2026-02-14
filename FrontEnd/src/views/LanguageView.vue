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
  <CrudComponent
    :title
    :btn-text
    :reset
    :submit
    :headers
    :items
    :on-edit
    :on-delete
    :items-per-page-text
  >
    <v-form ref="formRef" @submit.prevent class="pt-3 px-3">
      <v-text-field
        class="mb-3"
        v-model="formData.name"
        label="Nombre"
        :rules="requiredRule"
      />
    </v-form>
  </CrudComponent>
</template>

<script setup lang="ts">
    import CrudComponent from '@/components/CrudComponent.vue';
    import { useLanguage } from '@/composables/useLanguage';
    import { Language } from '@/dto/Language';
    import { requiredRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';

    const { 
        getAll,
        getById,
        create,
        update
    } = useLanguage()

    const title = 'Idiomas';
    const btnText = 'Crear Idioma';
    const itemsPerPageText = 'Idiomas por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Language());

    const items = ref<Language[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');

    onMounted(async() => {
        items.value = await getAll();
    })

    const headers: DataTableHeader[] = [
        { title: 'Nombre', key: "name" },
        { title: 'Acciones', key: "actions", sortable: false },
    ]

    const submit = async (): Promise<boolean> => {
        let { valid } = await formRef.value!.validate();

        if (valid) {
            const values = {...formData.value}
            if (values.id){
                await update(values);
            } else {
                await create(values);
            }
            reset();
            items.value = await getAll();
        }

        return valid
    };

    const onEdit = async (id: number) => {
        formData.value = await getById(id);
    }

    const onDelete = async (values: Language) => {
    try {
      await update({ ...values, state: false })
      items.value = await getAll();
    } catch({ response: { data: { detail } } }: AxiosError) {
      showSnackbar.value = true;
      snackbarText.value = detail
    }
    }

    const reset = () => {
      formRef.value!.reset();
      formData.value = new Language();
    }
</script>