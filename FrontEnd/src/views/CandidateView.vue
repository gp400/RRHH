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
      <v-row>
        <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.institution"
              label="Institucion"
              :rules="requiredRule"
            />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.level"
            :items="workerTypeOptions"
            item-title="Name"
            item-value="Id"
            label="Nivel"
            :rules="requiredRule"
          />
        </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.initial_date"
              type="date"
              label="Fecha Desde"
              :max="formData.end_date"
              :rules="requiredRule"
              clearable
          />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.end_date"
              type="date"
              label="Fecha Hasta"
              :min="formData.initial_date"
              :rules="requiredRule"
              clearable
            />
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="formData.description"
              label="Descripción"
              :rules="requiredRule"
            />
          </v-col>
      </v-row>
    </v-form>
  </CrudComponent>
</template>

<script setup lang="ts">
    import CrudComponent from '@/components/CrudComponent.vue';
    import { useWorker } from '@/composables/useWorker';
    import { Worker } from '@/dto/Worker';
    import { WorkerType } from '@/enum/workerType';
import { parseWorkerType } from '@/utils/parseWorkerType';
    import { requiredRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';

    const { 
        getAll,
        getById,
        create,
        update
    } = useWorker()

    const title = 'Capacitaciones';
    const btnText = 'Crear Capacitacion';
    const itemsPerPageText = 'Capacitaciones por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Worker());

    const workerType = ref<WorkerType>(WorkerType.candidate);
    const items = ref<Worker[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');
    const workerTypeOptions = ref([
      { Id: WorkerType.candidate, Name: parseWorkerType(WorkerType.candidate) },
      { Id: WorkerType.employee, Name: parseWorkerType(WorkerType.employee) },
    ]);

    onMounted(async() => {
        items.value = await getAll(workerType.value);
    })

    const headers: DataTableHeader[] = [
        { title: 'Cédula', key: "identification" },
        { title: 'Nombre', key: "name" },
        { title: 'Puesto', key: "position.name" },
        { title: 'Departamento', key: "department.name" },
        { title: 'Salario', key: "wage" },
        { title: 'Recomendado por', key: "recommended.name" },
        { title: 'Acciones', key: "actions", sortable: false },
    ]

    const submit = async (): Promise<boolean> => {
        let { valid } = await formRef.value!.validate();

        if (valid) {
            const values = {...formData.value, workerType: WorkerType.candidate}
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