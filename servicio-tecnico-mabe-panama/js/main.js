// Servicio Técnico Cartagena — funciones compartidas del sitio
(function () {
  "use strict";

  // Fuerza que cada página cargue desde arriba (donde está el título <h1>),
  // salvo que la URL tenga un ancla específica (#contacto-...). Evita que el
  // navegador restaure una posición de scroll de la página anterior.
  if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
  }
  if (!window.location.hash) {
    window.scrollTo(0, 0);
  }
  window.addEventListener("pageshow", function () {
    if (!window.location.hash) window.scrollTo(0, 0);
  });

  // Menú móvil
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.querySelector("nav.main-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var abierto = menu.classList.toggle("abierto");
      toggle.setAttribute("aria-expanded", abierto ? "true" : "false");
    });
  }

  // Tracking simple de clics en CTA (WhatsApp / llamada) hacia dataLayer (GTM)
  window.dataLayer = window.dataLayer || [];
  function trackConversion(label) {
    window.dataLayer.push({ event: "conversion_click", cta_label: label });
  }
  document.querySelectorAll("[data-track]").forEach(function (el) {
    el.addEventListener("click", function () {
      trackConversion(el.getAttribute("data-track"));
    });
  });

  // Formulario de agendamiento -> arma un mensaje y redirige a WhatsApp
  var form = document.querySelector("#form-agendamiento");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var nombre = form.nombre.value.trim();
      var telefono = form.telefono.value.trim();
      var servicio = form.servicio.value;
      var marca = form.dataset.marca || "";
      var detalle = form.detalle.value.trim();
      var numero = form.dataset.whatsapp;

      var texto =
        "Hola, quiero agendar un servicio técnico" +
        (marca ? " " + marca : "") +
        " en Cartagena.%0A" +
        "Nombre: " + nombre + "%0A" +
        "Teléfono: " + telefono + "%0A" +
        "Servicio: " + servicio +
        (detalle ? "%0ADetalle: " + detalle : "");

      trackConversion("Formulario_Agendamiento");
      window.open("https://wa.me/" + numero + "?text=" + texto, "_blank");
      form.reset();
      var msg = form.querySelector(".form-gracias");
      if (msg) msg.hidden = false;
    });
  }
})();
