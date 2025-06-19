import math


CALC_REGISTRY = {}

def register_calc(name):
    def decorator(func):
        CALC_REGISTRY[name] = func
        return func
    return decorator


## Medical dosage and Administration calculations ##
@register_calc("Dosage by Weight")
def dosage_by_weight(dosePerKg: float, weight: float) -> float:
    """
    Calculates the appropriate drug dosage based on a patient's weight.
    Formula: Dosage = Dose per kg × Weight (kg)
    """
    return dosePerKg * weight


@register_calc("IV Flow Rate")
def iv_flow_rate(volume: float, time: float) -> float:
    """
    Calculates the IV flow rate in mL per hour for proper administration.
    Formula: Flow Rate (mL/hr) = Volume (mL) / Time (hr)
    """
    return volume / time


@register_calc("Drip Rate")
def drip_rate(volume: float, dropFactor: float, time: float) -> float:
    """
    Calculates the number of drops per minute for an IV infusion.
    Formula: Drip Rate (gtt/min) = (Volume (mL) × Drop factor (gtt/mL)) / Time (min)
    """
    return (volume * dropFactor) / time


@register_calc("Medication Dose (Volume to Administer)")
def medication_dose_volume_to_administer(desiredDose: float, stockStrength: float) -> float:
    """
    Calculates the required volume to administer based on the desired dose and available concentration.
    Formula: Volume to administer (mL) = Desired Dose (mg) / Stock Strength (mg/mL)
    """
    return desiredDose / stockStrength


@register_calc("Medication Dose (Amount of Drug Required)")
def medication_dose_amount_of_drug_required(desiredConcentration: float, finalVolume: float) -> float:
    """
    Calculates the amount of drug needed to achieve a desired concentration in a given final volume.
    Formula: Amount of drug (mg) = Desired Concentration (mg/mL) × Final Volume (mL)
    """
    return desiredConcentration * finalVolume


@register_calc("Insulin Dose Calculation")
def insulin_dose(currentGlucose: float, targetGlucose: float, correctionFactor: float) -> float:
    """
    Calculates insulin dose based on blood glucose levels and correction factor.
    Formula: Insulin dose = (Current glucose - Target glucose) / Correction factor
    """
    return (currentGlucose - targetGlucose) / correctionFactor


@register_calc("Pediatric Dosage (Young's Rule)")
def pediatric_dosage_youngs_rule(age: float, adultDose: float) -> float:
    """
    Calculates pediatric drug dose using Young's Rule.
    Formula: Pediatric Dose = (Age ÷ (Age + 12)) × Adult Dose
    """
    return (age / (age + 12)) * adultDose


@register_calc("Pediatric Dosage (Clark's Rule)")
def pediatric_dosage_clarks_rule(weight: float, adultDose: float) -> float:
    """
    Calculates pediatric drug dose using Clark's Rule.
    Formula: Pediatric Dose = (Weight (lb) ÷ 150) × Adult Dose
    """
    return (weight / 150) * adultDose


@register_calc("Creatinine Clearance (Cockcroft-Gault Equation)")
def creatinine_clearance(age: float, weight: float, serumCreatinine: float, sex: str) -> float:
    """
    Estimates creatinine clearance for medication dosing in patients with renal impairment.
    Formula: CrCl (mL/min) = [(140 - Age) × Weight (kg) × (0.85 if female)] / (72 × Serum Creatinine (mg/dL))
    sex: 'male' or 'female'
    """
    factor = 0.85 if sex.lower() == "female" else 1
    return ((140 - age) * weight * factor) / (72 * serumCreatinine)


@register_calc("Heparin Infusion Rate")
def heparin_infusion_rate(unitsPerHour: float, concentration: float) -> float:
    """
    Calculates the required heparin infusion rate.
    Formula: Rate (mL/hr) = (Units/hr ordered ÷ Concentration (units/mL))
    """
    return unitsPerHour / concentration


@register_calc("Fluid Maintenance for Pediatrics (4-2-1 Rule)")
def fluid_maintenance_pediatrics(weight: float) -> float:
    """
    Calculates the fluid maintenance requirement for pediatric patients.
    Formula: Total Fluid (mL/hr) = 4mL/kg for first 10kg + 2mL/kg for next 10kg + 1mL/kg for remaining weight
    """
    if weight <= 10:
        return weight * 4
    elif weight <= 20:
        return 40 + (weight - 10) * 2
    else:
        return 60 + (weight - 20) * 1


@register_calc("APGAR Score")
def apgar_score(appearance: int, pulse: int, grimace: int, activity: int, respiration: int) -> int:
    """
    Calculates newborn health status based on appearance, pulse, grimace, activity, and respiration.
    Formula: APGAR Score = Sum of 5 criteria scored 0-2 each
    """
    return appearance + pulse + grimace + activity + respiration


@register_calc("Oxygen Flow Rate")
def oxygen_flow_rate(fiO2: float, minuteVentilation: float) -> float:
    """
    Calculates the required oxygen flow rate based on desired FiO2.
    Formula: Flow Rate (L/min) = (FiO2 - 0.21) / 0.79 × Minute Ventilation
    """
    pure_O2_fraction = (fiO2 - 0.21) / 0.79
    return pure_O2_fraction * minuteVentilation


@register_calc("Anion Gap")
def anion_gap(sodium: float, potassium: float, chloride: float, bicarbonate: float) -> float:
    """
    Calculates the anion gap to assess acid-base balance.
    Formula: Anion Gap = (Na+ + K+) - (Cl- + HCO3-)
    """
    return (sodium + potassium) - (chloride + bicarbonate)

## End of Medical dosage and Administration calculations ##


## Patient Monitoring calculations ##
def _score_respiratory_rate(rr: float) -> int:
    if rr <= 8:
        return 3
    elif rr <= 11:
        return 1
    elif rr <= 20:
        return 0
    elif rr <= 24:
        return 2
    else:
        return 3

