// Timer functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Select2
    if ($.fn.select2) {
        $('.select2').select2({
            theme: 'bootstrap-5'
        });
    }

    // Delete confirmation
    window.confirmDelete = function(url) {
        if (confirm('Are you sure you want to delete this entry?')) {
            window.location.href = url;
        }
    };
}); 