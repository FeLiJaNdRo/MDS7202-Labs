import os

import gradio as gr
from services import enviar_prediccion

# Leer backend url desde variables de entorno (usada dentro de services.py)
backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# Categorías válidas para los dropdown
canal_ticket_opciones = ["Whatsapp", "Correo", "Página Web"]
categoria_problema_opciones = ["Técnica", "Otro", "Fraude", "Cuenta", "Cobros", "Pregunta general"]
tipo_cuenta_opciones = ["Premium", "Free", "Business"]

# CSS custom: borde naranjo en las secciones + violeta claro al hacer focus en inputs
CUSTOM_CSS = """
/* Borde naranjo explícito en las secciones del formulario */
.seccion-borde-naranjo {
    border: 1px solid #f97316 !important;
    border-radius: 6px !important;
}

/* Violeta claro y saturado al hacer focus en cualquier input/textarea/select */
input:focus, textarea:focus, select:focus {
    border-color: #c084fc !important;
    box-shadow: 0 0 0 1px #c084fc !important;
    outline: none !important;
}
"""

# Definir el tema moderno, minimalista y con colores adecuados a una fintech
tema_personalizado = gr.themes.Base(
    primary_hue="sky",  # Celeste para los botones y elementos principales
    secondary_hue="orange",  # Naranja para elementos secundarios o enfoques
    neutral_hue="slate",  # Gris oscuro/moderno para fondos y bordes
).set(
    button_primary_background_fill="*primary_600",
    button_primary_background_fill_hover="*primary_700",
    button_secondary_background_fill="*secondary_500",
    input_background_fill="*neutral_800",
    input_background_fill_focus="*neutral_700",
    block_title_text_color="#c084fc",
    block_radius="6px",
    button_large_radius="6px",
    body_text_size="14px",
)


# Nota: canal, categoria, tipo_cuenta y antiguedad se capturan por completitud del formulario, pero NO se envían al modelo. El modelo final solo consume Asunto_Ticket + Contenido_Ticket.
def predecir(asunto, contenido, canal, categoria, tipo_cuenta, antiguedad):
    """Callback del botón: valida campos mínimos y llama al backend"""
    if not asunto.strip() or not contenido.strip():
        return "Asunto y Contenido son obligatorios para predecir la prioridad."

    return enviar_prediccion(asunto=asunto, contenido=contenido)


# Construcción de la interfaz de usuario
with gr.Blocks(theme=tema_personalizado, css=CUSTOM_CSS, title="ChaucherApp - Priorización de Tickets") as demo:
    gr.Markdown("# 💰 ChaucherApp — Priorización de Tickets de Soporte")

    # Sección de entrada de datos del ticket
    with gr.Group(elem_classes="seccion-borde-naranjo"):
        gr.Markdown("### Atributos del Ticket 📋")
        asunto_input = gr.Textbox(label="Asunto del Ticket", placeholder="Resumen breve del problema...")
        contenido_input = gr.Textbox(
            label="Contenido del Ticket", lines=4, placeholder="Describe el problema en detalle..."
        )
        with gr.Row():
            canal_input = gr.Dropdown(choices=canal_ticket_opciones, label="Canal del Ticket")
            categoria_input = gr.Dropdown(choices=categoria_problema_opciones, label="Categoría del Problema")

    # Atributos del usuario
    with gr.Group(elem_classes="seccion-borde-naranjo"):
        gr.Markdown("### Atributos del Usuario 👤")
        with gr.Row():
            tipo_cuenta_input = gr.Dropdown(choices=tipo_cuenta_opciones, label="Tipo de Cuenta")
            antiguedad_input = gr.Number(label="Antigüedad de la Cuenta (días)", minimum=0)

    # Boton para enviar la predicción y mostrar el resultado
    predecir_btn = gr.Button("Predecir Prioridad ↵", variant="primary")
    resultado_output = gr.Textbox(
        label="Nivel de Prioridad Predicho", interactive=False, elem_classes="seccion-borde-naranjo"
    )

    # Conectar el botón con la función de predicción
    predecir_btn.click(
        fn=predecir,
        inputs=[asunto_input, contenido_input, canal_input, categoria_input, tipo_cuenta_input, antiguedad_input],
        outputs=resultado_output,
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")