def _score_oxygen_saturation(spo2: float) -> int:
    if spo2 <= 91:
        return 3
    elif spo2 <= 93:
        return 2
    elif spo2 <= 95:
        return 1
    else:
        return 0

def _score_temperature(temp: float) -> int:
    if temp <= 35.0:
        return 3
    elif temp <= 36.0:
        return 1
    elif temp <= 38.0:
        return 0
    elif temp <= 39.0:
        return 1
    else:
        return 2

def _score_systolic_bp(sbp: float) -> int:
    if sbp <= 90:
        return 3
    elif sbp <= 100:
        return 2
    elif sbp <= 110:
        return 1
    elif sbp <= 219:
        return 0
    else:
        return 3

def _score_heart_rate(hr: float) -> int:
    if hr <= 40:
        return 3
    elif hr <= 50:
        return 1
    elif hr <= 90:
        return 0
    elif hr <= 110:
        return 1
    elif hr <= 130:
        return 2
    else:
        return 3

@register_calc("Early Warning Score (EWS)")
def early_warning_score(
    respiratoryRate: float,
    oxygenSaturation: float,
    temperature: float,
    systolicBP: float,
    heartRate: float
) -> int:
    """
    Calculates an early warning score based on vital signs to identify patient deterioration.
    Formula: EWS = Sum of scores for respiratory rate, oxygen saturation, temperature,
             systolic blood pressure, and heart rate
    """
    rr_score = _score_respiratory_rate(respiratoryRate)
    spo2_score = _score_oxygen_saturation(oxygenSaturation)
    temp_score = _score_temperature(temperature)
    sbp_score = _score_systolic_bp(systolicBP)
    hr_score = _score_heart_rate(heartRate)

    return rr_score + spo2_score + temp_score + sbp_score + hr_score



@register_calc("Respiratory Rate to Tidal Volume Ratio")
def respiratory_rate_to_tidal_volume_ratio(respiratoryRate: float, tidalVolume: float) -> float:
    """
    Calculates the ratio of respiratory rate to tidal volume for assessing respiratory efficiency.
    Formula: RR/TV Ratio = Respiratory Rate / Tidal Volume
    """
    return respiratoryRate / tidalVolume


@register_calc("Shock Index")
def shock_index(heartRate: float, systolicBP: float) -> float:
    """
    Calculates the shock index to assess hemodynamic stability.
    Formula: Shock Index = Heart Rate / Systolic Blood Pressure
    """
    return heartRate / systolicBP


@register_calc("Glasgow Coma Scale (GCS)")
def glasgow_coma_scale(eyeResponse: int, verbalResponse: int, motorResponse: int) -> int:
    """
    Calculates the Glasgow Coma Scale score to assess consciousness level.
    Formula: GCS = Eye Response + Verbal Response + Motor Response
    """
    return eyeResponse + verbalResponse + motorResponse


@register_calc("Pulse Pressure")
def pulse_pressure(systolicBP: float, diastolicBP: float) -> float:
    """
    Calculates the pulse pressure to assess cardiovascular health.
    Formula: Pulse Pressure = Systolic Blood Pressure - Diastolic Blood Pressure
    """
    return systolicBP - diastolicBP


@register_calc("Mean Arterial Pressure (MAP)")
def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """
    Calculates mean arterial pressure to assess perfusion.
    Formula: MAP = [(2 × Diastolic) + Systolic] / 3
    """
    return ((2 * diastolic) + systolic) / 3


@register_calc("Oxygenation Index (OI)")
def oxygenation_index(fiO2: float, meanAirwayPressure: float, paO2: float) -> float:
    """
    Calculates the oxygenation index to assess the severity of hypoxemia.
    Formula: OI = (FiO2 × Mean Airway Pressure × 100) / PaO2
    """
    return (fiO2 * meanAirwayPressure * 100) / paO2

## End of Patient Monitoring calculations ##


## Nutrition and Fluid Management ##


@register_calc("Caloric Requirements (Harris-Benedict Equation)")
def caloric_requirements_harris_benedict_full(weight: float, height: float, age: int, sex: str, activityFactor: float) -> float:
    """
    Calculates daily caloric needs using the Harris-Benedict equation and activity level.
    Formula:
      For males:   BMR = 88.362 + (13.397 × Weight) + (4.799 × Height) - (5.677 × Age)
      For females: BMR = 447.593 + (9.247 × Weight) + (3.098 × Height) - (4.330 × Age)
      Calories = BMR × Activity Factor
    sex: 'male' or 'female'
    """
    if sex.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr * activityFactor

@register_calc("Caloric Requirements (Mifflin-St Jeor Equation)")
def caloric_requirements_mifflin_st_jeor(weight: float, height: float, age: int, sex: str, activityFactor: float) -> float:
    """
    Calculates daily caloric needs using the Mifflin-St Jeor equation and activity level.
    Formula:
      For males:   BMR = (10 × Weight) + (6.25 × Height) - (5 × Age) + 5
      For females: BMR = (10 × Weight) + (6.25 × Height) - (5 × Age) - 161
      Calories = BMR × Activity Factor
    sex: 'male' or 'female'
    """
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if sex.lower() == "male" else -161)
    return bmr * activityFactor


@register_calc("Fluid Requirement by Body Weight")
def fluid_requirement_by_body_weight(weight: float) -> float:
    """
    Calculates daily fluid requirement based on body weight.
    Formula: Fluid (mL/day) = Weight (kg) × 30 mL
    """
    return weight * 30


@register_calc("Enteral Nutrition Formula")
def enteral_nutrition_formula(caloricNeeds: float, formulaCaloricDensity: float) -> float:
    """
    Calculates the required volume of enteral nutrition formula to meet caloric needs.
    Formula: Volume (mL) = Caloric Needs (kcal) / Formula Caloric Density (kcal/mL)
    """
    return caloricNeeds / formulaCaloricDensity


