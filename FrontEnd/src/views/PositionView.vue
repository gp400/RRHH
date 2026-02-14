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
              v-model="formData.name"
              label="Nombre"
              :rules="requiredRule"
            />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            v-model="formData.risk_level"
            :items="riskLevelOptions"
            item-title="Name"
            item-value="Id"
            label="Nivel de Riesgo"
            :rules="requiredRule"
          />
        </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.min_wage"
              type="number"
              label="Nivel Mínimo Salario"
              min="1"
              :rules="[ ...requiredRule, ...greaterOrEqualThanRule(1), ...maxValueRule(formData.max_wage) ]"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.max_wage"
              type="number"
              label="Nivel Máximo Salario"
              min="1"
              :rules="[ ...requiredRule, ...greaterOrEqualThanRule(1),...minValueRule(formData.min_wage) ]"
            />
          </v-col>
      </v-row>
    </v-form>
  </CrudComponent>
</template>

<script setup lang="ts">
    import CrudComponent from '@/components/CrudComponent.vue';
    import { usePosition } from '@/composables/usePosition';
    import { Position } from '@/dto/Position';
    import { requiredRule, greaterOrEqualThanRule, maxValueRule, minValueRule } from '@/utils/Validations';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';
    import { PositionRiskLevel } from '../enum/positionRiskLevel';
    import { parsePositionRiskLevel } from '@/utils/parsepositionRiskLevel';

    const { 
        getAll,
        getById,
        create,
        update
    } = usePosition()

    const title = 'Puestos';
    const btnText = 'Crear Puesto';
    const itemsPerPageText = 'Puestos por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Position());

    const items = ref<Position[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');
    const riskLevelOptions = ref([
      { Id: PositionRiskLevel.High, Name: parsePositionRiskLevel(PositionRiskLevel.High) },
      { Id: PositionRiskLevel.Medium, Name: parsePositionRiskLevel(PositionRiskLevel.Medium) },
      { Id: PositionRiskLevel.Low, Name: parsePositionRiskLevel(PositionRiskLevel.Low) },
    ]);

    onMounted(async() => {
        items.value = await getAll();
    })

    const headers: DataTableHeader[] = [
        { title: 'Nombre', key: "name" },
        { title: 'Nivel de Riesgo', key: "risk_level_text" },
        { title: 'Nivel Mínimo Salario', key: "min_wage_text" },
        { title: 'Nivel Máximo Salario', key: "max_wage_text" },
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

    const onDelete = async (values: Position) => {
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
      formData.value = new Position();
    }
</script>