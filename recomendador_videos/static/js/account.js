document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('.interest-category > label > input');

    categories.forEach(input => {
        const subInterests = input.closest('.interest-category').querySelector('.sub-interests');

        if (subInterests) {
            subInterests.style.display = input.checked ? 'block' : 'none';

            input.addEventListener('change', function() {
                if (input.checked) {
                    subInterests.style.display = 'block';
                } else {
                    const anyChildChecked = Array.from(subInterests.querySelectorAll('input')).some(child => child.checked);
                    if (!anyChildChecked) {
                        subInterests.style.display = 'none';
                        subInterests.querySelectorAll('input').forEach(subInput => subInput.checked = false);
                    }
                }
            });
        }
    });

    const clearButton = document.getElementById('clear-selection');
    if (clearButton) {
        clearButton.addEventListener('click', function () {
            document.querySelectorAll('#interest-form input[type="checkbox"]').forEach(input => input.checked = false);
            document.querySelectorAll('.sub-interests').forEach(subInterests => subInterests.style.display = 'none');
        });
    }
});
