// JavaScript per gestire il cambio di tema
const themeToggles = [
  document.getElementById("theme-toggle-mobile"),
  document.getElementById("theme-toggle"),
  document.getElementById("theme-toggle-light"),
  // Add dropdown toggles
  document.getElementById("theme-toggle-dropdown-dark"),
  document.getElementById("theme-toggle-dropdown-light")
].filter(Boolean); // Filter out any null elements

const htmlElement = document.documentElement;

// Funzione per leggere e stampare il tema corrente dal localStorage
const printCurrentTheme = () => {
  const currentTheme = localStorage.getItem("theme");
  return currentTheme;
};

const setTheme = (theme) => {
  const isDark = theme === "dark";
  htmlElement.classList.toggle("dark", isDark);
  
  // Handle all toggles regardless of type (img or i elements)
  themeToggles.forEach((toggle) => {
    if (toggle) {
      // For FontAwesome icons
      if (toggle.tagName === 'I') {
        toggle.classList.toggle("text-black", !isDark);
        toggle.classList.toggle("fa-sun", isDark);
        toggle.classList.toggle("fa-moon", !isDark);
        toggle.classList.toggle("icona", isDark);
      }
      
      // For image toggles, they'll be properly shown/hidden by CSS classes
    }
  });
  
  localStorage.setItem("theme", theme);
  // Chiama la funzione per stampare il tema corrente
  printCurrentTheme();
  // Dispatch event for components that need to react to theme changes
  window.dispatchEvent(new Event("themeChanged"));
};

// Set up event listeners for all toggle elements
themeToggles.forEach((toggle) => {
  if (toggle) {
    // For direct toggles (images or icons)
    toggle.addEventListener("click", () => {
      const newTheme = htmlElement.classList.contains("dark") ? "light" : "dark";
      setTheme(newTheme);
    });
    
    // For parent elements that might need click handling
    if (toggle.parentElement && (toggle.id === "theme-toggle" || toggle.id === "theme-toggle-light")) {
      toggle.parentElement.addEventListener("click", () => {
        const newTheme = htmlElement.classList.contains("dark") ? "light" : "dark";
        setTheme(newTheme);
      });
    }
  }
});

// Apply saved theme or use system preference as fallback
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  setTheme(savedTheme);
} else {
  // Use system preference
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  setTheme(prefersDark ? "dark" : "light");
}

// funzione tooltip
function toggleTooltip(element) {
  const tooltipContainerId = element.getAttribute("data-tooltip-target");
  const tooltipContainer = document.getElementById(tooltipContainerId);

  const isActive = tooltipContainer.classList.contains("active");
  document
    .querySelectorAll(".tooltip_container.active")
    .forEach((container) => container.classList.remove("active"));

  if (!isActive) {
    tooltipContainer.classList.add("active");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".form-group, .form-group2").forEach((form) => {
    form.addEventListener("click", function (e) {
      if (e.target.classList.contains("clear-button")) {
        const input = e.target.previousElementSibling.previousElementSibling;
        input.value = "";
        input.focus();
        updateClearButton(input);
        e.preventDefault();
      }
    });
  });

  function updateClearButton(input) {
    const clearButton = input.parentElement.querySelector(".clear-button");
    clearButton.style.display =
      input.value || document.activeElement === input ? "flex" : "none";
  }

  document.querySelectorAll(".custom-input").forEach((input) => {
    // Mostra/nascondi X su input
    input.addEventListener("input", () => updateClearButton(input));

    // Mostra X su focus
    input.addEventListener("focus", () => updateClearButton(input));

    // Nascondi X su blur
    input.addEventListener("blur", () => {
      setTimeout(() => updateClearButton(input), 100);
    });

    // Inizializzazione
    updateClearButton(input);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.querySelector("#intervention_scope");
  
  // Verifica se l'elemento textarea esiste prima di procedere
  if (textarea) {
    const clearButton = textarea.parentElement.querySelector(".clear-button");
    
    // Controlla anche se il clearButton esiste
    if (clearButton) {
      // Funzione per controllare se mostrare la X
      const updateClearButton = (element) => {
        const clearBtn = element.parentElement.querySelector(".clear-button");
        const shouldShow = element.value || document.activeElement === element;
        clearBtn.style.display = shouldShow ? "flex" : "none";
      };

      // Gestisce il click sulla X
      clearButton.addEventListener("click", function () {
        textarea.value = "";
        textarea.focus();
      });

      // Gestisce l'input
      textarea.addEventListener("input", function () {
        updateClearButton(this);
      });

      // Gestisce il focus
      textarea.addEventListener("focus", function () {
        updateClearButton(this);
      });

      // Gestisce la perdita del focus
      textarea.addEventListener("blur", function () {
        updateClearButton(this);
      });
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const requiredFields = document.querySelectorAll("[custom_req]");
  const submitButton = document.querySelector("#nextButton");
  if (submitButton) {
    submitButton.addEventListener("click", function(e) {
      let hasEmptyField = false;
      
      requiredFields.forEach(field => {
        if (!field.value || field.value.trim() === '') {
          field.style.border = '3px solid red';
          hasEmptyField = true;
        } else {
          field.style.border = ''; // Reset border if field has value
        }
      });

      if (hasEmptyField) {
        e.preventDefault(); // Prevent form submission if required fields are empty
        alert("Per favore, completa tutti i campi obbligatori.");
      }
    });

    // Remove red border when user starts typing
    requiredFields.forEach(field => {
      field.addEventListener('input', function() {
        if (field.value && field.value.trim() !== '') {
          field.style.border = '';
        }
      });
    });
  }
  
})

document.addEventListener("DOMContentLoaded", function() {
  // Get all input elements
  const inputs = document.querySelectorAll('input');
  
  // Add keydown event listener to each input
  inputs.forEach(input => {
    input.addEventListener('keydown', function(e) {
      // Check if the pressed key is Enter
      if (e.key === 'Enter') {
        e.preventDefault(); // Prevent default Enter behavior
      }
    });
  });
});

