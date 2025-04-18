// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Initialize date pickers if any
    if (typeof flatpickr !== 'undefined') {
        flatpickr('.datepicker', {
            dateFormat: 'Y-m-d',
            minDate: 'today'
        });
        
        flatpickr('.timepicker', {
            enableTime: true,
            noCalendar: true,
            dateFormat: 'H:i',
            time_24hr: true
        });
    }
});

// Appointment booking form
const doctorSelect = document.getElementById('doctor_id');
if (doctorSelect) {
    doctorSelect.addEventListener('change', function() {
        // Here you could add AJAX to fetch available time slots for the selected doctor
        console.log('Selected doctor ID:', this.value);
    });
}

// Confirmation dialogs
const confirmButtons = document.querySelectorAll('.confirm-action');
confirmButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        if (!confirm('Are you sure you want to perform this action?')) {
            event.preventDefault();
        }
    });
});