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
            :items="levelOptions"
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
    import { useTraining } from '@/composables/useTraining';
    import { Training } from '@/dto/Training';
    import { TrainingLevel } from '@/enum/trainingLevel';
    import { parseTrainingLevel } from '@/utils/parseTrainingLevel';
    import { requiredRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';

    const { 
        getAll,
        getById,
        create,
        update
    } = useTraining()

    const title = 'Capacitaciones';
    const btnText = 'Crear Capacitacion';
    const itemsPerPageText = 'Capacitaciones por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Training());

    const items = ref<Training[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');
    const levelOptions = ref([
      { Id: TrainingLevel.Degree, Name: parseTrainingLevel(TrainingLevel.Degree) },
      { Id: TrainingLevel.Postgraduate, Name: parseTrainingLevel(TrainingLevel.Postgraduate) },
      { Id: TrainingLevel.Mastery, Name: parseTrainingLevel(TrainingLevel.Mastery) },
      { Id: TrainingLevel.Doctorate, Name: parseTrainingLevel(TrainingLevel.Doctorate) },
      { Id: TrainingLevel.Technical, Name: parseTrainingLevel(TrainingLevel.Technical) },
      { Id: TrainingLevel.Management, Name: parseTrainingLevel(TrainingLevel.Management) },
    ]);

    onMounted(async() => {
        items.value = await getAll();
    })

    const headers: DataTableHeader[] = [
        { title: 'Nivel', key: "level_text" },
        { title: 'Fecha Desde', key: "initial_date" },
        { title: 'Fecha Hasta', key: "end_date" },
        { title: 'Institución', key: "institution" },
        { title: 'Descripción', key: "description" },
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

    const onDelete = async (values: Training) => {
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
      formData.value = new Training();
    }
</script>