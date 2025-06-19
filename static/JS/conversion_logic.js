function populateUnits(select, units) {
  select.innerHTML = '';
  units.forEach((u) => {
    const opt = document.createElement('option');
    opt.value = u;
    opt.textContent = u;
    select.appendChild(opt);
  });
}

function convertValue(category, value, from, to, extra = {}) {
  if (!CONVERSIONS[category]) return value;

  if (typeof CONVERSIONS[category].convert === 'function') {
    if (category === 'concentration') {
      return CONVERSIONS[category].convert(
        Number(value),
        from,
        to,
        extra.analyte
      );
    }

    if (category === 'infusion') {
      return CONVERSIONS[category].convert(
        Number(value),
        from,
        to,
        extra.concentrationMgPerMl,
        extra.analyte
      );
    }

    return CONVERSIONS[category].convert(Number(value), from, to);
  }

  if (from === to) return value;
  const key = `${from}:${to}`;
  const factor = CONVERSIONS[category].factors[key];
  return factor ? Number(value) * factor : value;
}

function setupConversionCard(card) {
  const category = card.dataset.category;
  const units = CONVERSIONS[category].units;
  const inputFrom = card.querySelector('.conv-input.from');
  const inputTo = card.querySelector('.conv-input.to');
  const selectFrom = card.querySelector('.conv-unit.from');
  const selectTo = card.querySelector('.conv-unit.to');
  const swapBtn = card.querySelector('.swap-btn');
  const warning = card.querySelector('.conversion-warning');

  populateUnits(selectFrom, units);
  populateUnits(selectTo, units);
  selectTo.selectedIndex = 1;

  let extra = {};
  if (category === 'concentration') {
    let analyteSelect = card.querySelector('.conv-analyte');
    if (!analyteSelect) {
      analyteSelect = document.createElement('select');
      analyteSelect.className = 'conv-analyte';
      Object.keys(
        CONVERSIONS.concentration.convert(0, '', '', '')
          ? CONVERSIONS.concentration.convert(0, '', '', '')
          : {}
      ).forEach((analyte) => {
        const opt = document.createElement('option');
        opt.value = analyte;
        opt.textContent = analyte;
        analyteSelect.appendChild(opt);
      });
      card.querySelector('.conversion-row').appendChild(analyteSelect);
    }
    analyteSelect.addEventListener('change', () => {
      extra.analyte = analyteSelect.value;
      updateConversion();
    });
    extra.analyte = analyteSelect.value;
  }

  let concentrationInput = null;
  if (category === 'infusion') {
    concentrationInput = card.querySelector('.conv-concentration');
    if (concentrationInput) {
      concentrationInput.addEventListener('input', updateConversion);
    }
  }
  let analyteSelect = null;
  if (category === 'infusion') {
    analyteSelect = card.querySelector('.conv-analyte');
    if (analyteSelect) {
      analyteSelect.addEventListener('change', updateConversion);
    }
    concentrationInput = card.querySelector('.conv-concentration');
    if (concentrationInput) {
      concentrationInput.addEventListener('input', updateConversion);
    }
  }
  function updateConversion(e) {
    if (e && e.target === inputTo) return;
    const value = inputFrom.value;
    const from = selectFrom.value;
    const to = selectTo.value;
    if (category === 'infusion') {
      extra.concentrationMgPerMl = concentrationInput
        ? parseFloat(concentrationInput.value) || null
        : null;
      extra.analyte = analyteSelect ? analyteSelect.value : null;

      const from = selectFrom.value;
      const to = selectTo.value;
      if (
        (from === 'IU' || to === 'IU') &&
        !(['mg', 'µg'].includes(from) || ['mg', 'µg'].includes(to))
      ) {
        if (warning) warning.style.display = 'block';
        inputTo.value = '';
        return;
      } else {
        if (warning) warning.style.display = 'none';
      }
    }
    if (value === '' || isNaN(value)) {
      inputTo.value = '';
      return;
    }
    inputTo.value = convertValue(category, value, from, to, extra);
  }

  inputFrom.addEventListener('input', updateConversion);
  selectFrom.addEventListener('change', updateConversion);
  selectTo.addEventListener('change', updateConversion);

  swapBtn.addEventListener('click', function () {
    const temp = selectFrom.value;
    selectFrom.value = selectTo.value;
    selectTo.value = temp;

    inputFrom.value = inputTo.value;
    updateConversion();
  });

  updateConversion();
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.conversion-card').forEach(setupConversionCard);
});
