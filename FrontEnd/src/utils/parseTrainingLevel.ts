import { TrainingLevel } from "@/enum/trainingLevel";

export const parseTrainingLevel = (trainingLevel: TrainingLevel): string => {
    switch (trainingLevel) {
        case TrainingLevel.Degree:
            return "Grado";
        case TrainingLevel.Postgraduate:
            return "Post-grado";
        case TrainingLevel.Mastery:
            return "Maestría";
        case TrainingLevel.Doctorate:
            return "Doctorado";
        case TrainingLevel.Technical:
            return "Técnico";
        case TrainingLevel.Management:
            return "Gestión";
        default:
            throw new Error("Nivel desconocido");
    }
}