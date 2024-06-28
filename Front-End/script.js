window.addEventListener('scroll', function() {
    var formContainer = document.getElementById('form-container');
    var contentPosition = document.getElementById('content').getBoundingClientRect().bottom;
    var formPosition = formContainer.getBoundingClientRect().top;
    var windowHeight = window.innerHeight;

    if (contentPosition < windowHeight && formPosition > windowHeight) {
        formContainer.style.display = 'block';
        setTimeout(function() {
            formContainer.style.opacity = 1;
        }, 100);
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

    // Initialize date pickers
    document.getElementById('departure-date').addEventListener('click', function() {
        showDatePicker(this);
    });

    document.getElementById('arrival-date').addEventListener('click', function() {
        showDatePicker(this);
    });

    function showDatePicker(input) {
        var datePicker = document.createElement('div');
        datePicker.className = 'date-picker';
        datePicker.innerHTML = `
            <div class="date-picker-header">
                <button class="date-picker-btn today-btn">Today</button>
                <button class="date-picker-btn close-btn">Close</button>
            </div>
            <div class="date-picker-body">
                <div class="date-picker-section">
                    <label>Day</label>
                    <select class="day-select">${generateOptions(1, 31)}</select>
                </div>
                <div class="date-picker-section">
                    <label>Month</label>
                    <select class="month-select">${generateOptions(1, 12)}</select>
                </div>
                <div class="date-picker-section">
                    <label>Year</label>
                    <select class="year-select">${generateOptions(2020, 2030)}</select>
                </div>
            </div>
        `;

        input.parentNode.appendChild(datePicker);

        datePicker.querySelector('.today-btn').addEventListener('click', function() {
            var today = new Date();
            input.value = formatDate(today);
            datePicker.remove();
        });

        datePicker.querySelector('.close-btn').addEventListener('click', function() {
            datePicker.remove();
        });

        datePicker.querySelectorAll('select').forEach(function(select) {
            select.addEventListener('change', function() {
                var day = datePicker.querySelector('.day-select').value;
                var month = datePicker.querySelector('.month-select').value;
                var year = datePicker.querySelector('.year-select').value;
                var date = new Date(year, month - 1, day);
                input.value = formatDate(date);
            });
        });
    }

    function generateOptions(start, end) {
        var options = '';
        for (var i = start; i <= end; i++) {
            options += `<option value="${i}">${i}</option>`;
        }
        return options;
    }

    function formatDate(date) {
        var day = ('0' + date.getDate()).slice(-2);
        var month = ('0' + (date.getMonth() + 1)).slice(-2);
        var year = date.getFullYear();
        return `${day}/${month}/${year}`;
    }
});
