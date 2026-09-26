// Target B - Enterprise Cloud Dashboard Interactions
document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const sidebar = document.getElementById('sidebar');
  const menuToggleBtn = document.getElementById('menu-toggle-btn');
  const sidebarCloseBtn = document.getElementById('sidebar-close-btn');

  const stateSelect = document.getElementById('state-select');
  const stateDataContainer = document.getElementById('state-data-container');
  const stateLoadingContainer = document.getElementById('state-loading-container');
  const stateEmptyContainer = document.getElementById('state-empty-container');
  const stateErrorContainer = document.getElementById('state-error-container');

  const filterChips = document.getElementById('filter-chips');
  const searchInput = document.getElementById('search-input');
  const tableBody = document.getElementById('table-body');
  const resetFilterBtn = document.getElementById('reset-filter-btn');
  const retryBtn = document.getElementById('retry-btn');

  const openNewDeploymentBtn = document.getElementById('open-new-deployment-btn');
  const deploymentModalBackdrop = document.getElementById('deployment-modal-backdrop');
  const closeDeploymentModalBtn = document.getElementById('close-deployment-modal-btn');
  const cancelDeploymentBtn = document.getElementById('cancel-deployment-btn');
  const newDeploymentForm = document.getElementById('new-deployment-form');

  let activeFilter = 'all';
  let activeSearch = '';

  // 1. Sidebar Drawer Toggle
  if (menuToggleBtn && sidebar) {
    menuToggleBtn.addEventListener('click', () => {
      sidebar.classList.add('drawer-open');
    });
  }

  if (sidebarCloseBtn && sidebar) {
    sidebarCloseBtn.addEventListener('click', () => {
      sidebar.classList.remove('drawer-open');
    });
  }

  // 2. UI State Switcher (for automated / deterministic UI testing)
  function setActiveState(state) {
    const states = {
      data: stateDataContainer,
      loading: stateLoadingContainer,
      empty: stateEmptyContainer,
      error: stateErrorContainer,
    };

    Object.entries(states).forEach(([key, el]) => {
      if (!el) return;
      if (key === state) {
        el.style.display = (key === 'data' ? 'block' : 'flex');
      } else {
        el.style.display = 'none';
      }
    });
  }

  if (stateSelect) {
    stateSelect.addEventListener('change', (e) => {
      setActiveState(e.target.value);
    });
  }

  // 3. Table Filtering
  function filterRows() {
    if (!tableBody) return;
    const rows = tableBody.querySelectorAll('tr');
    let visibleCount = 0;

    rows.forEach((row) => {
      const status = row.getAttribute('data-status');
      const text = row.textContent.toLowerCase();
      const matchesFilter = (activeFilter === 'all' || status === activeFilter);
      const matchesSearch = (!activeSearch || text.includes(activeSearch));

      if (matchesFilter && matchesSearch) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });

    // If active state is data but no rows match, switch to empty state or back
    if (stateSelect && stateSelect.value === 'data') {
      if (visibleCount === 0) {
        stateDataContainer.style.display = 'none';
        stateEmptyContainer.style.display = 'flex';
      } else {
        stateDataContainer.style.display = 'block';
        stateEmptyContainer.style.display = 'none';
      }
    }
  }

  if (filterChips) {
    filterChips.addEventListener('click', (e) => {
      const chip = e.target.closest('.chip');
      if (!chip) return;
      filterChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeFilter = chip.getAttribute('data-filter') || 'all';
      filterRows();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      activeSearch = e.target.value.trim().toLowerCase();
      filterRows();
    });
  }

  if (resetFilterBtn) {
    resetFilterBtn.addEventListener('click', () => {
      activeFilter = 'all';
      activeSearch = '';
      if (searchInput) searchInput.value = '';
      if (filterChips) {
        filterChips.querySelectorAll('.chip').forEach((c, idx) => {
          c.classList.toggle('active', idx === 0);
        });
      }
      if (stateSelect) stateSelect.value = 'data';
      setActiveState('data');
      filterRows();
    });
  }

  if (retryBtn) {
    retryBtn.addEventListener('click', () => {
      if (stateSelect) stateSelect.value = 'data';
      setActiveState('data');
    });
  }

  // 4. Modal Dialog Handlers
  function openModal() {
    if (deploymentModalBackdrop) {
      deploymentModalBackdrop.classList.add('open');
      deploymentModalBackdrop.setAttribute('aria-hidden', 'false');
      const firstInput = deploymentModalBackdrop.querySelector('input');
      if (firstInput) firstInput.focus();
    }
  }

  function closeModal() {
    if (deploymentModalBackdrop) {
      deploymentModalBackdrop.classList.remove('open');
      deploymentModalBackdrop.setAttribute('aria-hidden', 'true');
    }
  }

  if (openNewDeploymentBtn) {
    openNewDeploymentBtn.addEventListener('click', openModal);
  }

  if (closeDeploymentModalBtn) {
    closeDeploymentModalBtn.addEventListener('click', closeModal);
  }

  if (cancelDeploymentBtn) {
    cancelDeploymentBtn.addEventListener('click', closeModal);
  }

  if (newDeploymentForm) {
    newDeploymentForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const serviceName = document.getElementById('service-name')?.value || 'new-service';
      const region = document.getElementById('target-region')?.value || 'us-east-1';
      const replicas = document.getElementById('replicas')?.value || '1';

      if (tableBody) {
        const newRow = document.createElement('tr');
        newRow.setAttribute('data-status', 'pending');
        newRow.id = `row-${serviceName.replace(/[^a-zA-Z0-9_-]/g, '')}`;
        newRow.innerHTML = `
          <td class="font-semibold">${serviceName}</td>
          <td>${region}</td>
          <td><span class="status-pill status-pending">Pending</span></td>
          <td>1 / ${replicas}</td>
          <td>--</td>
          <td class="text-right">
            <button class="btn btn-sm btn-outline row-action-btn" data-service="${serviceName}">View</button>
          </td>
        `;
        tableBody.prepend(newRow);
      }

      newDeploymentForm.reset();
      closeModal();
      filterRows();
    });
  }
});
