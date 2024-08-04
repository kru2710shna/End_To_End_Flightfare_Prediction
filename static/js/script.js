// Function to validate the flight booking form
function validateForm() {
    var departureDate = document.getElementById("departure-date").value;
    var arrivalDate = document.getElementById("arrival-date").value;
    var stops = document.getElementById("stops").value;
    var fromLocation = document.getElementById("from-location").value;
    var toLocation = document.getElementById("to-location").value;
    var airline = document.getElementById("airlines").value;

    // Check for missing values
    if (!departureDate || !arrivalDate || !stops || !fromLocation || !toLocation || !airline) {
        alert("Please fill out all fields.");
        return false;
    }

    // Check if departure and destination locations are the same
    if (fromLocation === toLocation) {
        alert("Departure and destination locations cannot be the same.");
        return false;
    }

    return true;
}

// Reset form fields on page reload/refresh
function resetForm() {
    document.getElementById("fare-form").reset();
}

// Handle form submission
function handleFormSubmit(event) {
    if (!validateForm()) {
        event.preventDefault(); // Prevent form submission
    }
}

// Handle scroll event
function handleScroll() {
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
}

// Consolidate all initializations in one window.onload
window.onload = function() {
    resetForm();
};

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('#fare-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

window.addEventListener('scroll', handleScroll);
