document.getElementById('weather-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const city = document.getElementById('city').value;
    const response = await fetch(`http://4.175.81.118:8000/weather-bulletin/${city}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (response.ok) {
        // Utilisez response.blob() pour traiter les données audio comme un blob
        const audioBlob = await response.blob();
        // Créez un objet URL pour le blob
        const audioUrl = URL.createObjectURL(audioBlob);
        // Créez un élément audio et définissez son source
        const audioElement = document.createElement('audio');
        audioElement.src = audioUrl;
        audioElement.controls = true; // Ajoutez des contrôles pour jouer/pause
        document.getElementById('audio-container').appendChild(audioElement); // Ajoutez l'élément audio au DOM
        audioElement.play(); // Commencez à jouer l'audio
    } else {
        alert('Erreur lors de la requête à l\'API.');
    }
});

