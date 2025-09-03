// app.js
document.addEventListener('DOMContentLoaded', function () {
  // ============================
  // THEME TOGGLE (works on all pages)
  // ============================
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;

  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const useDark = (savedTheme === 'dark') || (!savedTheme && prefersDark);

  if (useDark) {
    document.body.classList.add('dark-theme');
    if (themeIcon) themeIcon.classList.replace('fa-moon', 'fa-sun');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-theme');
      if (document.body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
        if (themeIcon) themeIcon.classList.replace('fa-moon', 'fa-sun');
      } else {
        localStorage.setItem('theme', 'light');
        if (themeIcon) themeIcon.classList.replace('fa-sun', 'fa-moon');
      }
    });
  }

  // ============================
  // INDEX PAGE ONLY: QUESTIONNAIRE + RECOMMENDATION
  // ============================
  const recommendBtn = document.getElementById('recommend-btn');
  const resultsContainer = document.getElementById('results-container');
  const petResults = document.getElementById('pet-results');
  const sortSelect = document.getElementById('sort-by');

  if (recommendBtn && resultsContainer && petResults) {
    recommendBtn.addEventListener('click', async function () {
      const homeSize = document.getElementById('home-size').value;
      const kids = document.getElementById('kids').value;
      const allergies = document.getElementById('allergies').value;
      const activity = document.getElementById('activity').value;
      const experience = document.getElementById('experience').value;

      if (!homeSize || !kids || !allergies || !activity || !experience) {
        alert('Please complete all fields in the questionnaire.');
        return;
      }

      const prefs = {
        home_size: homeSize,
        has_kids: kids !== 'none',
        kids_age: kids,
        allergies: allergies,
        activity: activity,
        experience: experience
      };

      try {
        const res = await fetch('/api/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(prefs)
        });
        if (!res.ok) throw new Error('Server error');
        const results = await res.json();

        // Update chips
        const setChip = (id, selId) => {
          const chip = document.getElementById(id);
          const sel = document.getElementById(selId);
          if (chip && sel) chip.querySelector('span').textContent = sel.selectedOptions[0].text;
        };
        setChip('chip-home-size', 'home-size');
        setChip('chip-kids', 'kids');
        setChip('chip-allergies', 'allergies');
        setChip('chip-activity', 'activity');
        setChip('chip-experience', 'experience');

        // Show results
        resultsContainer.style.display = 'block';
        renderResults(results);

        // Smooth scroll
        resultsContainer.scrollIntoView({ behavior: 'smooth' });

        // Attach sorting
        if (sortSelect) {
          sortSelect.onchange = () => renderResults(results, sortSelect.value);
        }
      } catch (err) {
        console.error(err);
        alert('Something went wrong with the recommendation.');
      }
    });

    function renderResults(results, sortBy = 'score') {
      petResults.innerHTML = '';
      let sorted = [...results];
      if (sortBy === 'size') {
        sorted.sort((a, b) => (a.size || '').localeCompare(b.size || ''));
      } else if (sortBy === 'activity') {
        sorted.sort((a, b) => (a.activity || '').localeCompare(b.activity || ''));
      } else {
        sorted.sort((a, b) => (b.match || 0) - (a.match || 0));
      }

      sorted.forEach(pet => {
        const petCard = document.createElement('div');
        petCard.className = 'pet-card fade-in subtle';
        petCard.innerHTML = `
          <div class="pet-image" style="background-image: url('${pet.image}')"></div>
          <div class="pet-info">
              <span class="match-badge">${pet.match ?? 0}% Match</span>
              <h3>${pet.name}</h3>
              <div class="pet-meta">${pet.type} • ${pet.breed} • ${pet.age}</div>
              <div class="pet-meta">${pet.size} • ${pet.temperament || ''}</div>
              <p class="pet-description">${pet.description || ''}</p>
              <div class="pet-actions">
                  <button class="btn outline learnMoreBtn">Learn More</button>
                  <button class="btn primary contactBtn">Contact Shelter</button>
              </div>
          </div>
        `;
        // wire buttons
        petCard.querySelector('.learnMoreBtn').addEventListener('click', () => openLearnMore(pet));
        petCard.querySelector('.contactBtn').addEventListener('click', () => openContactForm(pet));

        petResults.appendChild(petCard);
      });
    }
  }

  // ============================
  // FADE-IN (subtle)
  // ============================
  const fadeElements = document.querySelectorAll('.fade-in');
  if (fadeElements.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.style.opacity = 1;
      });
    }, { threshold: 0.1 });

    fadeElements.forEach(element => {
      element.style.opacity = 0;
      element.style.transition = 'opacity 0.45s ease-in-out';
      observer.observe(element);
    });
  }

  // ============================
  // SHARED MODALS (present on both pages)
  // ============================
  window.openLearnMore = function (pet) {
    const m = document.getElementById("learnMoreModal");
    if (!m) return;
    document.getElementById("petName").textContent = pet.name;
    document.getElementById("petImage").src = pet.image;
    document.getElementById("petBreed").textContent = pet.breed || "—";
    document.getElementById("petAge").textContent = pet.age || "—";
    document.getElementById("petSize").textContent = pet.size || "—";
    document.getElementById("petTemperament").textContent = pet.temperament || "—";
    document.getElementById("petDescription").textContent = pet.description || "";
    m.style.display = "block";
  };

  window.openContactForm = function (pet) {
    const m = document.getElementById("contactModal");
    if (!m) return;
    document.getElementById("contactPetName").value = pet.name;
    m.style.display = "block";
  };

  const closeLearn = document.getElementById("closeLearnMore");
  if (closeLearn) closeLearn.onclick = () => {
    document.getElementById("learnMoreModal").style.display = "none";
  };
  const closeContact = document.getElementById("closeContact");
  if (closeContact) closeContact.onclick = () => {
    document.getElementById("contactModal").style.display = "none";
  };

  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", function(e) {
      e.preventDefault();
      alert(`Message sent for ${document.getElementById("contactPetName").value}!\nWe will contact you soon.`);
      document.getElementById("contactModal").style.display = "none";
    });
  }
});
