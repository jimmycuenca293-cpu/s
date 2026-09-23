// Servicio Técnico Mabe Panamá — interacción del sitio
(function () {
  "use strict";

  // Evita el salto de scroll al navegar (el navegador restaura la
  // posición de la página anterior en algunos casos de bfcache/SPA-like nav).
  if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
  }
  if (!location.hash) {
    window.scrollTo(0, 0);
  }

  document.addEventListener("DOMContentLoaded", function () {
    // Menú móvil
    var abrir = document.querySelector("[data-abrir-menu]");
    var cajon = document.querySelector("[data-cajon-movil]");
    var cerrar = document.querySelector("[data-cerrar-menu]");
    if (abrir && cajon) {
      abrir.addEventListener("click", function () {
        cajon.classList.add("abierto");
        document.body.style.overflow = "hidden";
      });
    }
    if (cerrar && cajon) {
      cerrar.addEventListener("click", function () {
        cajon.classList.remove("abierto");
        document.body.style.overflow = "";
      });
    }
    if (cajon) {
      cajon.addEventListener("click", function (e) {
        if (e.target === cajon) {
          cajon.classList.remove("abierto");
          document.body.style.overflow = "";
        }
      });
    }

    // Revelado suave al hacer scroll
    var elementos = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && elementos.length) {
      var obs = new IntersectionObserver(
        function (entradas) {
          entradas.forEach(function (entrada) {
            if (entrada.isIntersecting) {
              entrada.target.classList.add("visto");
              obs.unobserve(entrada.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );
      elementos.forEach(function (el) {
        obs.observe(el);
      });
    } else {
      elementos.forEach(function (el) {
        el.classList.add("visto");
      });
    }

    // Formulario de agendamiento -> mensaje de WhatsApp
    var formulario = document.getElementById("form-agenda");
    if (formulario) {
      formulario.addEventListener("submit", function (e) {
        e.preventDefault();
        var numero = formulario.getAttribute("data-whatsapp") || "";
        var tipo = formulario.getAttribute("data-tipo") || "un electrodoméstico Mabe";
        var nombre = (formulario.querySelector("#nombre") || {}).value || "";
        var telefono = (formulario.querySelector("#telefono") || {}).value || "";
        var servicio = (formulario.querySelector("#servicio") || {}).value || "";
        var detalle = (formulario.querySelector("#detalle") || {}).value || "";
        var mensaje =
          "Hola, soy " + nombre + ". Necesito " + servicio + " para " + tipo +
          " Mabe en Panamá. Mi teléfono es " + telefono + ". " + detalle;
        var url = "https://wa.me/" + numero + "?text=" + encodeURIComponent(mensaje);
        window.open(url, "_blank", "noopener");
      });
    }

    // Seguimiento simple de clics a WhatsApp (para consola/analítica futura)
    document.querySelectorAll('a[href*="wa.me"]').forEach(function (a) {
      a.addEventListener("click", function () {
        if (window.gtag) {
          window.gtag("event", "click_whatsapp", { evento_categoria: "contacto" });
        }
      });
    });
  });
})();
