// all-pets.js
document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('all-pets-grid');
  const emptyState = document.getElementById('empty-state');

  const searchText = document.getElementById('search-text');
  const filterType = document.getElementById('filter-type');
  const filterAge = document.getElementById('filter-age');
  const filterSize = document.getElementById('filter-size');
  const filterActivity = document.getElementById('filter-activity');
  const filterHypo = document.getElementById('filter-hypo');
  const filterKids = document.getElementById('filter-kids');
  const sortAll = document.getElementById('sort-all');
  const resetBtn = document.getElementById('reset-filters');

  const KNOWN_TYPES = new Set([
    'dog', 'cat', 'rabbit', 'bird', 'hamster', 'guinea pig', 'turtle'
  ]);

  let allPets = [];
  let filtered = [];

  // Utilities
  const toMonths = (ageString = '') => {
    const s = String(ageString).toLowerCase().trim();
    // examples: "6 months", "1 year", "2 years", "8 months"
    const num = parseFloat(s);
    if (isNaN(num)) return null;
    if (s.includes('year')) return Math.round(num * 12);
    return Math.round(num); // assume months
  };

  const inAgeRange = (months, sel) => {
    if (months == null) return true; // keep items if age unknown
    switch (sel) {
      case 'under-12': return months < 12;
      case '12-36': return months >= 12 && months <= 36;
      case '37-72': return months >= 37 && months <= 72;
      case 'over-72': return months > 72;
      case 'any':
      default: return true;
    }
  };

  const normalize = (v) => (v || '').toString().toLowerCase();

  // Fetch all pets
  const load = async () => {
    const res = await fetch('/api/pets');
    allPets = await res.json();
    filtered = [...allPets];
    applyFiltersAndRender();
  };

  // Filtering
  const applyFiltersAndRender = () => {
    const q = normalize(searchText.value);
    const t = normalize(filterType.value);
    const a = filterAge.value;
    const sz = normalize(filterSize.value);
    const act = normalize(filterActivity.value);
    const hypo = filterHypo.checked;
    const kids = filterKids.checked;

    filtered = allPets.filter((p) => {
      const name = normalize(p.name);
      const breed = normalize(p.breed);
      const type = normalize(p.type);
      const desc = normalize(p.description);
      const size = normalize(p.size);
      const activity = normalize(p.activity);
      const goodWithKids = !!p.good_with_children;
      const isHypo = !!p.hypoallergenic;

      // search text
      if (q && !(name.includes(q) || breed.includes(q) || desc.includes(q) || type.includes(q))) {
        return false;
      }

      // type filter
      if (t !== 'all' && t !== '' && t !== 'others' && t !== 'other') {
        if (type !== t) return false;
      }
      if (t === 'others' || t === 'other') {
        if (KNOWN_TYPES.has(type)) return false; // show types not in the known set
      }

      // age filter
      const months = toMonths(p.age);
      if (!inAgeRange(months, a)) return false;

      // size filter
      if (sz && sz !== 'all' && size !== sz) return false;

      // activity filter
      if (act && act !== 'all' && activity !== act) return false;

      // hypo
      if (hypo && !isHypo) return false;

      // good with kids
      if (kids && !goodWithKids) return false;

      return true;
    });

    // sort
    const sortVal = sortAll.value;
    const sizeOrder = { small: 1, medium: 2, large: 3 };
    filtered.sort((a, b) => {
      if (sortVal === 'age-asc' || sortVal === 'age-desc') {
        const am = toMonths(a.age) ?? 9999;
        const bm = toMonths(b.age) ?? 9999;
        return sortVal === 'age-asc' ? am - bm : bm - am;
      }
      if (sortVal === 'size') {
        const as = sizeOrder[normalize(a.size)] ?? 2;
        const bs = sizeOrder[normalize(b.size)] ?? 2;
        return as - bs;
      }
      // default name A–Z
      return a.name.localeCompare(b.name);
    });

    render();
  };

  // Render
  const render = () => {
    grid.innerHTML = '';
    if (filtered.length === 0) {
      emptyState.style.display = 'block';
      return;
    }
    emptyState.style.display = 'none';

    filtered.forEach((pet) => {
      const card = document.createElement('div');
      card.className = 'pet-card fade-in subtle';
      card.innerHTML = `
        <div class="pet-image" style="background-image:url('${pet.image}')"></div>
        <div class="pet-info">
          <h3>${pet.name}</h3>
          <div class="pet-meta">${pet.type} • ${pet.breed} • ${pet.age}</div>
          <div class="pet-meta">${pet.size} • ${pet.activity || 'moderate'}</div>
          <p class="pet-description">${pet.description || ''}</p>
          <div class="pet-actions">
            <button class="btn outline learn-btn">Learn More</button>
            <button class="btn primary contact-btn">Contact Shelter</button>
          </div>
        </div>
      `;
      // wire buttons
      card.querySelector('.learn-btn').addEventListener('click', () => {
        (window.openLearnMore || fallbackLearnMore)(pet);
      });
      card.querySelector('.contact-btn').addEventListener('click', () => {
        (window.openContactForm || fallbackContact)(pet);
      });

      grid.appendChild(card);
    });
  };

  // Fallback modals if app.js wasn’t loaded first (safety)
  function fallbackLearnMore(pet) {
    const m = document.getElementById('learnMoreModal');
    document.getElementById('petName').textContent = pet.name;
    document.getElementById('petImage').src = pet.image;
    document.getElementById('petBreed').textContent = pet.breed || '—';
    document.getElementById('petAge').textContent = pet.age || '—';
    document.getElementById('petSize').textContent = pet.size || '—';
    document.getElementById('petTemperament').textContent = pet.temperament || '—';
    document.getElementById('petDescription').textContent = pet.description || '';
    m.style.display = 'block';
  }
  function fallbackContact(pet) {
    document.getElementById('contactPetName').value = pet.name;
    document.getElementById('contactModal').style.display = 'block';
  }

  // Events
  const debounce = (fn, ms=250) => {
    let t; 
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  };

  searchText.addEventListener('input', debounce(applyFiltersAndRender, 200));
  [filterType, filterAge, filterSize, filterActivity, sortAll].forEach(el =>
    el.addEventListener('change', applyFiltersAndRender)
  );
  [filterHypo, filterKids].forEach(el =>
    el.addEventListener('input', applyFiltersAndRender)
  );
  resetBtn.addEventListener('click', () => {
    searchText.value = '';
    filterType.value = 'all';
    filterAge.value = 'any';
    filterSize.value = 'all';
    filterActivity.value = 'all';
    filterHypo.checked = false;
    filterKids.checked = false;
    sortAll.value = 'name-az';
    applyFiltersAndRender();
  });

  // Start
  load();
});
