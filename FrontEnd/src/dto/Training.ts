import type { TrainingLevel } from "@/enum/trainingLevel";

export class Training {
    id: number | null = null;
    description: string = "";
    level: TrainingLevel | null = null;
    initial_date: Date | null = null;
    end_date: Date | null = null;
    institution: string = '';
    state: boolean = true;
    level_text: string = '';
}