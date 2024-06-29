window.addEventListener('scroll', function() {
    var content = document.getElementById('content');
    var videoContainer = document.querySelector('.video-container');

    if (!content || !videoContainer) return;

    var contentRect = content.getBoundingClientRect();
    var videoRect = videoContainer.getBoundingClientRect();

    if (contentRect.top < videoRect.bottom && contentRect.bottom > videoRect.top) {
        content.style.zIndex = 1; // Content goes under video container
    } else {
        content.style.zIndex = 2; // Content stays above video container
    }
});

document.getElementById('fare-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData(event.target);
    var data = {
        departureDate: formData.get('departure-date'),
        arrivalDate: formData.get('arrival-date'),
        fromLocation: formData.get('from-location'),
        toLocation: formData.get('to-location'),
        stops: formData.get('stops'),
        airlines: formData.get('airlines')
    };

    fetch('/predict-fare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('prediction-result').innerText = 'Predicted Fare: ' + result.fare;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('prediction-result').innerText = 'An error occurred. Please try again.';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize moving text
    var movingTextContainer = document.querySelector('.moving-text');
    var text = movingTextContainer.textContent;
    movingTextContainer.innerHTML = '';

    for (let i = 0; i < 3; i++) {
        let span = document.createElement('span');
        span.textContent = text;
        span.style.animationDelay = (i * 3) + 's';
        movingTextContainer.appendChild(span);
    }
});
