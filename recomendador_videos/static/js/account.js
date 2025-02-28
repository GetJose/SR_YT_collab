document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('.interest-category > label > input');

    categories.forEach(input => {
        const subInterests = input.closest('.interest-category').querySelector('.sub-interests');

        if (subInterests) {
            const checkSubInterests = () => {
                const anyChildChecked = Array.from(subInterests.querySelectorAll('input')).some(child => child.checked);
                subInterests.style.display = (input.checked || anyChildChecked) ? 'block' : 'none';
            };

            checkSubInterests();

            input.addEventListener('change', checkSubInterests);

            subInterests.querySelectorAll('input').forEach(subInput => {
                subInput.addEventListener('change', checkSubInterests);
            });
        }
    });

    const clearButton = document.getElementById('clear-selection');
    if (clearButton) {
        clearButton.addEventListener('click', function () {
            const checkboxes = document.querySelectorAll('form input[type="checkbox"]');

            checkboxes.forEach(input => input.checked = false);

            document.querySelectorAll('.sub-interests').forEach(subInterests => subInterests.style.display = 'none');

            checkboxes.forEach(input => input.removeAttribute('checked'));
        });
    }
});
