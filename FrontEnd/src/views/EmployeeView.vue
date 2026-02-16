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
              v-model="formData.identification"
              label="Cédula (Sin guiones)"
              :rules="[...requiredRule, ...numberRule, ...maxLengthRule(indentificationCounter), ...identificacionRule]"
              @input="(e: InputEvent) => filterNumbers(e, 'identification')"
              :counter="indentificationCounter"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
              v-model="formData.name"
              label="Nombre"
              :rules="requiredRule"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.initial_date"
            type="date"
            label="Fecha Inicio"
            :rules="requiredRule"
            clearable
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.department_id"
            :items="departmentOptions"
            item-title="name"
            item-value="id"
            label="Departamento"
            :rules="requiredRule"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.position_id"
            :items="positionOptions"
            item-title="name"
            item-value="id"
            label="Puesto al que aspira"
            :rules="requiredRule"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.wage"
            type="number"
            label="Salario Mensual"
            min="1"
            :rules="[ ...requiredRule, ...greaterOrEqualThanRule(1) ]"
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
    import { requiredRule, numberRule, maxLengthRule, identificacionRule, greaterOrEqualThanRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';
    import { WorkerType } from '@/enum/workerType';
    import { usePosition } from '@/composables/usePosition';
    import { useDepartment } from '@/composables/useDepartment';
    import { Position } from '@/dto/Position';
    import { Department } from '@/dto/Department';

    const { getAll: getAllPositions } = usePosition()
    const { getAll: getAllDepartments } = useDepartment()

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

    const indentificationCounter = ref<number>(11);
    const workerType = ref<WorkerType>(WorkerType.employee);
    const items = ref<Worker[]>([]);
    const positionOptions = ref<Position[]>([]);
    const departmentOptions = ref<Department[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');

    onMounted(async() => {
        items.value = await getAll(workerType.value);
        positionOptions.value = await getAllPositions();
        departmentOptions.value = await getAllDepartments();
    })

    const headers: DataTableHeader[] = [
        { title: 'Cédula', key: "identification" },
        { title: 'Nombre', key: "name" },
        { title: 'Fecha Ingreso', key: "initial_date" },
        { title: 'Departamento', key: "department.name" },
        { title: 'Puesto', key: "position.name" },
        { title: 'Salario Mensual', key: "wage_text" },
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