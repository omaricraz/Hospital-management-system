document.addEventListener('DOMContentLoaded', function() {
    // ... (keep all your existing code except the form submission part)

    // Real form submission handling with loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"], .submit-btn');
            if (!submitBtn) return;
            
            const originalBtnText = submitBtn.innerHTML;
            const formAction = form.getAttribute('action') || window.location.pathname;
            
            try {
                // Show loading state
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.innerHTML = `
                    <span class="btn-loader"></span>
                    Sending...
                `;
                
                // Collect form data
                const formData = new FormData(form);
                
                // Add CSRF token if not present
                if (!formData.has('csrfmiddlewaretoken')) {
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                    if (csrfToken) formData.append('csrfmiddlewaretoken', csrfToken);
                }
                
                // Send to Django backend
                const response = await fetch(formAction, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                // Handle response
                let data;
                try {
                    data = await response.json();
                } catch (error) {
                    throw new Error('Invalid server response');
                }
                
                if (!response.ok) {
                    throw new Error(data.error || data.message || 'Form submission failed');
                }
                
                // Success handling
                showFormMessage(form, data.message || 'Message sent successfully!', 'success');
                form.reset();
                
            } catch (error) {
                // Error handling
                showFormMessage(form, error.message, 'error');
                console.error('Form submission error:', error);
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
                submitBtn.innerHTML = originalBtnText;
            }
        });
    });
    
    // Helper function to show form messages
    function showFormMessage(form, message, type) {
        // Remove existing messages
        const existingMessages = form.querySelectorAll('.form-message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `form-message ${type}`;
        messageDiv.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            ${message}
        `;
        
        // Insert message
        form.insertBefore(messageDiv, form.firstChild);
        
        // Scroll to message
        messageDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.style.opacity = '0';
            setTimeout(() => messageDiv.remove(), 300);
        }, 5000);
    }
    
    // ... (rest of your existing code)
});