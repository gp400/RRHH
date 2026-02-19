<template>
    <h3 class="text-h3 text-center">Reporte de Empleados</h3>

    <v-row justify="space-between" class="align-center mt-0">
        <v-col cols="6">
            <v-btn color="primary" class="text-none" @click="downloadPdf" :disabled="!isDateRangeValid">Imprimir</v-btn>
        </v-col>
        <v-col>
            <v-row justify="end">
                <v-col cols="12">
                <v-row justify="end">
                    <v-col cols="12" md="6">
                    <v-text-field
                        type="date"
                        label="Fecha Inicio"
                        v-model="initialDate"
                        :max="endDate"
                        clearable
                        hide-details
                        @update:model-value="setItems"
                    />
                    </v-col>
                    <v-col cols="12" md="6">
                    <v-text-field
                        type="date"
                        label="Fecha Fin"
                        v-model="endDate"
                        :min="initialDate"
                        clearable
                        hide-details
                        @update:model-value="setItems"
                    />
                    </v-col>
                </v-row>
                </v-col>
            </v-row>
        </v-col>
    </v-row>

    <div ref="pdfContent" class="mt-9" v-if="isDateRangeValid">
        <h4 class="text-h4 text-center">Empleados Nuevos</h4>
        <DataTableComponent
            :items="items.sort((a, b) => new Date(a.initial_date!).getTime() - new Date(b.initial_date!).getTime())"
            :headers
            items-per-page
            hide-default-footer
        />
    </div>
    <div class="mt-10" v-else>
        <p class="text-center font-weight-bold">Ingrese el rango de fechas</p>
    </div>
</template>

<script setup lang="ts">
    import { useWorker } from '@/composables/useWorker';
    import { computed, ref } from 'vue';
    import { Worker } from '@/dto/Worker';
    import { WorkerType } from '@/enum/workerType';
    import DataTableComponent from '@/components/DataTableComponent.vue';
import html2pdf from 'html2pdf.js';

    const { 
        getAll
    } = useWorker()

    const headers: DataTableHeader[] = [
        { title: 'Cédula', key: "identification" },
        { title: 'Nombre', key: "name" },
        { title: 'Fecha Ingreso', key: "initial_date" },
        { title: 'Departamento', key: "department.name" },
        { title: 'Puesto', key: "position.name" },
        { title: 'Salario Mensual', key: "wage_text" }
    ]

    const items = ref<Worker[]>([]);
    const endDate = ref<Date | null>(null);
    const initialDate = ref<Date | null>(null);
    const pdfContent = ref<HTMLDivElement | null>(null);

    const isDateRangeValid = computed(() => !!(initialDate.value || endDate.value))

    const setItems = async() => items.value = isDateRangeValid
                                                ? await getAll({ worker_type: WorkerType.employee, initial_date: initialDate.value, end_date: endDate.value }) 
                                                : []
    
    const downloadPdf = async() => {
        html2pdf()
            .set({
            filename: "Empleados Nuevos.pdf",        // name of the downloaded file
            margin: 0.5,                        // optional margins
            jsPDF: { unit: "in", format: "letter" },
            })
            .from(pdfContent.value!.innerHTML)
            .save(); 
    }

</script>