@register_calc("Parenteral Nutrition Macronutrient Distribution")
def parenteral_nutrition_macronutrient_distribution(totalCalories: float, macronutrientPercentage: float) -> float:
    """
    Calculates the distribution of macronutrients in parenteral nutrition.
    Formula: Macronutrient Distribution = Total Calories × Macronutrient Percentage
    """
    return totalCalories * macronutrientPercentage


@register_calc("Electrolyte Requirements")
def electrolyte_requirements(weight: float, requirementFactor: float) -> float:
    """
    Calculates daily electrolyte requirements based on weight.
    Formula: Electrolyte (mEq/day) = Weight (kg) × Requirement Factor
    """
    return weight * requirementFactor


@register_calc("Body Mass Index (BMI)")
def body_mass_index(weight: float, height: float) -> float:
    """
    Calculates BMI to assess body weight relative to height.
    Formula: BMI = Weight (kg) / (Height (m)²)
    """
    return weight / (height ** 2)



@register_calc("Tube Feeding Rate")
def tube_feeding_rate(totalVolume: float, feedingDuration: float) -> float:
    """
    Calculates the required rate for enteral feeding.
    Formula: Rate (mL/hr) = Total Volume (mL) / Feeding Duration (hr)
    """
    return totalVolume / feedingDuration


@register_calc("Fluid Replacement")
def fluid_replacement(deficit: float, maintenance: float) -> float:
    """
    Calculates the fluid replacement requirement based on deficit and maintenance needs.
    Formula: Total Fluid (mL) = Deficit (mL) + Maintenance (mL)
    """
    return deficit + maintenance


@register_calc("Protein Requirement")
def protein_requirement(weight: float, proteinFactor: float) -> float:
    """
    Calculates daily protein needs based on body weight.
    Formula: Protein (g/day) = Weight (kg) × Protein Factor (g/kg)
    """
    return weight * proteinFactor


@register_calc("Daily Water Requirement")
def daily_water_requirement(weight: float) -> float:
    """
    Calculates the daily water requirement based on body weight.
    Formula: Water (mL/day) = Weight (kg) × 40 mL
    """
    return weight * 40

## End of Nutrition and Fluid Management ##


## Pharmacokinetics ##
@register_calc("Half-Life")
def half_life(volumeOfDistribution: float, clearance: float) -> float:
    """
    Calculates the time required for the drug concentration to reduce by half.
    Formula: Half-Life (t½) = (0.693 × Volume of Distribution) / Clearance
    """
    return (0.693 * volumeOfDistribution) / clearance


@register_calc("Clearance")
def clearance(dose: float, bioavailability: float, auc: float) -> float:
    """
    Calculates the clearance rate of a drug from the body.
    Formula: Clearance (L/time) = (Dose × Bioavailability) / Area Under the Curve (AUC)
    """
    return (dose * bioavailability) / auc


@register_calc("Volume of Distribution")
def volume_of_distribution(dose: float, plasmaConcentration: float) -> float:
    """
    Calculates the apparent volume in which the drug is distributed.
    Formula: Volume of Distribution (L) = Dose / Plasma Concentration
    """
    return dose / plasmaConcentration


@register_calc("Loading Dose")
def loading_dose(targetConcentration: float, volumeOfDistribution: float, bioavailability: float) -> float:
    """
    Calculates the initial dose required to achieve the desired plasma concentration.
    Formula: Loading Dose (mg) = Target Concentration × Volume of Distribution / Bioavailability
    """
    return (targetConcentration * volumeOfDistribution) / bioavailability


@register_calc("Maintenance Dose")
def maintenance_dose(clearance: float, targetConcentration: float, bioavailability: float) -> float:
    """
    Calculates the dose required to maintain a steady-state concentration.
    Formula: Maintenance Dose (mg/time) = Clearance × Target Concentration / Bioavailability
    """
    return (clearance * targetConcentration) / bioavailability


@register_calc("Steady-State Concentration")
def steady_state_concentration(doseRate: float, bioavailability: float, clearance: float) -> float:
    """
    Calculates the steady-state concentration of a drug during continuous dosing.
    Formula: Steady-State Concentration (mg/L) = (Dose Rate × Bioavailability) / Clearance
    """
    return (doseRate * bioavailability) / clearance


@register_calc("Elimination Rate Constant")
def elimination_rate_constant(clearance: float, volumeOfDistribution: float) -> float:
    """
    Calculates the rate constant for drug elimination.
    Formula: Elimination Rate Constant (k) = Clearance / Volume of Distribution
    """
    return clearance / volumeOfDistribution


@register_calc("Area Under the Curve (AUC)")
def area_under_curve(dose: float, bioavailability: float, clearance: float) -> float:
    """
    Calculates the total drug exposure over time.
    Formula: AUC (mg·time/L) = Dose × Bioavailability / Clearance
    """
    return (dose * bioavailability) / clearance


@register_calc("Time to Reach Steady State")
def time_to_steady_state(halfLife: float) -> float:
    """
    Calculates the time required to reach steady-state concentration during continuous dosing.
    Formula: Time to Steady State = 5 × Half-Life
    """
    return 5 * halfLife


@register_calc("Accumulation Factor")
def accumulation_factor(k: float, tau: float) -> float:
    """
    Calculates the accumulation factor for a drug given its dosing interval and half-life.
    Formula: Accumulation Factor = 1 / (1 - e^(-k × τ))
    """
    return 1 / (1 - math.exp(-k * tau))


@register_calc("Peak Plasma Concentration (Cmax)")
def peak_plasma_concentration(dose: float, bioavailability: float, volumeOfDistribution: float) -> float:
    """
    Calculates the peak plasma concentration after a single dose.
    Formula: Cmax = (Dose × Bioavailability) / (Volume of Distribution)
    """
    return (dose * bioavailability) / volumeOfDistribution


@register_calc("Trough Plasma Concentration (Cmin)")
def trough_plasma_concentration(cmax: float, k: float, tau: float) -> float:
    """
    Calculates the trough plasma concentration before the next dose.
    Formula: Cmin = Cmax × e^(-k × τ)
    """
    return cmax * math.exp(-k * tau)


