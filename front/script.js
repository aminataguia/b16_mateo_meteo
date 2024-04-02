document.getElementById('weather-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const city = document.getElementById('city').value;
    const response = await fetch(`http://localhost:8001/weather-bulletin/${city}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (response.ok) {
        const data = await response.json();
        if (data.message) {
            alert(data.message);
            // Assuming the audio file is saved locally and accessible
            const audioElement = document.createElement('audio');
            audioElement.src = "audio.mp3";
            audioElement.controls = true;
            document.getElementById('audio-container').appendChild(audioElement);
        } else {
            alert('Erreur lors de la génération du fichier audio.');
        }
    } else {
        alert('Erreur lors de la requête à l\'API.');
    }
});
