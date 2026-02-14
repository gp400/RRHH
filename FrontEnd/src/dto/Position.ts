import type { PositionRiskLevel } from "@/enum/positionRiskLevel";

export class Position {
    id: number | null = null;
    name: string = "";
    risk_level: PositionRiskLevel | null = null
    min_wage: number | null = null;
    max_wage: number | null = null;
    state: boolean = true
    risk_level_text: string = ''
    min_wage_text: string = ''
    max_wage_text: string = ''
}