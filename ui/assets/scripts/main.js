function initializeModals() {
  function openModal($el) {
    $el.classList.add("is-active");
  }

  function closeModal($el) {
    $el.classList.remove("is-active");
  }

  function closeAllModals() {
    (document.querySelectorAll(".modal") || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  (document.querySelectorAll(".js-modal-trigger") || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener("click", () => {
      openModal($target);
    });
  });

  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button"
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");

    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllModals();
    }
  });
}

function errorAlert(text) {
  Toastify({
    text: text,
    close: true,
    style: {
      background: "hsl(348, 100%, 61%)	",
    },
  }).showToast();
}

function successAlert(text) {
  Toastify({
    text: text,
    close: true,
    style: {
      background: "hsl(141, 71%, 48%)	",
    },
  }).showToast();
}

document.addEventListener("DOMContentLoaded", () => {
  initializeModals();
});
