(() => {
  'use strict';

  const issueSearch = document.querySelector('[data-issue-search]');
  const issueRows = [...document.querySelectorAll('[data-issue-row]')];
  const filterButtons = [...document.querySelectorAll('[data-issue-filter]')];
  const issueCount = document.querySelector('[data-issue-count]');
  const noResults = document.querySelector('[data-no-results]');
  let activeFilter = 'all';

  function normalize(value) {
    return String(value || '').trim().toLocaleLowerCase();
  }

  function filterIssues() {
    if (!issueRows.length) return;
    const term = normalize(issueSearch?.value);
    let visible = 0;

    issueRows.forEach((row) => {
      const haystack = normalize(row.dataset.search);
      const status = row.dataset.status || '';
      const matchesTerm = !term || haystack.includes(term);
      const matchesFilter = activeFilter === 'all' || status === activeFilter;
      const show = matchesTerm && matchesFilter;
      row.hidden = !show;
      if (show) visible += 1;
    });

    if (issueCount) {
      issueCount.textContent = `${visible} issue${visible === 1 ? '' : 's'} shown`;
    }
    if (noResults) noResults.hidden = visible !== 0;
  }

  issueSearch?.addEventListener('input', filterIssues);

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.issueFilter || 'all';
      filterButtons.forEach((candidate) => {
        candidate.setAttribute('aria-pressed', String(candidate === button));
      });
      filterIssues();
    });
  });

  filterIssues();

  // Keep long process pages calm: opening one check closes the others.
  const checkCards = [...document.querySelectorAll('details[data-exclusive-check]')];
  checkCards.forEach((card) => {
    card.addEventListener('toggle', () => {
      if (!card.open) return;
      checkCards.forEach((other) => {
        if (other !== card) other.open = false;
      });
    });
  });
})();