@register_calc("Therapeutic Index")
def therapeutic_index(td50: float, ed50: float) -> float:
    """
    Calculates the therapeutic index of a drug to assess its safety margin.
    Formula: Therapeutic Index = TD50 / ED50
    """
    return td50 / ed50


@register_calc("Loading Dose Adjustment")
def loading_dose_adjustment(targetConcentration: float, adjustedVolumeOfDistribution: float) -> float:
    """
    Calculates the adjusted loading dose for a patient with altered pharmacokinetics.
    Formula: Adjusted Loading Dose = Target Concentration × Adjusted Volume of Distribution
    """
    return targetConcentration * adjustedVolumeOfDistribution

## End of Pharmacokinetics ##



## Blood and Lab Values ##
@register_calc("Hemoglobin to Hematocrit Conversion")
def hemoglobin_to_hematocrit(hemoglobin: float) -> float:
    """
    Converts hemoglobin level to hematocrit.
    Formula: Hematocrit (%) = Hemoglobin × 3
    """
    return hemoglobin * 3


@register_calc("Red Cell Distribution Width (RDW)")
def red_cell_distribution_width(stdDevRBCVolume: float, meanCorpuscularVolume: float) -> float:
    """
    Calculates the variation in red blood cell size.
    Formula: RDW (%) = (Standard Deviation of RBC Volume / Mean Corpuscular Volume) × 100
    """
    return (stdDevRBCVolume / meanCorpuscularVolume) * 100


@register_calc("Reticulocyte Production Index (RPI)")
def reticulocyte_production_index(reticulocyteCount: float, hematocrit: float, normalHematocrit: float, maturationFactor: float) -> float:
    """
    Adjusts the reticulocyte count for anemia severity.
    Formula: RPI = (Reticulocyte Count × Hematocrit) / (Normal Hematocrit × Maturation Factor)
    """
    return (reticulocyteCount * hematocrit) / (normalHematocrit * maturationFactor)


@register_calc("Mean Platelet Volume (MPV)")
def mean_platelet_volume(plateletVolume: float, plateletCount: float) -> float:
    """
    Calculates the average size of platelets in the blood.
    Formula: MPV (fL) = Platelet Volume / Platelet Count
    """
    return plateletVolume / plateletCount


@register_calc("Neutrophil-to-Lymphocyte Ratio (NLR)")
def neutrophil_to_lymphocyte_ratio(neutrophilCount: float, lymphocyteCount: float) -> float:
    """
    Calculates the ratio of neutrophils to lymphocytes as an inflammatory marker.
    Formula: NLR = Neutrophil Count / Lymphocyte Count
    """
    return neutrophilCount / lymphocyteCount


@register_calc("Corrected Reticulocyte Count")
def corrected_reticulocyte_count(reticulocyteCount: float, patientsHematocrit: float, normalHematocrit: float) -> float:
    """
    Adjusts the reticulocyte count for anemia.
    Formula: Corrected Reticulocyte Count (%) = Reticulocyte Count × (Patient's Hematocrit / Normal Hematocrit)
    """
    return reticulocyteCount * (patientsHematocrit / normalHematocrit)


@register_calc("Corrected Calcium")
def corrected_calcium(measuredCalcium: float, albumin: float) -> float:
    """
    Adjusts calcium level based on albumin concentration.
    Formula: Corrected Calcium (mg/dL) = Measured Calcium + 0.8 × (4 - Albumin)
    """
    return measuredCalcium + 0.8 * (4 - albumin)


@register_calc("Anion Gap")
def anion_gap(sodium: float, potassium: float, chloride: float, bicarbonate: float) -> float:
    """
    Calculates the anion gap to assess acid-base balance.
    Formula: Anion Gap = (Na+ + K+) - (Cl- + HCO3-)
    """
    return (sodium + potassium) - (chloride + bicarbonate)


@register_calc("eGFR (Estimated Glomerular Filtration Rate)")
def egfr(serumCreatinine: float, age: float, sex: str, race: str) -> float:
    """
    Estimates kidney function based on serum creatinine, age, sex, and race.
    Formula: eGFR (mL/min/1.73m²) = 186 × (Serum Creatinine)^-1.154 × (Age)^-0.203 × (0.742 if female) × (1.212 if Black)
    sex: 'male' or 'female'
    race: 'black' or 'non-black'
    """
    sexFactor = 0.742 if sex.lower() == "female" else 1.0
    raceFactor = 1.212 if race.lower() == "black" else 1.0
    return 186 * (serumCreatinine ** -1.154) * (age ** -0.203) * sexFactor * raceFactor


@register_calc("Mean Corpuscular Volume (MCV)")
def mean_corpuscular_volume(hematocrit: float, rbcCount: float) -> float:
    """
    Calculates the average volume of red blood cells.
    Formula: MCV (fL) = (Hematocrit × 10) / RBC Count
    """
    return (hematocrit * 10) / rbcCount


@register_calc("Transferrin Saturation")
def transferrin_saturation(serumIron: float, tibc: float) -> float:
    """
    Calculates transferrin saturation to assess iron status.
    Formula: Transferrin Saturation (%) = (Serum Iron / Total Iron Binding Capacity) × 100
    """
    return (serumIron / tibc) * 100

## End of Blood and Lab Values ##


## Cardiovascular Health ##
@register_calc("Cardiac Output")
def cardiac_output(strokeVolume: float, heartRate: float) -> float:
    """
    Calculates the amount of blood the heart pumps per minute.
    Formula: Cardiac Output (L/min) = Stroke Volume × Heart Rate / 1000
    """
    return (strokeVolume * heartRate) / 1000


@register_calc("Stroke Volume")
def stroke_volume(endDiastolicVolume: float, endSystolicVolume: float) -> float:
    """
    Calculates the amount of blood pumped out of the ventricle with each heartbeat.
    Formula: Stroke Volume = End Diastolic Volume - End Systolic Volume
    """
    return endDiastolicVolume - endSystolicVolume


