<template>
  <v-data-table
    :headers
    :items
    :show-expand
    :search
    v-model:expanded="expanded"
    item-value="id"
    class="elevation-1 mt-3"
    :items-per-page-text="`${itemsPerPageText}:`"
    :items-per-page
    :hide-default-footer
    :no-data-text="noDataText"
  >
    <template #expanded-row="{ item, columns }">
      <td :colspan="columns.length">
        
        <h3 class="w-90 ml-auto my-3">Competencias</h3>
        <v-data-table
          :headers="competenceHeaders"
          :items="item.worker_competences"
          class="w-90 ml-auto nested-table"
          hide-default-footer
          :no-data-text="noDataText"
        />

        <h3 class="w-90 ml-auto my-3">Capacitaciones</h3>
        <v-data-table
          :headers="trainingHeaders"
          :items="item.worker_trainings"
          class="w-90 ml-auto nested-table my-4"
          hide-default-footer
          :no-data-text="noDataText"
        />

        <h3 class="w-90 ml-auto my-3">Experiencia Laboral</h3>
        <v-data-table
          :headers="experienceHeaders"
          :items="item.experiences"
          class="w-90 ml-auto nested-table my-4"
          hide-default-footer
          :no-data-text="noDataText"
        />
      </td>
    </template>
    <template #item.actions="{ item }">
      <div class="d-flex flex-wrap">
        <div class="pa-2">
          <v-btn icon color="yellow" @click="onEdit(item.id!)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </div>
        <div class="pa-2">
          <v-btn icon color="red" @click="onDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </div>
      </div>
    </template>
  </v-data-table>
</template>

<style>
  .nested-table {
    border: 1px solid #D4D4D4;
  }
</style>

<script setup lang="ts">
  
  import { ref } from 'vue';
  import { DataTableHeader } from 'vuetify';

  const props = defineProps<{
    competenceHeaders: DataTableHeader[],
    trainingHeaders: DataTableHeader[],
    experienceHeaders: DataTableHeader[],
    itemsPerPageText: String,
    itemsPerPage: number,
    hideDefaultFooter: boolean,
    onEdit: Function,
    onDelete: Function
  }>()
  
  const noDataText = 'No existen registros'
  const expanded = ref([]);
</script>