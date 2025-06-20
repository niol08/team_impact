function redirectToDetailPage(element) {
  const slug = element.getAttribute('data-slug');
  window.location.href = `/card/${slug}`;
}
window.redirectToDetailPage = redirectToDetailPage;

// document.addEventListener('DOMContentLoaded', function () {
//   document.querySelectorAll('.card[data-slug]').forEach(function (card) {
//     card.addEventListener('click', function () {
//       const slug = card.getAttribute('data-slug');
//       window.location.href = `/card/${slug}`;
//     });
//   });
// });

const DEMO_POLICIES = {
  planA: [
    'Deductible is ₦20,000 annually.',
    'Specialist visits are covered at 80% after a ₦500 copay.',
    'Prior authorization is required for CT scans, MRIs, and injections.',
  ],
  planB: [
    'All preventive services are covered at 100%.',
    'Lab tests are 90% covered after deductible.',
    'You must get a referral for all specialist visits.',
  ],
};

document.addEventListener('DOMContentLoaded', function () {
  const yearSpan = document.getElementById('current-year');
  const currentYear = new Date().getFullYear();
  yearSpan.textContent = currentYear;
});

document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('search-input');
  const resultsDiv = document.getElementById('live-search-results');

  if (!input || !resultsDiv) return;

  input.addEventListener('input', function () {
    const query = input.value.trim();
    if (query.length === 0) {
      resultsDiv.innerHTML = '';
      return;
    }
    fetch(`/search_api?query=${encodeURIComponent(query)}`)
      .then((response) => response.json())
      .then((results) => {
        if (results.length === 0) {
          resultsDiv.innerHTML = '<p>No results found.</p>';
        } else {
          resultsDiv.innerHTML =
            '<ul>' +
            results
              .map(
                (card) =>
                  `<li>
  <a href="/search?query=${encodeURIComponent(card.name)}">${card.name}</a>
  <p>${card.description}</p>
</li>`
              )
              .join('') +
            '</ul>';
        }
      });
  });

  document.addEventListener('click', function (e) {
    if (!resultsDiv.contains(e.target) && e.target !== input) {
      resultsDiv.innerHTML = '';
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const counter = document.getElementById('calc-counter');
  const section = document.getElementById('calc-count-section');
  let hasAnimated = false;

  if (!counter || !section) return;

  function animateCounter() {
    let count = 1;
    const target = 100;
    const duration = 1500;
    const stepTime = Math.max(Math.floor(duration / target), 10);

    function updateCounter() {
      counter.textContent = count;
      if (count < target) {
        count++;
        setTimeout(updateCounter, stepTime);
      }
    }
    updateCounter();
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !hasAnimated) {
          animateCounter();
          hasAnimated = true;
          obs.unobserve(section);
        }
      });
    },
    { threshold: 0.3 }
  );

  observer.observe(section);
});

document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger-btn');
  const navLinks = document.getElementById('nav-links');
  const navOverlay = document.getElementById('nav-overlay');

  function closeMenu() {
    hamburger.classList.remove('open');
    navLinks.classList.remove('open');
    navOverlay.classList.remove('open');
    document.body.classList.remove('no-scroll');
  }

  if (hamburger && navLinks && navOverlay) {
    hamburger.addEventListener('click', function () {
      const isOpen = hamburger.classList.toggle('open');
      navLinks.classList.toggle('open');
      navOverlay.classList.toggle('open');
      document.body.classList.toggle('no-scroll', isOpen);
    });

    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMenu);
    });

    navOverlay.addEventListener('click', closeMenu);
  }
});