@register_calc("Mean Arterial Pressure (MAP)")
def mean_arterial_pressure(systolic: float, diastolic: float) -> float:
    """
    Calculates the average arterial pressure during a single cardiac cycle.
    Formula: MAP = [(2 × Diastolic BP) + Systolic BP] / 3
    """
    return ((2 * diastolic) + systolic) / 3


@register_calc("Systemic Vascular Resistance (SVR)")
def systemic_vascular_resistance(map: float, cvp: float, cardiacOutput: float) -> float:
    """
    Calculates systemic vascular resistance, an indicator of vessel constriction.
    Formula: SVR = [(MAP - CVP) × 80] / Cardiac Output
    """
    return ((map - cvp) * 80) / cardiacOutput


@register_calc("Pulse Pressure")
def pulse_pressure(systolicBP: float, diastolicBP: float) -> float:
    """
    Calculates the difference between systolic and diastolic pressure.
    Formula: Pulse Pressure = Systolic BP - Diastolic BP
    """
    return systolicBP - diastolicBP


@register_calc("Ejection Fraction")
def ejection_fraction(strokeVolume: float, endDiastolicVolume: float) -> float:
    """
    Calculates the percentage of blood leaving the heart each time it contracts.
    Formula: Ejection Fraction (%) = (Stroke Volume / End Diastolic Volume) × 100
    """
    return (strokeVolume / endDiastolicVolume) * 100


@register_calc("Cardiac Index")
def cardiac_index(cardiacOutput: float, bodySurfaceArea: float) -> float:
    """
    Adjusts the cardiac output to a person's body surface area.
    Formula: Cardiac Index = Cardiac Output / Body Surface Area
    """
    return cardiacOutput / bodySurfaceArea


@register_calc("Left Ventricular Stroke Work Index (LVSWI)")
def left_ventricular_stroke_work_index(map: float, pcwp: float, strokeVolumeIndex: float) -> float:
    """
    Measures the amount of work the left ventricle does per beat per body surface area.
    Formula: LVSWI = (MAP - PCWP) × Stroke Volume Index × 0.0136
    """
    return (map - pcwp) * strokeVolumeIndex * 0.0136


@register_calc("Rate Pressure Product (RPP)")
def rate_pressure_product(heartRate: float, systolicBP: float) -> float:
    """
    Estimates myocardial oxygen consumption.
    Formula: RPP = Heart Rate × Systolic Blood Pressure
    """
    return heartRate * systolicBP


@register_calc("Fractional Shortening")
def fractional_shortening(lvedd: float, lvesd: float) -> float:
    """
    Calculates the percentage change in the diameter of the left ventricle during contraction.
    Formula: FS (%) = (LVEDD - LVESD) / LVEDD × 100
    """
    return ((lvedd - lvesd) / lvedd) * 100


@register_calc("QTc Interval")
def qtc_interval(qtInterval: float, rrInterval: float) -> float:
    """
    Corrects the QT interval for heart rate.
    Formula: QTc = QT Interval / √RR Interval
    """
    return qtInterval / math.sqrt(rrInterval)

## End of Cardiovascular Health ##



## Body Mechanism and Growth ##


@register_calc("Bone Mineral Density (BMD)")
def bone_mineral_density(boneMass: float, boneArea: float) -> float:
    """
    Calculates bone mineral density to assess bone health.
    Formula: BMD (g/cm²) = Bone Mass / Bone Area
    """
    return boneMass / boneArea

@register_calc("Waist-to-Hip Ratio")
def waist_to_hip_ratio(waistCircumference: float, hipCircumference: float) -> float:
    """
    Calculates the waist-to-hip ratio to assess body fat distribution.
    Formula: Waist-to-Hip Ratio = Waist Circumference / Hip Circumference
    """
    return waistCircumference / hipCircumference

@register_calc("Growth Hormone Dosage")
def growth_hormone_dosage(weight: float, bsa: float, dosageFactor: float) -> float:
    """
    Calculates the dosage of growth hormone based on weight or body surface area.
    Formula: Dosage (mg/day) = Weight × Dosage Factor or BSA × Dosage Factor
    """
    if bsa:
        return bsa * dosageFactor
    return weight * dosageFactor

@register_calc("Total Energy Expenditure (TEE)")
def total_energy_expenditure(bmr: float, activityFactor: float) -> float:
    """
    Calculates the total energy expenditure based on BMR and activity level.
    Formula: TEE (kcal/day) = BMR × Activity Factor
    """
    return bmr * activityFactor

@register_calc("Body Surface Area (BSA)")
def body_surface_area(height: float, weight: float) -> float:
    """
    Calculates the body surface area based on height and weight.
    Formula: BSA (m²) = √[(height (cm) × weight (kg)) / 3600]
    """
    return math.sqrt((height * weight) / 3600)

@register_calc("Lean Body Mass (LBM)")
def lean_body_mass(weight: float, bodyFatPercentage: float) -> float:
    """
    Calculates lean body mass based on weight and body fat percentage.
    Formula: LBM (kg) = Weight × (1 - Body Fat Percentage / 100)
    """
    return weight * (1 - bodyFatPercentage / 100)

@register_calc("Growth Velocity")
def growth_velocity(heightAtEnd: float, heightAtStart: float, timePeriod: float) -> float:
    """
    Calculates the growth velocity over a specific time period.
    Formula: Growth Velocity (cm/year) = (Height at End - Height at Start) / Time Period
    """
    return (heightAtEnd - heightAtStart) / timePeriod

@register_calc("Basal Metabolic Rate (BMR)")
def basal_metabolic_rate(weight: float, height: float, age: int, sex: str) -> float:
    """
    Calculates the basal metabolic rate to estimate energy expenditure at rest.
    Formula: BMR (kcal/day) = 10 × Weight (kg) + 6.25 × Height (cm) - 5 × Age (years) + (5 if male, -161 if female)
    sex: 'male' or 'female'
    """
    gender_factor = 5 if sex.lower() == "male" else -161
    return 10 * weight + 6.25 * height - 5 * age + gender_factor

