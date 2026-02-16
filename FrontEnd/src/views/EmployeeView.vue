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

      <v-textarea
        v-model="formData.description"
        label="Descripcion"
      />
    </v-form>
  </CrudComponent>
</template>

<script setup lang="ts">
    import CrudComponent from '@/components/CrudComponent.vue';
    import { useWorker } from '@/composables/useWorker';
    import { Worker } from '@/dto/Worker';
    import { requiredRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';
    import { WorkerType } from '@/enum/workerType';

    const { 
        getAll,
        getById,
        create,
        update
    } = useWorker()

    const title = 'Empleados';
    const btnText = 'Crear Empleado';
    const itemsPerPageText = 'Em por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Worker());

    const workerType = ref<WorkerType>(WorkerType.employee);
    const items = ref<Worker[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');

    onMounted(async() => {
        items.value = await getAll(workerType.value);
    })

    const headers: DataTableHeader[] = [
        { title: 'Cédula', key: "identification" },
        { title: 'Nombre', key: "name" },
        { title: 'Fecha Ingreso', key: "initial_date" },
        { title: 'Departamento', key: "department.name" },
        { title: 'Puesto', key: "position.name" },
        { title: 'Salario Mensual', key: "wage_text" },
        { title: 'Recomendado por', key: "recommended.name" },
        { title: 'Acciones', key: "actions", sortable: false },
    ]

    const submit = async (): Promise<boolean> => {
        let { valid } = await formRef.value!.validate();

        if (valid) {
            const values = {...formData.value, type: WorkerType.employee}
            if (values.id){
                await update(values);
            } else {
                await create(values);
            }
            reset();
            items.value = await getAll(workerType.value);
        }

        return valid
    };

    const onEdit = async (id: number) => {
        formData.value = await getById(id);
    }

    const onDelete = async (values: Worker) => {
    try {
      await update({ ...values, state: false })
      items.value = await getAll(workerType.value);
    } catch({ response: { data: { detail } } }: AxiosError) {
      showSnackbar.value = true;
      snackbarText.value = detail
    }
    }

    const reset = () => {
      formRef.value!.reset();
      formData.value = new Worker();
    }
</script>