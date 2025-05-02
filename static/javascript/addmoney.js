
document.addEventListener('DOMContentLoaded', function() {
    const incomeRadio = document.getElementById('add_income');
    const expenseRadio = document.getElementById('add_expense');
    const categorySelect = document.getElementById('categorySelect');

    function toggleCategoryField() {
        if (incomeRadio.checked) {
            categorySelect.disabled = true;
            categorySelect.removeAttribute('required');
        } else {
            categorySelect.disabled = false;
            categorySelect.setAttribute('required', 'required');
        }
    }

    if (incomeRadio && expenseRadio && categorySelect) {
        incomeRadio.addEventListener('change', toggleCategoryField);
        expenseRadio.addEventListener('change', toggleCategoryField);
        toggleCategoryField(); // run on load
    }
});