@register_calc("Body Fat Percentage")
def body_fat_percentage(bmi: float, age: int, sex: str) -> float:
    """
    Estimates body fat percentage using BMI, age, and sex.
    Formula: Body Fat (%) = (1.20 × BMI) + (0.23 × Age) - (10.8 × Sex) - 5.4
    sex: 'male' or 'female'
    """
    sex_factor = 10.8 if sex.lower() == "male" else 0
    return (1.20 * bmi) + (0.23 * age) - sex_factor - 5.4

@register_calc("Resting Energy Expenditure (REE)")
def resting_energy_expenditure(weight: float, height: float, age: int, sex: str) -> float:
    """
    Calculates the resting energy expenditure to estimate daily caloric needs using the Mifflin-St Jeor equation.
    Formula: REE (kcal/day) = (10 × Weight (kg)) + (6.25 × Height (cm)) - (5 × Age (years)) + (5 if male, -161 if female)
    sex: 'male' or 'female'
    """
    gender_factor = 5 if sex.lower() == "male" else -161
    return (10 * weight) + (6.25 * height) - (5 * age) + gender_factor

## End of Body Mechanism and Growth ##



## Infection Control and Epidemiology ##
@register_calc("Basic Reproduction Number (R0)")
def basic_reproduction_number(contactRate: float, transmissionProbability: float, durationOfInfectiousness: float) -> float:
    """
    Estimates the average number of secondary infections caused by one infected individual in a fully susceptible population.
    Formula: R0 = Contact Rate × Transmission Probability × Duration of Infectiousness
    """
    return contactRate * transmissionProbability * durationOfInfectiousness

@register_calc("Effective Reproduction Number (Rt)")
def effective_reproduction_number(r0: float, susceptiblePopulation: int, totalPopulation: int) -> float:
    """
    Estimates the average number of secondary infections in a partially immune population.
    Formula: Rt = R0 × (Susceptible Population / Total Population)
    """
    return r0 * (susceptiblePopulation / totalPopulation)

@register_calc("Infection Fatality Rate (IFR)")
def infection_fatality_rate(numberOfDeaths: int, totalInfectedIndividuals: int) -> float:
    """
    Calculates the proportion of deaths among all infected individuals, including asymptomatic cases.
    Formula: IFR (%) = (Number of Deaths / Total Infected Individuals) × 100
    """
    return (numberOfDeaths / totalInfectedIndividuals) * 100

@register_calc("Serial Interval")
def serial_interval(secondaryCaseOnset: float, primaryCaseOnset: float) -> float:
    """
    Calculates the average time between successive cases in a chain of transmission.
    Formula: Serial Interval = Time of Symptom Onset in Secondary Case - Time of Symptom Onset in Primary Case
    """
    return secondaryCaseOnset - primaryCaseOnset

@register_calc("Quarantine Effectiveness")
def quarantine_effectiveness(transmissionWithQuarantine: int, transmissionWithoutQuarantine: int) -> float:
    """
    Estimates the reduction in transmission due to quarantine measures.
    Formula: Effectiveness (%) = (1 - (Transmission with Quarantine / Transmission without Quarantine)) × 100
    """
    return (1 - (transmissionWithQuarantine / transmissionWithoutQuarantine)) * 100

@register_calc("Case Fatality Rate (CFR)")
def case_fatality_rate(numberOfDeaths: int, numberOfConfirmedCases: int) -> float:
    """
    Calculates the proportion of deaths among confirmed cases of a disease.
    Formula: CFR (%) = (Number of Deaths / Number of Confirmed Cases) × 100
    """
    return (numberOfDeaths / numberOfConfirmedCases) * 100

@register_calc("Attack Rate")
def attack_rate(numberOfIllIndividuals: int, totalPopulationAtRisk: int) -> float:
    """
    Calculates the proportion of individuals who become ill after exposure to a disease.
    Formula: Attack Rate (%) = (Number of Ill Individuals / Total Population at Risk) × 100
    """
    return (numberOfIllIndividuals / totalPopulationAtRisk) * 100

@register_calc("Incidence Rate")
def incidence_rate(numberOfNewCases: int, populationAtRisk: int, time: float) -> float:
    """
    Calculates the rate of new cases of a disease in a population over a specific time period.
    Formula: Incidence Rate = Number of New Cases / (Population at Risk × Time)
    """
    return numberOfNewCases / (populationAtRisk * time)


@register_calc("Secondary Attack Rate")
def secondary_attack_rate(numberOfSecondaryCases: int, numberOfExposedContacts: int) -> float:
    """
    Calculates the proportion of secondary cases among contacts of primary cases.
    Formula: Secondary Attack Rate (%) = (Number of Secondary Cases / Number of Exposed Contacts) × 100
    """
    return (numberOfSecondaryCases / numberOfExposedContacts) * 100

@register_calc("Herd Immunity Threshold")
def herd_immunity_threshold(r0: float) -> float:
    """
    Calculates the proportion of the population that needs to be immune to stop disease transmission.
    Formula: Herd Immunity Threshold (%) = (1 - (1 / R0)) × 100
    """
    return (1 - (1 / r0)) * 100

@register_calc("Prevalence Rate")
def prevalence_rate(numberOfExistingCases: int, totalPopulation: int) -> float:
    """
    Calculates the proportion of individuals in a population who have a disease at a specific point in time.
    Formula: Prevalence Rate (%) = (Number of Existing Cases / Total Population) × 100
    """
    return (numberOfExistingCases / totalPopulation) * 100

@register_calc("Doubling Time")
def doubling_time(growthRate: float) -> float:
    """
    Calculates the time it takes for the number of cases to double.
    Formula: Doubling Time = ln(2) / Growth Rate
    """
    return math.log(2) / growthRate

## End of Infection Control and Epidemiology ##



