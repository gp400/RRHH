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
          <v-text-field
            v-model="formData.wage"
            type="number"
            label="Salario al que aspira"
            min="1"
            :rules="[ ...requiredRule, ...greaterOrEqualThanRule(1) ]"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.recommended_id"
            :items="employeeOptions"
            item-title="name"
            item-value="id"
            label="Recomendado por"
            clearable
          />
        </v-col>
        <v-col cols="12">
          <div class="d-flex">
            <v-select
              v-model="competenceId"
              :items="competenceOptions.filter(competence => 
                !formData.worker_competences.some(wc => wc.competence_id === competence.id)
              )"
              item-title="name"
              item-value="id"
              label="Competencias"
            />
            <div class="ps-2">
              <v-btn icon color="blue add-btn" @click="addBtn">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </div>
          <v-data-table
            v-if="formData.worker_competences.length > 0"
            :headers="medicineHeadersAction"
            :items="formData.worker_competences"
            class="elevation-1 mt-2"
            hide-default-footer
            hide-actions
          >
            <template #item.Delete="{ item }">
              <v-btn icon color="red" class="delete-btn" @click="onDeleteCompetence(item)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-col>
        <v-col cols="12">
          <div class="d-flex">
            <v-select
              v-model="trainingId"
              :items="trainingOptions.filter(training => 
                !formData.worker_trainings.some(wt => wt.training_id === training.id)
              )"
              item-title="name"
              item-value="id"
              label="Competencias"
              ref="medicineSelect"
            />
            <div class="ps-2">
              <v-btn icon color="blue add-btn" @click="addBtn">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </div>
          <v-data-table
            v-if="formData.worker_competences.length > 0"
            :headers="medicineHeadersAction"
            :items="formData.worker_competences"
            class="elevation-1 mt-2"
            hide-default-footer
            hide-actions
          >
            <template #item.Delete="{ item }">
              <v-btn icon color="red" class="delete-btn" @click="onDeleteCompetence(item)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-form>
  </CrudComponent>
</template>

<style scoped>
  .add-btn {
    height: 55px;
    width: 55px;
  }

  .delete-btn {
    height: 40px;
    width: 40px;
  }
</style>

<script setup lang="ts">
    import CrudComponent from '@/components/CrudComponent.vue';
    import { useCompetence } from '@/composables/useCompetence';
    import { useDepartment } from '@/composables/useDepartment';
    import { usePosition } from '@/composables/usePosition';
    import { useTraining } from '@/composables/useTraining';
    import { useWorker } from '@/composables/useWorker';
    import { Competence } from '@/dto/Competence';
    import { Department } from '@/dto/Department';
    import { Position } from '@/dto/Position';
    import { Training } from '@/dto/Training';
    import { Worker } from '@/dto/Worker';
    import { WorkerCompetence } from '@/dto/WorkerCompetence';
    import { WorkerType } from '@/enum/workerType';
    import { parseWorkerType } from '@/utils/parseWorkerType';
    import { numberRule, requiredRule, maxLengthRule, identificacionRule, greaterOrEqualThanRule, validateList } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';

    const { getAll: getAllPositions } = usePosition()
    const { getAll: getAllDepartments } = useDepartment()
    const { getAll: getAllCompetences } = useCompetence()
    const { getAll: getAllTraining } = useTraining()

    const { 
        getAll,
        getById,
        create,
        update
    } = useWorker()

    const title = 'Candidatos';
    const btnText = 'Crear Candidato';
    const itemsPerPageText = 'Candidatos por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Worker());
    const competenceId = ref<number | null>(null);

    const indentificationCounter = ref<number>(11);
    const workerType = ref<WorkerType>(WorkerType.candidate);
    const items = ref<Worker[]>([]);
    const positionOptions = ref<Position[]>([]);
    const departmentOptions = ref<Department[]>([]);
    const employeeOptions = ref<Worker[]>([]);
    const competenceOptions = ref<Competence[]>([]);
    const trainingOptions = ref<Training[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');
    const workerTypeOptions = ref([
      { Id: WorkerType.candidate, Name: parseWorkerType(WorkerType.candidate) },
      { Id: WorkerType.employee, Name: parseWorkerType(WorkerType.employee) },
    ]);

    onMounted(async() => {
        items.value = await getAll(workerType.value);
        positionOptions.value = await getAllPositions();
        departmentOptions.value = await getAllDepartments();
        employeeOptions.value = await getAll(WorkerType.employee);
        competenceOptions.value = await getAllCompetences();
        trainingOptions.value = await getAllTraining();
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

    const competenceHeaders: DataTableHeader[] = [
      { title: 'Nombre', key: "competence.name" },
    ]

    const medicineHeadersAction: DataTableHeader[] = [
      ...competenceHeaders.values(),
      { title: 'Acciones', key: "Delete", sortable: false },
    ]

    const filterNumbers = (value: InputEvent, prop: string) => {
        const validator = numberRule[0]!;
        if (validator(value.data as string) !== true && value.data) {
            formData.value[prop] = (formData.value[prop] as string).replace(value.data, '');
        }
    }

    const submit = async (): Promise<boolean> => {
        let { valid } = await formRef.value!.validate();

        if (valid) {
            const values = {...formData.value, type: WorkerType.candidate};
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

  const addBtn = () => {
    formData.value.worker_competences.push({
      id: null,
      worker_id: null,
      competence_id: competenceId.value,
      competence: competenceOptions.value.find(c => c.id == competenceId.value)!,
      state: true
    });
    competenceId.value = null;
  }

  const onDeleteCompetence = async (values: WorkerCompetence) => {
    formData.value.worker_competences = formData.value.worker_competences.filter(wc => wc.competence_id !== values.competence_id);
  }
</script>