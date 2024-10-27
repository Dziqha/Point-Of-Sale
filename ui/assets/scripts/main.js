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

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

function formatRupiah(value) {
  const [whole, fraction] = value.toFixed(2).split(".");

  const formattedWhole = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  return `${formattedWhole},${fraction}`;
}

function formatRupiahv2(amount) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

function inputToRupiah(value) {
  if (typeof value !== "string") {
    value = value.toString();
  }

  const cleanedValue = value.replace(/[^,\d]/g, "");
  const [whole, fraction] = cleanedValue.split(",");

  const formattedWhole = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

  return fraction !== undefined
    ? `${formattedWhole},${fraction}`
    : formattedWhole;
}

function formatInputToRupiah(input) {
  let value = input.value;

  value = inputToRupiah(value);

  input.value = value;
}

// function formatRupiah(amount) {
//   return new Intl.NumberFormat("id-ID", {
//     style: "currency",
//     currency: "IDR",
//   }).format(amount);
// }

// function parseRupiah(rupiahString) {
//   return parseInt(rupiahString.replace(/[^\d]/g, "")) || 0;
// }

// function formatInputToRupiah(input) {
//   let value = input.value.replace(/[^\d]/g, "");
//   if (value !== "") {
//     input.value = formatRupiah(parseInt(value));
//   } else {
//     input.value = "";
//   }
//}

document.addEventListener("DOMContentLoaded", () => {
  initializeModals();
});

var dropdown = document.querySelector(".dropdown");

dropdown.addEventListener("click", function (event) {
  event.stopPropagation();
  dropdown.classList.toggle("is-active");
});
