const CONVERSIONS = {
  // --- LENGTH ---
  length: {
    units: ['m', 'cm', 'mm', 'in', 'ft'],
    factors: {
      'm:cm': 100,
      'cm:m': 0.01,
      'm:mm': 1000,
      'mm:m': 0.001,
      'cm:mm': 10,
      'mm:cm': 0.1,
      'm:in': 39.3701,
      'in:m': 0.0254,
      'm:ft': 3.28084,
      'ft:m': 0.3048,
      'cm:in': 0.393701,
      'in:cm': 2.54,
      'ft:in': 12,
      'in:ft': 0.0833333,
      'ft:cm': 30.48,
      'cm:ft': 0.0328084,
      'ft:mm': 304.8,
      'mm:ft': 0.00328084,
    },
  },

  // --- WEIGHT / MASS ---
  weight: {
    units: ['kg', 'g', 'lb', 'oz'],
    factors: {
      'kg:g': 1000,
      'g:kg': 0.001,
      'kg:lb': 2.20462,
      'lb:kg': 0.453592,
      'kg:oz': 35.274,
      'oz:kg': 0.0283495,
      'g:lb': 0.00220462,
      'lb:g': 453.592,
      'g:oz': 0.035274,
      'oz:g': 28.3495,
      'lb:oz': 16,
      'oz:lb': 0.0625,
    },
  },

  // --- TEMPERATURE ---
  temperature: {
    units: ['C', 'F', 'K'],
    convert: function (value, from, to) {
      if (from === to) return value;
      if (from === 'C' && to === 'F') return (value * 9) / 5 + 32;
      if (from === 'F' && to === 'C') return ((value - 32) * 5) / 9;
      if (from === 'C' && to === 'K') return value + 273.15;
      if (from === 'K' && to === 'C') return value - 273.15;
      if (from === 'F' && to === 'K') return ((value - 32) * 5) / 9 + 273.15;
      if (from === 'K' && to === 'F') return ((value - 273.15) * 9) / 5 + 32;
      return value;
    },
  },

  // --- PRESSURE ---
  pressure: {
    units: ['mmHg', 'kPa', 'atm', 'cmH2O', 'Torr'],
    factors: {
      'mmHg:kPa': 0.133322,
      'kPa:mmHg': 7.50062,
      'mmHg:atm': 0.00131579,
      'atm:mmHg': 760,
      'mmHg:Torr': 1,
      'Torr:mmHg': 1,
      'cmH2O:mmHg': 0.73556,
      'mmHg:cmH2O': 1.35951,
      'kPa:atm': 0.00986923,
      'atm:kPa': 101.325,
      'kPa:cmH2O': 10.1972,
      'cmH2O:kPa': 0.0980665,
    },
  },

  // --- AREA ---
  area: {
    units: ['m2', 'cm2', 'ft2', 'in2', 'ha'],
    factors: {
      'm2:cm2': 10000,
      'cm2:m2': 0.0001,
      'm2:ft2': 10.7639,
      'ft2:m2': 0.092903,
      'm2:in2': 1550,
      'in2:m2': 0.00064516,
      'ft2:in2': 144,
      'in2:ft2': 0.00694444,
      'ha:m2': 10000,
      'm2:ha': 0.0001,
    },
  },

  // --- VOLUME / FLUID ---
  volume: {
    units: ['mL', 'L', 'oz', 'cup', 'tsp', 'Tbsp', 'fl_oz_US'],
    factors: {
      'mL:L': 0.001,
      'L:mL': 1000,
      'mL:oz': 0.033814,
      'oz:mL': 29.5735,
      'mL:fl_oz_US': 0.033814,
      'fl_oz_US:mL': 29.5735,
      'L:oz': 33.814,
      'oz:L': 0.0295735,
      'mL:cup': 0.00422675,
      'cup:mL': 236.588,
      'mL:tsp': 0.202884,
      'tsp:mL': 4.92892,
      'mL:Tbsp': 0.067628,
      'Tbsp:mL': 14.7868,
      'cup:oz': 8,
      'oz:cup': 0.125,
      'cup:tsp': 48,
      'tsp:cup': 0.0208333,
      'cup:Tbsp': 16,
      'Tbsp:cup': 0.0625,
      'tsp:Tbsp': 0.333333,
      'Tbsp:tsp': 3,
    },
  },

  // --- ENERGY / NUTRITION ---
  energy: {
    units: ['kcal', 'kJ', 'g_protein', 'g_carb', 'g_fat'],
    factors: {
      'kcal:kJ': 4.184,
      'kJ:kcal': 0.239006,

      'g_protein:kcal': 4,
      'kcal:g_protein': 0.25,
      'g_carb:kcal': 4,
      'kcal:g_carb': 0.25,
      'g_fat:kcal': 9,
      'kcal:g_fat': 0.111111,

      'g_fat:g_protein': function (v) {
        return (v * 9) / 4;
      },
      'g_protein:g_fat': function (v) {
        return (v * 4) / 9;
      },
      'g_carb:g_protein': function (v) {
        return (v * 4) / 4;
      },
      'g_protein:g_carb': function (v) {
        return (v * 4) / 4;
      },
    },
    convert: function (value, from, to) {
      const key = `${from}:${to}`;
      const f = this.factors[key];
      if (typeof f === 'number') return value * f;
      if (typeof f === 'function') return f(value);

      return value;
    },
  },

  // --- INFUSION RATES / DOSAGES (MASS & VOLUME) ---
  infusion: {
    units: ['g', 'mg', 'µg', 'IU', 'mL'],
    factors: {
      // Mass conversions
      'g:mg': 1000,
      'mg:g': 0.001,
      'mg:µg': 1000,
      'µg:mg': 0.001,
      'g:µg': 1e6,
      'µg:g': 1e-6,
      'mg:mL': 1,
      'mL:mg': 1,
      'g:mL': 1000,
      'mL:g': 0.001,
    },
    iuFactors: {
      insulin: 0.0347,
      heparin: 0.002,
      vitaminD: 0.000025,
      vitaminA: 0.0003,
      vitaminE: 0.67,
      erythropoietin: 0.0000084,
    },

    convert: function (
      value,
      from,
      to,
      concentrationMgPerMl = null,
      analyte = null
    ) {
      const key = `${from}:${to}`;
      if (this.factors[key]) {
        return value * this.factors[key];
      }

      console.log('IU DEBUG', {
        value,
        from,
        to,
        analyte,
        iuFactor: this.iuFactors[analyte],
      });

      if (
        (from === 'IU' || to === 'IU') &&
        analyte &&
        this.iuFactors[analyte]
      ) {
        const iuFactor = this.iuFactors[analyte];
        if (from === 'IU' && to === 'mg') return value * iuFactor;
        if (from === 'mg' && to === 'IU') return value / iuFactor;
        if (from === 'IU' && to === 'µg') return value * iuFactor * 1000;
        if (from === 'µg' && to === 'IU') return value / (iuFactor * 1000);
      }

      if (from === 'mg' && to === 'mL' && concentrationMgPerMl) {
        return value / concentrationMgPerMl;
      }
      if (from === 'mL' && to === 'mg' && concentrationMgPerMl) {
        return value * concentrationMgPerMl;
      }

      return value;
    },
  },

  // --- CONCENTRATION / LAB UNITS ---
  concentration: {
    units: ['mg/dL', 'mmol/L', 'µmol/L', 'µg/L'],
    convert: function (value, from, to, analyte) {
      const molarMasses = {
        glucose: 180.16,
        cholesterol: 386.65,
        triglycerides: 886.0,
        bun: 28.0,
        creatinine: 113.12,
        uric_acid: 168.11,
        calcium: 40.08,
      };

      if (from === to || !analyte || !molarMasses[analyte]) return value;
      const mm = molarMasses[analyte];

      if (from === 'mg/dL' && to === 'mmol/L') {
        return value / (mm * 10);
      }
      if (from === 'mmol/L' && to === 'mg/dL') {
        return value * mm * 10;
      }

      if (from === 'mg/dL' && to === 'µmol/L') {
        return (value * 10000) / mm;
      }
      if (from === 'µmol/L' && to === 'mg/dL') {
        return (value * mm) / 10000;
      }

      if (from === 'µmol/L' && to === 'mmol/L') {
        return value / 1000;
      }
      if (from === 'mmol/L' && to === 'µmol/L') {
        return value * 1000;
      }
      return value;
    },
  },
};