## Electrolyte Replacement calculations ##
@register_calc("Sodium Deficit")
def sodium_deficit(desiredSodium: float, currentSodium: float, totalBodyWater: float) -> float:
    """
    Calculates the sodium deficit to correct hyponatremia.
    Formula: Sodium Deficit (mEq) = (Desired Sodium - Current Sodium) × Total Body Water
    """
    return (desiredSodium - currentSodium) * totalBodyWater

@register_calc("Chloride Replacement")
def chloride_replacement(desiredChloride: float, currentChloride: float, totalBodyWater: float) -> float:
    """
    Calculates the chloride replacement required to correct hypochloremia.
    Formula: Chloride Replacement (mEq) = (Desired Chloride - Current Chloride) × Total Body Water
    """
    return (desiredChloride - currentChloride) * totalBodyWater

@register_calc("Bicarbonate Replacement")
def bicarbonate_replacement(baseDeficit: float, totalBodyWater: float) -> float:
    """
    Calculates the bicarbonate replacement required to correct metabolic acidosis.
    Formula: Bicarbonate Replacement (mEq) = Base Deficit × Total Body Water
    """
    return baseDeficit * totalBodyWater

@register_calc("Phosphate Correction for Calcium")
def phosphate_correction_for_calcium(phosphateReplacement: float, correctionFactor: float) -> float:
    """
    Adjusts phosphate replacement based on calcium levels to avoid precipitation.
    Formula: Adjusted Phosphate (mmol) = Phosphate Replacement × Correction Factor
    """
    return phosphateReplacement * correctionFactor

@register_calc("Hyperkalemia Correction")
def hyperkalemia_correction(currentPotassium: float, targetPotassium: float) -> float:
    """
    Calculates the reduction in potassium levels required to correct hyperkalemia.
    Formula: Potassium Reduction (mEq/L) = Current Potassium - Target Potassium
    """
    return currentPotassium - targetPotassium

@register_calc("Potassium Replacement")
def potassium_replacement(desiredPotassium: float, currentPotassium: float, totalBodyPotassium: float) -> float:
    """
    Calculates the potassium replacement required to correct hypokalemia.
    Formula: Potassium Replacement (mEq) = (Desired Potassium - Current Potassium) × Total Body Potassium
    """
    return (desiredPotassium - currentPotassium) * totalBodyPotassium

@register_calc("Calcium Correction for Albumin")
def calcium_correction_for_albumin(measuredCalcium: float, albumin: float) -> float:
    """
    Adjusts calcium level based on albumin concentration.
    Formula: Corrected Calcium (mg/dL) = Measured Calcium + 0.8 × (4 - Albumin)
    """
    return measuredCalcium + 0.8 * (4 - albumin)

@register_calc("Magnesium Replacement")
def magnesium_replacement(desiredMagnesium: float, currentMagnesium: float, totalBodyMagnesium: float) -> float:
    """
    Calculates the magnesium replacement required to correct hypomagnesemia.
    Formula: Magnesium Replacement (mEq) = (Desired Magnesium - Current Magnesium) × Total Body Magnesium
    """
    return (desiredMagnesium - currentMagnesium) * totalBodyMagnesium

@register_calc("Phosphate Replacement")
def phosphate_replacement(desiredPhosphate: float, currentPhosphate: float, totalBodyPhosphate: float) -> float:
    """
    Calculates the phosphate replacement required to correct hypophosphatemia.
    Formula: Phosphate Replacement (mmol) = (Desired Phosphate - Current Phosphate) × Total Body Phosphate
    """
    return (desiredPhosphate - currentPhosphate) * totalBodyPhosphate

## End of Electrolyte Replacement calculations ##


## Others ##
@register_calc("Parkland Formula")
def parkland_formula(weight: float, tbsa: float) -> float:
    """
    Calculates fluid resuscitation requirements for burn patients.
    Formula: Total Fluid (mL) = 4 × Weight (kg) × TBSA (%)
    """
    return 4 * weight * tbsa

@register_calc("Oxygen Delivery")
def oxygen_delivery(cardiacOutput: float, hemoglobin: float, saO2: float, paO2: float) -> float:
    """
    Calculates oxygen delivery to tissues.
    Formula: Oxygen Delivery (mL/min) = Cardiac Output × (1.34 × Hemoglobin × SaO2 + (PaO2 × 0.003))
    """
    return cardiacOutput * (1.34 * hemoglobin * saO2 + (paO2 * 0.003))

@register_calc("Ideal Body Weight (IBW)")
def ideal_body_weight(height: float, sex: str) -> float:
    """
    Calculates the ideal body weight based on height and sex.
    Formula: IBW (kg) = 50 + 2.3 × (Height (in) - 60) for males, 45.5 + 2.3 × (Height (in) - 60) for females
    sex: 'male' or 'female'
    """
    base = 50 if sex.lower() == "male" else 45.5
    return base + 2.3 * (height - 60)

@register_calc("Adjusted Body Weight (ABW)")
def adjusted_body_weight(ibw: float, actualWeight: float) -> float:
    """
    Calculates adjusted body weight for obese patients.
    Formula: ABW (kg) = IBW + 0.4 × (Actual Weight - IBW)
    """
    return ibw + 0.4 * (actualWeight - ibw)

@register_calc("Corrected Sodium")
def corrected_sodium(measuredSodium: float, glucose: float) -> float:
    """
    Adjusts sodium level for hyperglycemia.
    Formula: Corrected Sodium (mEq/L) = Measured Sodium + 0.016 × (Glucose - 100)
    """
    return measuredSodium + 0.016 * (glucose - 100)

@register_calc("A-a Gradient")
def a_a_gradient(PAO2: float, PaO2: float) -> float:
    """
    Calculates the alveolar-arterial oxygen gradient.
    Formula: A-a Gradient = PAO2 - PaO2
    """
    return PAO2 - PaO2

