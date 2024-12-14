document.addEventListener('DOMContentLoaded', function () {
    const profileForm = document.getElementById('profileForm');

    profileForm.addEventListener('submit', function (e) {
        e.preventDefault(); 

        const formData = new FormData(profileForm);

        fetch(profileForm.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert('Profile updated successfully!');
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(() => {
                alert('An unexpected error occurred. Please try again.');
            });
    });
});
