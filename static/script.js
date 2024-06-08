async function convertTextToSpeech() {
    const text = document.getElementById('text-input').value;
    const button = document.getElementById('convert-btn');
    const downloadLink = document.getElementById('download-link');
    const audioPlayer = document.getElementById('audio-player');

    if (!text) {
        alert('Please enter some text.');
        return;
    }

    button.disabled = true;
    button.textContent = 'Converting...';

    try {
        const response = await fetch('/generate_tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error('Failed to convert text to speech');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Set up the audio player
        audioPlayer.src = url;
        audioPlayer.style.display = 'block';
        audioPlayer.play();

        // Set up the download link
        downloadLink.href = url;
        downloadLink.download = 'speech.wav';
        downloadLink.style.display = 'block';
        downloadLink.textContent = 'Download Audio';
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        button.disabled = false;
        button.textContent = 'Convert to Speech';
    }
}