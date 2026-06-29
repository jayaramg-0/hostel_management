// Hostel Management System - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    var deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm || 'Are you sure?')) {
                e.preventDefault();
            }
        });
    });

    // Active sidebar link
    var currentPath = window.location.pathname;
    var sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
    sidebarLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentPath || 
            (currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
            link.classList.add('active');
        }
    });

    // Search form reset
    var searchResetBtns = document.querySelectorAll('.search-reset');
    searchResetBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var form = this.closest('form');
            form.querySelectorAll('input, select').forEach(function(input) {
                if (input.type === 'text' || input.type === 'search') {
                    input.value = '';
                } else if (input.tagName === 'SELECT') {
                    input.selectedIndex = 0;
                }
            });
            form.submit();
        });
    });

    // Print functionality
    var printBtns = document.querySelectorAll('.btn-print');
    printBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            window.print();
        });
    });

    // Date picker initialization (if using flatpickr)
    if (typeof flatpickr !== 'undefined') {
        flatpickr('input[type="date"]', {
            dateFormat: 'Y-m-d',
            allowInput: true
        });
    }

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Toggle sidebar on mobile
    var sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('show');
        });
    }

    // Data table search
    var tableSearch = document.getElementById('tableSearch');
    if (tableSearch) {
        tableSearch.addEventListener('keyup', function() {
            var filter = this.value.toLowerCase();
            var table = document.querySelector('.table tbody');
            var rows = table.querySelectorAll('tr');
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }

    // File input preview
    var fileInputs = document.querySelectorAll('input[type="file"][data-preview]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var preview = document.getElementById(this.dataset.preview);
            if (preview && this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // Notification badge update
    function updateNotificationBadge() {
        var badge = document.querySelector('.notification-badge');
        if (badge) {
            fetch('/api/notifications/count/')
                .then(response => response.json())
                .then(data => {
                    badge.textContent = data.count;
                    badge.style.display = data.count > 0 ? 'inline' : 'none';
                })
                .catch(err => console.log('Notification fetch error:', err));
        }
    }

    // Update notifications every 60 seconds
    setInterval(updateNotificationBadge, 60000);
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// AJAX CSRF setup for Django
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

const csrftoken = getCookie('csrftoken');

// Export functions
window.HMS = {
    formatCurrency: formatCurrency,
    formatDate: formatDate,
    csrftoken: csrftoken
};
