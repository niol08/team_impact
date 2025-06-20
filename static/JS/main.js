function saveRecentCalculation(
  calcName,
  categoryTitle,
  categorySlug,
  result,
  unit
) {
  let recent = JSON.parse(localStorage.getItem('recentCalculations') || '[]');
  recent = recent.filter(
    (item) => item.calcName !== calcName || item.categorySlug !== categorySlug
  );
  recent.unshift({
    calcName,
    categoryTitle,
    categorySlug,
    result,
    unit,
  });
  if (recent.length > 10) recent = recent.slice(0, 10);
  localStorage.setItem('recentCalculations', JSON.stringify(recent));
}

function formatResult(result) {
  let num = Number(result);
  if (isNaN(num)) return result;
  if (Number.isInteger(num)) return num;
  const decimalPart = result.toString().split('.')[1];
  if (decimalPart && decimalPart.length > 4) {
    return num.toFixed(4).replace(/\.?0+$/, '');
  }
  return result;
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.calc-form').forEach((form) => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const index = form.getAttribute('data-index');
      const resultDiv = document.getElementById('result-' + index);
      resultDiv.textContent = 'Calculating...';
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.result !== undefined) {
            let roundedResult = formatResult(data.result);
            let unit = data.unit
              ? `<span class="result-unit">${data.unit}</span>`
              : '';

            resultDiv.innerHTML = `
            <div class="d-flex align-items-center justify-content-center gap-3 flex-wrap">
              <span class="result-label">Result:</span>
              <span class="result-value" style="color:#1d4ed8; font-weight:600;">${roundedResult} ${unit}</span>
              <button class="btn explain-btn" 
                style="background:#1d4ed8; color:#fff; border:none; border-radius:20px; padding:0.375rem 1.25rem; font-weight:500; box-shadow:0 2px 8px rgba(30,41,59,0.08); transition:background 0.2s;"
                type="button">
                Explain
              </button>
            </div>
            <div class="explanation mt-3"></div>
          `;

            const parameters = {};
            form
              .querySelectorAll('input, select, textarea')
              .forEach((input) => {
                if (!input.name) return;
                if (input.type === 'radio') {
                  if (input.checked) {
                    parameters[input.name] = input.value;
                  }
                } else {
                  if (input.value !== '') {
                    parameters[input.name] = input.value;
                  }
                }
              });

            localStorage.setItem(
              'lastCalculationParams',
              JSON.stringify(parameters)
            );

            const explainBtn = resultDiv.querySelector('.explain-btn');
            const explanationDiv = resultDiv.querySelector('.explanation');
            explainBtn.addEventListener('click', function () {
              explainBtn.disabled = true;
              explainBtn.textContent = 'Explaining...';
              fetch('/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  calc_name: form.querySelector(
                    'input[name="calculation_name"]'
                  ).value,
                  result: roundedResult,
                  parameters: parameters,
                }),
              })
                .then((res) => res.json())
                .then((data) => {
                  let cleanText = data.explanation.replace(/\*/g, '').trim();
                  explanationDiv.innerHTML = `
                    <div>${cleanText}</div>
                    <button class="btn btn-outline-primary mt-3 ask-policy-btn">Ask Policy AI</button>
                  `;
                  explanationDiv.style.display = 'block';

                  const askBtn =
                    explanationDiv.querySelector('.ask-policy-btn');
                  askBtn.addEventListener('click', async function () {
                    try {
                      const resp = await fetch('/dashboard', { method: 'GET' });
                      if (resp.status === 200) {
                        window.location.href = '/policyai';
                      } else {
                        const modal = document.getElementById('authModal');
                        if (modal) {
                          let bsModal =
                            bootstrap.Modal.getOrCreateInstance(modal);
                          bsModal.show();
                        } else {
                          alert('Please sign in to use Policy AI.');
                        }
                      }
                    } catch (err) {
                      alert('Could not check session. Please try again.');
                    }
                  });

                  explainBtn.disabled = false;
                  explainBtn.textContent = 'Explain result';
                })
                .catch(() => {
                  explanationDiv.innerHTML =
                    'Sorry, could not get explanation.';
                  explanationDiv.style.display = 'block';
                  explainBtn.disabled = false;
                  explainBtn.textContent = 'Explain';
                });
            });

            const calcName = form.querySelector(
              'input[name="calculation_name"]'
            ).value;

            const categoryTitleElem = document.querySelector('.page-header h2');
            const categoryTitle = categoryTitleElem
              ? categoryTitleElem.textContent
              : '';
            const categorySlug = window.location.pathname.split('/').pop();
            const plainUnit = data.unit ? data.unit : '';
            saveRecentCalculation(
              calcName,
              categoryTitle,
              categorySlug,
              roundedResult,
              plainUnit
            );
          } else {
            resultDiv.textContent = 'Error: ' + (data.error || 'Unknown error');
          }
        })
        .catch(() => {
          resultDiv.textContent = 'An error occurred. Please try again.';
        });
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const recentLink = document.getElementById('recent-link');
  const recentTable = document.getElementById('recent-list-table');
  if (recentLink && recentTable) {
    recentLink.addEventListener('click', function () {
      const tbody = recentTable.querySelector('tbody');
      let recent = JSON.parse(
        localStorage.getItem('recentCalculations') || '[]'
      );
      tbody.innerHTML = '';
      if (recent.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="2" style="text-align:center;">No recent calculations.</td></tr>';
      } else {
        recent.forEach((item) => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
           <td>
             <a href="/card/${item.categorySlug}#${item.calcName.replace(
            / /g,
            '_'
          )}">
               ${item.calcName} <span style="color: #888;">(${
            item.categoryTitle
          })</span>
             </a>
           </td>
           <td style="text-align:right; color:#1d4ed8; font-weight:600;">
             ${item.result} ${item.unit ? item.unit : ''}
           </td>
         `;
          tbody.appendChild(tr);
        });
      }
    });
  }
});

function redirectToDetailPage(element) {
  const slug = element.getAttribute('data-slug');
  window.location.href = `/card/${slug}`;
}
