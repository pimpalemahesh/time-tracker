document.addEventListener('DOMContentLoaded', function() {
    // Initialize Select2
    if ($.fn.select2) {
        // For filter form
        $('#filterForm .select2').select2({
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: 'Select an option'
        });

        // For timer modal
        $('#timerModal .select2').select2({
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: 'Select an option',
            dropdownParent: $('#timerModal') // This is important!
        });
    }

    // Handle filter form submission
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        // Auto-submit on select change for FILTER form only
        $('#filterForm .select2, #filterForm select[name="date_range"]').on('change', function() {
            filterForm.submit();
        });
    }

    // Reset timer form when "Start Timer" button is clicked
    $('button[data-bs-toggle="modal"][data-bs-target="#timerModal"]').on('click', function() {
        const form = $('#timerModal form');
        // Reset the form
        form[0].reset();
        // Clear all Select2 fields
        form.find('select').each(function() {
            $(this).val(null).trigger('change');
        });
        // Clear the description field
        form.find('input[name="description"]').val('');
    });

    // Also reset when modal is shown (as a backup)
    $('#timerModal').on('show.bs.modal', function () {
        const form = $(this).find('form');
        // Reset the form
        form[0].reset();
        // Clear all Select2 fields
        form.find('select').each(function() {
            $(this).val(null).trigger('change');
        });
        // Clear the description field
        form.find('input[name="description"]').val('');
    });

    // Function to show alerts on the dashboard
    function showAlert(type, message) {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        const alertContainer = $('#alertContainer');
        alertContainer.html(alertHtml);
        
        // Only scroll if the alert container exists and is visible
        if (alertContainer.length && alertContainer.is(':visible')) {
            const offset = alertContainer.offset();
            if (offset) {
                $('html, body').animate({
                    scrollTop: offset.top - 20
                }, 200);
            }
        }

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            $('.alert').fadeOut('slow', function() {
                $(this).remove();
            });
        }, 5000);
    }

    // Handle timer form submission from the modal
    $('#timerModal form').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        const modal = $('#timerModal');
        
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                // Always close the modal
                modal.modal('hide');
                
                if (response.success) {
                    // Show success message and reload page
                    showAlert('success', response.message);
                    setTimeout(() => {
                        window.location.reload();
                    }, 500); // Small delay to ensure alert is shown
                } else {
                    // Show error message on dashboard
                    showAlert('warning', response.message || 'An error occurred');
                    // Clear the form
                    form[0].reset();
                    form.find('select').each(function() {
                        $(this).val(null).trigger('change');
                    });
                }
            },
            error: function() {
                modal.modal('hide');
                showAlert('danger', 'An error occurred while starting the timer');
            }
        });
    });

    // Handle company form submission
    $('#companyForm').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    // Add new option to company select in timer modal
                    const newOption = new Option(response.company.name, response.company.id, true, true);
                    $('#timerModal select[name="company"]').append(newOption).trigger('change');
                    
                    // Close modal
                    $('#companyModal').modal('hide');
                    
                    // Reset form
                    form[0].reset();
                    
                    // Show success message
                    showAlert('success', 'Company added successfully');
                } else {
                    showAlert('danger', response.message || 'An error occurred');
                }
            },
            error: function() {
                showAlert('danger', 'An error occurred while adding the company');
            }
        });
    });

    // Similar handlers for project and tag forms
    $('#projectForm').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    const newOption = new Option(response.project.name, response.project.id, true, true);
                    $('#timerModal select[name="project"]').append(newOption).trigger('change');
                    $('#projectModal').modal('hide');
                    form[0].reset();
                    showAlert('success', 'Project added successfully');
                } else {
                    showAlert('danger', response.message || 'An error occurred');
                }
            },
            error: function() {
                showAlert('danger', 'An error occurred while adding the project');
            }
        });
    });

    $('#tagForm').on('submit', function(e) {
        e.preventDefault();
        const form = $(this);
        
        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: form.serialize(),
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    const newOption = new Option(response.tag.name, response.tag.id, true, true);
                    $('#timerModal select[name="tags"]').append(newOption).trigger('change');
                    $('#tagModal').modal('hide');
                    form[0].reset();
                    showAlert('success', 'Tag added successfully');
                } else {
                    showAlert('danger', response.message || 'An error occurred');
                }
            },
            error: function() {
                showAlert('danger', 'An error occurred while adding the tag');
            }
        });
    });

    // Clear filters functionality
    $('#clearFilters').on('click', function(e) {
        e.preventDefault();
        window.location.href = window.location.pathname;
    });

    // Handle stop timer via AJAX
    $('.stop-timer').on('click', function(e) {
        e.preventDefault();
        const btn = $(this);
        const entryId = btn.data('entry-id');

        $.ajax({
            url: `/stop-timer/${entryId}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    // Update only the time entries table
                    $('#timeEntriesTable').html(response.html);
                    if (response.message) {
                        showAlert('success', response.message);
                    }
                } else {
                    showAlert('danger', response.message || 'An error occurred');
                }
            },
            error: function() {
                showAlert('danger', 'An error occurred while stopping the timer');
            }
        });
    });

    // Initialize timers
    initializeTimers();

    // Add confirmDelete function
    window.confirmDelete = function(deleteUrl) {
        const modal = $('#deleteConfirmModal');
        const confirmBtn = modal.find('#confirmDeleteBtn');
        
        // Set the delete URL
        confirmBtn.attr('href', deleteUrl);
        
        // Show the modal
        modal.modal('show');
        
        // Handle delete confirmation
        confirmBtn.one('click', function(e) {
            e.preventDefault();
            
            $.ajax({
                url: deleteUrl,
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    modal.modal('hide');
                    if (response.success) {
                        showAlert('success', 'Entry deleted successfully');
                        setTimeout(() => {
                            window.location.reload();
                        }, 500);
                    } else {
                        showAlert('danger', response.message || 'Failed to delete entry');
                    }
                },
                error: function() {
                    modal.modal('hide');
                    showAlert('danger', 'An error occurred while deleting the entry');
                }
            });
        });
    };

    // Clear the delete URL when the modal is hidden
    $('#deleteConfirmModal').on('hidden.bs.modal', function() {
        $(this).find('#confirmDeleteBtn').attr('href', '#').off('click');
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Timer initialization function
function initializeTimers() {
    const runningTimers = document.querySelectorAll('.running-timer');
    runningTimers.forEach(timer => {
        const startTime = new Date(timer.dataset.startTime).getTime();
        
        setInterval(() => {
            const now = new Date().getTime();
            const duration = now - startTime;
            
            const hours = Math.floor(duration / (1000 * 60 * 60));
            const minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
            
            timer.textContent = hours > 0 ? 
                `${hours}h ${minutes}m` : 
                `${minutes}m`;
        }, 60000); // Update every minute
    });
}