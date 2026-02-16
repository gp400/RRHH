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

  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title>Seleccionar Candidado</v-card-title>

      <v-form ref="formLaboralRef" @submit.prevent class="pt-3 px-3">
        <v-text-field
          v-model="formData.initial_date"
          type="date"
          label="Fecha de Inicio Laboral"
          :rules="requiredRule"
          clearable
        />
      </v-form>
      
      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn class="text-none" color="red" @click="onCancelHire"> Cancelar </v-btn>

        <v-btn class="text-none" color="primary" @click="submit"> Guardar </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <CrudComponent
    :title
    :btn-text
    :reset
    :submit
    :headers
    :items
    :on-edit
    :on-delete
    :on-update="onHire"
    :items-per-page-text
    :disabled="isAddingExperience"
    :competence-headers
    :training-headers
    :experience-headers
    :show-expand
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
              <v-btn icon color="blue add-btn" @click="addCompetenceBtn">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </div>
          <v-data-table
            v-if="formData.worker_competences.length > 0"
            :headers="competenceHeadersAction"
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
              :item-title="item => `${item.institution}-${parseTrainingLevel(item.level)}`"
              item-value="id"
              label="Capacitaciones"
            />
            <div class="ps-2">
              <v-btn icon color="blue add-btn" @click="addTrainingBtn">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>
          </div>
          <v-data-table
            v-if="formData.worker_trainings.length > 0"
            :headers="trainingHeadersAction"
            :items="formData.worker_trainings"
            class="elevation-1 mt-2"
            hide-default-footer
            hide-actions
          >
            <template #item.Delete="{ item }">
              <v-btn icon color="red" class="delete-btn" @click="onDeleteTraining(item)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-col>
        <v-col cols="12">
          <div v-if="!isAddingExperience" class="text-end" @click="() => { isAddingExperience = true }">
            <v-btn color="primary" class="text-none">Agregar experiencia</v-btn>
          </div>
          <div v-else class="mt-3">
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                    v-model="experience.company"
                    label="Empresa"
                    :rules="[...requiredRule]"
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                    v-model="experience.position"
                    label="Puesto"
                    :rules="[...requiredRule]"
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="experience.wage"
                  type="number"
                  label="Salario"
                  min="1"
                  :rules="[ ...requiredRule, ...greaterOrEqualThanRule(1) ]"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="experience.initial_date"
                  type="date"
                  label="Fecha Desde"
                  :max="experience.end_date"
                  :rules="requiredRule"
                  clearable
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="experience.end_date"
                  type="date"
                  label="Fecha Hasta"
                  :min="experience.initial_date"
                  :rules="requiredRule"
                  clearable
                />
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="experience.description"
                  label="Descripción"
                  hide-details
                />
              </v-col>
              <v-col cols="12">
                <div class="d-flex flex-wrap justify-end">
                  <div class="pa-2">
                    <v-btn color="red" class="text-none" @click="onCancelExp">Cancelar</v-btn>
                  </div>
                  <div class="pa-2">
                    <v-btn color="primary" class="text-none" @click="onEditExpList(experience, undefined)">Guardar</v-btn>
                  </div>
                </div>
              </v-col>
            </v-row>
          </div>
          <v-data-table
            v-if="formData.experiences.length > 0"
            :headers="experienceHeadersAction"
            :items="formData.experiences"
            class="elevation-1 mt-2"
            hide-default-footer
            hide-actions
          >
            <template #item.Actions="{ item }">
              <div class="d-flex flex-wrap justify-end">
                <div class="pa-1">
                  <v-btn icon color="yellow" class="inner-modal-btn" @click="onEditExp(item)">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </div>
                <div class="pa-1">
                  <v-btn icon color="red" class="inner-modal-btn" @click="onEditExpList(undefined, item)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </div>
              </div>
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

  .inner-modal-btn {
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
    import { Experience } from '@/dto/Experience';
    import { Position } from '@/dto/Position';
    import { Training } from '@/dto/Training';
    import { Worker } from '@/dto/Worker';
    import { WorkerCompetence } from '@/dto/WorkerCompetence';
    import { WorkerTraining } from '@/dto/WorkerTraining';
    import { WorkerType } from '@/enum/workerType';
    import { parseTrainingLevel } from '@/utils/parseTrainingLevel';
    import { numberRule, requiredRule, maxLengthRule, identificacionRule, greaterOrEqualThanRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';
    import { shallowEqual } from '@/utils/shallowEqual';

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

    const showExpand = true;
    const title = 'Candidatos';
    const btnText = 'Crear Candidato';
    const itemsPerPageText = 'Candidatos por pagina'

    const dialog = ref<boolean>(false);
    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formLaboralRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Worker());
    const competenceId = ref<number | null>(null);
    const trainingId = ref<number | null>(null);
    const isAddingExperience = ref<boolean>(false);
    const experience = ref<Experience>(new Experience());
    const oldExperience = ref<Experience | null>(null);

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
        { title: 'Salario', key: "wage_text" },
        { title: 'Recomendado por', key: "recommended.name" },
        { title: 'Acciones', key: "actions", sortable: false },
    ]

    const competenceHeaders: DataTableHeader[] = [
      { title: 'Nombre', key: "competence.name" },
      { title: 'Descripcion', key: "competence.description" },
    ]

    const competenceHeadersAction: DataTableHeader[] = [
      ...competenceHeaders.values(),
      { title: 'Acciones', key: "Delete", sortable: false },
    ]

    const trainingHeaders: DataTableHeader[] = [
        { title: 'Nivel', key: "training.level_text" },
        { title: 'Fecha Desde', key: "training.initial_date" },
        { title: 'Fecha Hasta', key: "training.end_date" },
        { title: 'Institución', key: "training.institution" },
        { title: 'Descripción', key: "training.description" },
    ]

    const trainingHeadersAction: DataTableHeader[] = [
      ...trainingHeaders.values(),
      { title: 'Acciones', key: "Delete", sortable: false },
    ]

    const experienceHeaders: DataTableHeader[] = [
        { title: 'Empresa', key: "company" },
        { title: 'Puesto', key: "position" },
        { title: 'Fecha Desde', key: "initial_date" },
        { title: 'Fecha Fin', key: "end_date" },
        { title: 'Salario', key: "wage" },
        { title: 'Descripcion', key: "description" },
    ]

    const experienceHeadersAction: DataTableHeader[] = [
      ...experienceHeaders.values(),
      { title: 'Acciones', key: "Actions", sortable: false },
    ]

    const filterNumbers = (value: InputEvent, prop: string) => {
        const validator = numberRule[0]!;
        if (validator(value.data as string) !== true && value.data) {
            formData.value[prop] = (formData.value[prop] as string).replace(value.data, '');
        }
    }

    const submit = async (): Promise<boolean> => {
        const form = formRef.value ?? formLaboralRef.value;
        let { valid } = await form!.validate();

        if (valid) {
            const values = {...formData.value, type: formData.value.type ?? WorkerType.candidate};
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
        formData.value.experiences = formData.value.experiences.sort((a, b) => new Date(a.initial_date!).getTime() - new Date(b.initial_date!).getTime());
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

    const onHire = async (id: number) => {
        await onEdit(id);
        formData.value.type = WorkerType.employee;
        dialog.value=true;
    }

    const onCancelHire = () => {
      dialog.value = false;
      formData.value = new Worker();
    }

    const reset = () => {
      formRef.value?.reset();
      formLaboralRef.value?.reset();
      formData.value = new Worker();
      isAddingExperience.value = false
      dialog.value = false;
      experience.value = new Experience();
    }

  const addCompetenceBtn = () => {
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

  const addTrainingBtn = () => {
    formData.value.worker_trainings.push({
      id: null,
      worker_id: null,
      training_id: trainingId.value,
      training: trainingOptions.value.find(c => c.id == trainingId.value)!,
      state: true
    });
    trainingId.value = null;
  }

  const onDeleteTraining = async (values: WorkerTraining) => {
    formData.value.worker_trainings = formData.value.worker_trainings.filter(wt => wt.training_id !== values.training_id);
  }

  const onEditExp = (oldExp: Experience) => {
    isAddingExperience.value = true
    experience.value = { ...oldExp };
    oldExperience.value = { ...oldExp };
  }

  const onEditExpList = (newExp?: Experience, oldExp?: Experience) => {

    if (oldExperience.value) formData.value.experiences = formData.value.experiences.filter(exp => !shallowEqual(exp, oldExperience.value));
    if (oldExp) formData.value.experiences = formData.value.experiences.filter(exp => !shallowEqual(exp, oldExp));
    if (newExp) formData.value.experiences.push(newExp);
    formData.value.experiences = formData.value.experiences.sort((a, b) => new Date(a.initial_date!).getTime() - new Date(b.initial_date!).getTime());

    oldExperience.value = null;
    onCancelExp();
  }

  const onCancelExp = () => {
    experience.value = new Experience();
    isAddingExperience.value = false;
  }
</script>