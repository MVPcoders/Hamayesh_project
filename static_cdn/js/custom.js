// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


// آشکار و پنهان کردن رمز عبور
document.addEventListener('DOMContentLoaded', function () {
    const toggleButtons = document.querySelectorAll('.toggle-password');

    toggleButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const passwordField = this.previousElementSibling; // فیلد رمز قبل از آیکون
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);

            // تغییر آیکون
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });
});

//  رسید بخش تعرفه ها
function updateReceipt() {
    let total = 0;
    const receiptItems = document.getElementById('receipt-items');
    receiptItems.innerHTML = ''; // Clear previous items

    // Get selected radio button
    const selectedRadio = document.querySelector('input[name="quantum"]:checked');
    if (selectedRadio) {
        const radioPrice = parseFloat(selectedRadio.value) || 0;
        total += radioPrice;

        // Get label: the span with class "radio-label" inside the parent label element
        const radioLabelSpan = selectedRadio.closest('label').querySelector('.radio-label');
        const radioLabel = radioLabelSpan ? radioLabelSpan.innerText : "محصول رادیو";

        const radioRow = `<tr><td>${radioLabel}</td><td>${radioPrice.toLocaleString()} تومان</td></tr>`;
        receiptItems.innerHTML += radioRow;
    }

    // Get checked checkboxes
    const checkboxes = document.querySelectorAll('.cyberpunk-checkbox:checked');
    checkboxes.forEach(checkbox => {
        const checkboxPrice = parseFloat(checkbox.value) || 0;
        total += checkboxPrice;

        // Get label text: the text content of the label, excluding the input element
        const labelElement = checkbox.closest('label');
        let labelText = "";
        if (labelElement) {
            // Clone to manipulate without altering DOM
            const clonedLabel = labelElement.cloneNode(true);
            // Remove input element from clone
            const inputElement = clonedLabel.querySelector('input');
            if (inputElement) clonedLabel.removeChild(inputElement);
            labelText = clonedLabel.textContent.trim() || "محصول چک باکس";
        } else {
            labelText = "محصول چک باکس";
        }

        const checkboxRow = `<tr><td>${labelText}</td><td>${checkboxPrice.toLocaleString()} تومان</td></tr>`;
        receiptItems.innerHTML += checkboxRow;
    });

    // Update total price

    document.getElementById('total-price').innerText = total.toLocaleString() + ' تومان';
}


    // اسکرول خودکار
    // window.addEventListener('load', () => {
    // window.scrollTo({top: 500, behavior: 'smooth'});
    // });
