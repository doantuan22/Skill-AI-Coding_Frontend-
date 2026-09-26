document.addEventListener("DOMContentLoaded", () => {
  // Mobile Nav Toggle
  const navToggle = document.getElementById("nav-toggle");
  const navMenu = document.getElementById("nav-menu");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const isExpanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!isExpanded));
      navMenu.classList.toggle("is-active");
    });
  }

  // Dialog / Modal Logic
  const openModalBtn = document.getElementById("open-modal-btn");
  const closeModalBtn = document.getElementById("close-modal-btn");
  const modalDismissBtn = document.getElementById("modal-dismiss-btn");
  const modalBackdrop = document.getElementById("modal-backdrop");

  const openModal = () => {
    if (modalBackdrop) {
      modalBackdrop.classList.add("is-open");
      modalBackdrop.setAttribute("aria-hidden", "false");
      closeModalBtn?.focus();
    }
  };

  const closeModal = () => {
    if (modalBackdrop) {
      modalBackdrop.classList.remove("is-open");
      modalBackdrop.setAttribute("aria-hidden", "true");
      openModalBtn?.focus();
    }
  };

  openModalBtn?.addEventListener("click", openModal);
  closeModalBtn?.addEventListener("click", closeModal);
  modalDismissBtn?.addEventListener("click", closeModal);

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modalBackdrop?.classList.contains("is-open")) {
      closeModal();
    }
  });

  // Contact Form Validation
  const form = document.getElementById("contact-form");
  const nameInput = document.getElementById("input-name");
  const emailInput = document.getElementById("input-email");
  const messageInput = document.getElementById("input-message");
  const nameGroup = document.getElementById("group-name");
  const emailGroup = document.getElementById("group-email");
  const messageGroup = document.getElementById("group-message");
  const nameError = document.getElementById("name-error");
  const emailError = document.getElementById("email-error");
  const messageError = document.getElementById("message-error");
  const formStatus = document.getElementById("form-status");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      let isValid = true;

      // Validate Name
      if (!nameInput.value.trim()) {
        nameGroup.classList.add("has-error");
        nameError.textContent = "Full name is required.";
        isValid = false;
      } else {
        nameGroup.classList.remove("has-error");
        nameError.textContent = "";
      }

      // Validate Email
      const emailValue = emailInput.value.trim();
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailValue) {
        emailGroup.classList.add("has-error");
        emailError.textContent = "Corporate email is required.";
        isValid = false;
      } else if (!emailPattern.test(emailValue)) {
        emailGroup.classList.add("has-error");
        emailError.textContent = "Please enter a valid email address.";
        isValid = false;
      } else {
        emailGroup.classList.remove("has-error");
        emailError.textContent = "";
      }

      // Validate Message
      if (!messageInput.value.trim()) {
        messageGroup.classList.add("has-error");
        messageError.textContent = "Project scope description is required.";
        isValid = false;
      } else {
        messageGroup.classList.remove("has-error");
        messageError.textContent = "";
      }

      if (isValid) {
        formStatus.className = "form-status success";
        formStatus.textContent = "Thank you! Your validation request has been accepted.";
        form.reset();
      } else {
        formStatus.className = "form-status";
        formStatus.textContent = "";
      }
    });
  }
});