@register_calc("Fractional Excretion of Sodium (FENa)")
def fractional_excretion_of_sodium(urineSodium: float, plasmaCreatinine: float, plasmaSodium: float, urineCreatinine: float) -> float:
    """
    Assesses kidney function and differentiates between prerenal and intrinsic renal failure.
    Formula: FENa (%) = [(Urine Sodium × Plasma Creatinine) / (Plasma Sodium × Urine Creatinine)] × 100
    """
    return (urineSodium * plasmaCreatinine) / (plasmaSodium * urineCreatinine) * 100

@register_calc("Serum Osmolality")
def serum_osmolality(sodium: float, glucose: float, bun: float) -> float:
    """
    Calculates serum osmolality to assess hydration status.
    Formula: Serum Osmolality (mOsm/kg) = 2 × Sodium + Glucose / 18 + BUN / 2.8
    """
    return 2 * sodium + glucose / 18 + bun / 2.8

@register_calc("Winter's Formula")
def winters_formula(hco3: float) -> float:
    """
    Predicts the expected PaCO2 in metabolic acidosis.
    Formula: Expected PaCO2 = (1.5 × HCO3-) + 8 ± 2
    """
    return 1.5 * hco3 + 8

@register_calc("Alveolar Partial Pressure of Oxygen (PAO2)")
def alveolar_partial_pressure_of_oxygen(fiO2: float, barometricPressure: float, waterVaporPressure: float, paCO2: float, respiratoryQuotient: float) -> float:
    """
    Calculates the alveolar partial pressure of oxygen (PAO2).
    Formula: PAO2 = FiO2 × (Barometric Pressure - Water Vapor Pressure) - (PaCO2 / Respiratory Quotient)
    """
    return fiO2 * (barometricPressure - waterVaporPressure) - (paCO2 / respiratoryQuotient)

## End of Others ##


## Statistical Calculations ##
@register_calc("Sensitivity")
def sensitivity(truePositives: int, falseNegatives: int) -> float:
    """
    Calculates the sensitivity of a diagnostic test.
    Formula: Sensitivity (%) = (True Positives / (True Positives + False Negatives)) × 100
    """
    return (truePositives / (truePositives + falseNegatives)) * 100

@register_calc("Specificity")
def specificity(trueNegatives: int, falsePositives: int) -> float:
    """
    Calculates the specificity of a diagnostic test.
    Formula: Specificity (%) = (True Negatives / (True Negatives + False Positives)) × 100
    """
    return (trueNegatives / (trueNegatives + falsePositives)) * 100

@register_calc("Positive Predictive Value (PPV)")
def positive_predictive_value(truePositives: int, falsePositives: int) -> float:
    """
    Calculates the positive predictive value of a diagnostic test.
    Formula: PPV (%) = (True Positives / (True Positives + False Positives)) × 100
    """
    return (truePositives / (truePositives + falsePositives)) * 100

@register_calc("Negative Predictive Value (NPV)")
def negative_predictive_value(trueNegatives: int, falseNegatives: int) -> float:
    """
    Calculates the negative predictive value of a diagnostic test.
    Formula: NPV (%) = (True Negatives / (True Negatives + False Negatives)) × 100
    """
    return (trueNegatives / (trueNegatives + falseNegatives)) * 100

@register_calc("Accuracy")
def accuracy(truePositives: int, trueNegatives: int, falsePositives: int, falseNegatives: int) -> float:
    """
    Calculates the accuracy of a diagnostic test.
    Formula: Accuracy (%) = ((True Positives + True Negatives) / Total Cases) × 100
    """
    totalCases = truePositives + trueNegatives + falsePositives + falseNegatives
    return ((truePositives + trueNegatives) / totalCases) * 100

@register_calc("Prevalence")
def prevalence(numberOfCases: int, totalPopulation: int) -> float:
    """
    Calculates the prevalence of a condition in a population.
    Formula: Prevalence (%) = (Number of Cases / Total Population) × 100
    """
    return (numberOfCases / totalPopulation) * 100

@register_calc("Positive Likelihood Ratio (LR+)")
def positive_likelihood_ratio(sensitivity: float, specificity: float) -> float:
    """
    Calculates the positive likelihood ratio of a diagnostic test.
    Formula: LR+ = Sensitivity / (1 - Specificity)
    """
    return sensitivity / (1 - specificity)

@register_calc("Negative Likelihood Ratio (LR-)")
def negative_likelihood_ratio(sensitivity: float, specificity: float) -> float:
    """
    Calculates the negative likelihood ratio of a diagnostic test.
    Formula: LR- = (1 - Sensitivity) / Specificity
    """
    return (1 - sensitivity) / specificity


@register_calc("Incidence Rate")
def incidence_rate(numberOfNewCases: int, populationAtRisk: int, time: float) -> float:
    """
    Calculates the rate of new cases of a disease in a population over a specific time period.
    Formula: Incidence Rate = Number of New Cases / (Population at Risk × Time)
    """
    return numberOfNewCases / (populationAtRisk * time)


@register_calc("Odds Ratio (OR)")
def odds_ratio(oddsExposureCases: float, oddsExposureControls: float) -> float:
    """
    Calculates the odds ratio to measure the association between exposure and outcome.
    Formula: OR = Odds of Exposure in Cases / Odds of Exposure in Controls
    """
    return oddsExposureCases / oddsExposureControls

@register_calc("Relative Risk (RR)")
def relative_risk(riskExposedGroup: float, riskUnexposedGroup: float) -> float:
    """
    Calculates the relative risk to compare the risk of an outcome between two groups.
    Formula: RR = Risk in Exposed Group / Risk in Unexposed Group
    """
    return riskExposedGroup / riskUnexposedGroup

@register_calc("Number Needed to Treat (NNT)")
def number_needed_to_treat(absoluteRiskReduction: float) -> float:
    """
    Calculates the number needed to treat to prevent one additional adverse outcome.
    Formula: NNT = 1 / Absolute Risk Reduction
    """
    return 1 / absoluteRiskReduction

## End of Statistical Calculations ##
