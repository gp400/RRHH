import { PositionRiskLevel } from '../enum/positionRiskLevel';
export const parsePositionRiskLevel = (positionRiskLevel :PositionRiskLevel): string => {
    switch (positionRiskLevel) {
        case PositionRiskLevel.High:
            return "Alto";
        case PositionRiskLevel.Medium:
            return "Medio";
        case PositionRiskLevel.Low:
            return "Bajo";
        default:
            throw new Error("Nivel desconocida");
    }
}