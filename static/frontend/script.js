// static/frontend/script.js

document.getElementById('analysis-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const percentage = document.getElementById('percentage').value;
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error-message');

    // Ocultar mensajes anteriores y mostrar carga
    resultsDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        // !!! IMPORTANTE: Antes de desplegar en Render, cambia esta URL
        // !!! a tu dominio de Render (ej: 'https://mi-api.onrender.com/api/v1/analyze/')
        // !!!
        // !!! Para pruebas LOCALES (como ahora), usa 127.0.0.1:8000
        // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        const API_URL = 'http://127.0.0.1:8000/api/v1/analyze/';

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ train_percentage: percentage })
        });

        loadingDiv.classList.add('hidden');

        if (!response.ok) {
            // Manejo de errores 4xx o 5xx del servidor (ej. GCS no conecta)
            const errorData = await response.json();
            const status = response.status;
            errorDiv.textContent = `Error ${status}: ${errorData.error || response.statusText}. Por favor, verifica las variables de entorno de GCS.`;
            errorDiv.classList.remove('hidden');
            return;
        }

        const data = await response.json();
        displayResults(data.results);

    } catch (error) {
        // Manejo de errores de red (ej. servidor no está corriendo)
        loadingDiv.classList.add('hidden');
        errorDiv.textContent = `Error de conexión: ${error.message}. Asegúrate que el servidor de Django esté corriendo en ${API_URL}`;
        errorDiv.classList.remove('hidden');
    }
});

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    let htmlContent = '';

    // --- 1. Metadatos y Modelo Inicial (Todas las Características) ---
    htmlContent += `
        <h3>Metadatos y Modelo Inicial</h3>
        <p>Tamaño de Sets: ${results.train_size} (Entrenamiento) / ${results.validation_size} (Validación)</p>

        <h4>Métricas (Modelo con todas las características):</h4>
        <p><strong>F1 Score de Validación:</strong> <code>${results.f1_score_validation}</code></p>
        <p><strong>F1 Score de Entrenamiento:</strong> <code>${results.f1_score_training}</code></p>
        <hr>
    `;

    // --- 2. Top 10 Características ---
    htmlContent += '<h3>Top 10 Características + relevantes:</h3>';
    htmlContent += '<ol reversed>';
    results.top_10_features_desc.forEach((feature, index) => {
        htmlContent += `<li><strong>${feature}</strong></li>`;
    });
    htmlContent += '</ol>';

    // --- 3. Modelo Reducido ---
    htmlContent += `
        <hr>
        <h3>Resultados del modelo REDUCIDO (Solo Top 10)</h3>
        <p>F1 Score de Validación (Reducido): <code>${results.f1_score_validation_reduced}</code></p>
        <p>F1 Score de Entrenamiento (Reducido): <code>${results.f1_score_training_reduced}</code></p>
        <p class="nota"><em>El rendimiento se mantiene similar, demostrando la eficacia de la selección de características.</em></p>
        <hr>
    `;

    // --- 4. Todas las Características (para revisión) ---
    htmlContent += '<h3>Lista Completa de Features = Características (De - a + Importante):</h3>';
    htmlContent += '<ol>';
    results.features_asc.forEach(feature => {
        htmlContent += `<li>${feature}</li>`;
    });
    htmlContent += '</ol>';


    resultsDiv.innerHTML = htmlContent;
    resultsDiv.classList.remove('hidden');
}
