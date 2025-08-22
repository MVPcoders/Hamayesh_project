// to get current year
// function getYear() {
//     var currentDate = new Date();
//     var currentYear = currentDate.getFullYear();
//     document.querySelector("#displayYear").innerHTML = currentYear;
// }
//
// getYear();


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


// // اسکرول خودکار
// window.addEventListener('load', () => {
// window.scrollTo({top: 500, behavior: 'smooth'});
// });


// اسکرول خودکار بخش ورود به هنگام خطا
document.addEventListener('DOMContentLoaded', function () {
    // چک کنیم آیا خطایی وجود دارد (با توجه به ساختار ارورهای شما)
    const errorMessages = document.querySelectorAll('form p');
    const hasErrors = Array.from(errorMessages).some(p => p.textContent.trim().startsWith('*'));

    // یا اگر URL شامل هاف باشد
    const hash = window.location.hash;

    if (hash === '#signin_container1' || hasErrors) {
        const element = document.getElementById('signin_container1');
        if (element) {
            setTimeout(() => {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start' // برای تراز بهتر
                });
            }, 100);
        }
    }
});


// اسکرول خودکار بخش ثبت نام به هنگام خطا
document.addEventListener('DOMContentLoaded', function () {
    // چک کنیم آیا خطایی وجود دارد (با توجه به ساختار ارورهای شما)
    const errorMessages = document.querySelectorAll('form p');
    const hasErrors = Array.from(errorMessages).some(p => p.textContent.trim().startsWith('*'));

    // یا اگر URL شامل هاف باشد
    const hash = window.location.hash;

    if (hash === '#signup_container1' || hasErrors) {
        const element = document.getElementById('signup_container1');
        if (element) {
            setTimeout(() => {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start' // برای تراز بهتر
                });
            }, 100);
        }
    }
});


// نمایش پیام های  toast
document.addEventListener('DOMContentLoaded', function () {
    const toastMessages = document.querySelectorAll('.toast-message');

    toastMessages.forEach(message => {
        // تعیین نوع Toast بر اساس تگ پیغام
        let toastType = 'success';
        if (message.dataset.type === 'error') {
            toastType = 'error';
        }

        // ایجاد عنصر Toast
        const toast = document.createElement('div');
        toast.className = `toast ${toastType}`;

        // تعیین آیکون بر اساس نوع پیغام
        const icon = toastType === 'success' ? '✓' : '✗';

        // محتوای Toast
        toast.innerHTML = `
            <span class="toast-icon">${icon}</span>
            <span class="toast-text">${message.textContent}</span>
        `;

        // اضافه کردن Toast به صفحه
        document.body.appendChild(toast);

        // نمایش Toast با تأخیر
        setTimeout(() => toast.classList.add('show'), 100);


        // بستن خودکار پس از 3 ثانیه
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }, 3000);
    });
});

/*new header style***********************************************************************************************/

// اسکریپت کنترل منو
document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');

    // باز کردن منو
    menuToggle.addEventListener('click', function () {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // بستن منو با کلیک روی overlay
    overlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // بستن منو با اسکرول (اختیاری)
    window.addEventListener('scroll', function () {
        if (sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }
    });
});

function updateMenuToggle() {
    document.getElementById("menu-toggle").style.display =
        window.matchMedia('(max-width: 990px)').matches ? "block" : "none";
}

// اجرای اولیه
updateMenuToggle();

// گوش دادن به تغییر سایز
window.addEventListener('resize', updateMenuToggle);



