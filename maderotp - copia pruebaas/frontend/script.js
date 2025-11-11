// --- ELIMINAMOS personaForm y reservaForm ---
const tablaBody = document.querySelector("#tablaReservas tbody");
// --- AÑADIMOS el nuevo formulario ---
const reservaCompletaForm = document.getElementById("reservaCompletaForm");


// --- NUEVO LISTENER para el formulario combinado ---
reservaCompletaForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  // 1. Agrupar datos de la persona
  const datosPersona = {
    nombre: document.getElementById("nombre").value,
    telefono: document.getElementById("telefono").value,
    email: document.getElementById("email").value,
    direccion: document.getElementById("direccion").value
  };

  // 2. Agrupar datos de la reserva
  const datosReserva = {
    fecha: document.getElementById("fecha").value,
    hora: document.getElementById("hora").value,
    personas: document.getElementById("personas").value,
    ubicacion: document.getElementById("ubicacion").value,
    tipo_pedido: document.getElementById("tipo_pedido").value
  };

  // 3. Crear el objeto JSON combinado
  const data = {
    persona: datosPersona,
    reserva: datosReserva
  };

  try {
    // 4. Enviar al nuevo endpoint
    const response = await fetch("http://127.0.0.1:8000/reservas-completas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error desconocido del servidor');
    }

    alert("Reserva registrada correctamente ✅");
    reservaCompletaForm.reset();
    cargarReservas(); // Recarga la tabla

    // Redirigir a la página de reservas
    window.location.hash = "#page-reservas";

  } catch (error) {
    alert("Error al registrar reserva:\n" + error.message);
  }
});


// --- ELIMINAMOS los listeners de personaForm y reservaForm ---


// Mostrar reservas en tabla (Sin cambios)
async function cargarReservas() {
  try {
    const res = await fetch("http://127.0.0.1:8000/reservas");
    if (!res.ok) {
      throw new Error("No se pudieron cargar las reservas.");
    }
    const data = await res.json();
    tablaBody.innerHTML = "";

    data.forEach(r => {
      // Esta lógica ahora es más segura porque r.persona NUNCA será nulo
      const nombrePersona = r.persona ? r.persona.nombre : 'Error de datos';

      const row = `
        <tr>
          <td>${r.id}</td>
          <td>${nombrePersona}</td> 
          <td>${r.fecha}</td>
          <td>${r.hora}</td>
          <td>${r.personas}</td>
          <td>${r.ubicacion}</td>
          <td>${r.tipo_pedido}</td>
        </tr>
      `;
      tablaBody.innerHTML += row;
    });
  } catch (error) {
    tablaBody.innerHTML = `<tr><td colspan="7">Error al cargar datos: ${error.message}</td></tr>`;
  }
}

// Carga inicial de reservas
cargarReservas();


// Lógica de Navegación SPA (Sin cambios, solo renombramos el hash)
const pageSections = document.querySelectorAll(".page-section");

function navigate() {
  let hash = window.location.hash;
  
  // Renombramos el hash de registro
  if (hash === "#page-clientes") {
    hash = "#page-registrar";
  }

  if (!hash || hash === "#") {
    hash = "#page-inicio";
  }

  pageSections.forEach(section => {
    section.classList.remove("active");
  });

  try {
    const activePage = document.querySelector(hash);
    activePage.classList.add("active");
  } catch (e) {
    document.querySelector("#page-inicio").classList.add("active");
  }
}

window.addEventListener("hashchange", navigate);
document.addEventListener("DOMContentLoaded", navigate);