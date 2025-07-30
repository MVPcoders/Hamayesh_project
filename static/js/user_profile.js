
// فعال کردن تب‌ها
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('[data-tabs-toggle] button');
    const tabContents = document.querySelectorAll('#myTabContent > div');

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // حذف کلاس active از همه تب‌ها
            tabs.forEach(t => {
                t.classList.remove('active', 'text-purple-600');
                t.classList.add('text-gray-600');
            });
            tabContents.forEach(c => c.classList.add('hidden'));

            // اضافه کردن کلاس active به تب انتخاب شده
            this.classList.add('active', 'text-purple-600');
            this.classList.remove('text-gray-600');

            // نمایش محتوای تب مربوطه
            const targetId = this.getAttribute('data-tabs-target');
            document.querySelector(targetId).classList.remove('hidden');
        });
    });

    // نمایش نام فایل انتخاب شده برای تیکت
    const ticketFileInput = document.querySelector('#id_attachment');
    const ticketFileName = document.querySelector('#ticketFileName');

    if (ticketFileInput) {
        ticketFileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                ticketFileName.textContent = this.files[0].name;
            } else {
                ticketFileName.textContent = 'هیچ فایلی انتخاب نشده';
            }
        });
    }

    // نمایش نام فایل انتخاب شده برای مقاله
    const articleFileInput = document.querySelector('#newFile');
    const articleFileName = document.querySelector('#fileNameDisplay');

    if (articleFileInput) {
        articleFileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                articleFileName.textContent = this.files[0].name;
            } else {
                articleFileName.textContent = 'هیچ فایلی انتخاب نشده';
            }
        });
    }
});

// مدیریت مودال ویرایش مقاله
document.addEventListener('DOMContentLoaded', function () {
    // دکمه‌های ویرایش
    const editButtons = document.querySelectorAll('.edit-article-btn');

    // عناصر مودال
    const editModal = document.getElementById('editModal');
    const closeEditModal = document.getElementById('closeEditModal');
    const cancelEdit = document.getElementById('cancelEdit');
    const submitBtn = document.querySelector('#articleForm button[type="submit"]');
    const submitText = document.getElementById('submitText');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // برای هر دکمه ویرایش رویداد کلیک اضافه می‌کنیم
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            document.getElementById('articleId').value = this.getAttribute('data-article-id');
            document.getElementById('editPersianTitle').value = this.getAttribute('data-persian-title');
            document.getElementById('editEnglishTitle').value = this.getAttribute('data-english-title');
            document.getElementById('editLanguage').value = this.getAttribute('data-language');
            document.getElementById('editMainGoal').value = this.getAttribute('data-main-goal');
            document.getElementById('editAbstract').value = this.getAttribute('data-abstract');
            document.getElementById('FileName').innerText = this.getAttribute('data-file-name');
            document.getElementById('fileUrl').href = this.getAttribute('data-file-url');
            document.getElementById('fileUrl').setAttribute('download', this.getAttribute('data-file-name'));
            document.getElementById('fileNameDisplay').textContent = 'هیچ فایلی انتخاب نشده';

            // نمایش مودال
            editModal.style.display = 'flex';
            setTimeout(() => {
                editModal.classList.add('active');
            }, 10);
        });
    });

    // بستن مودال با دکمه بستن
    closeEditModal.addEventListener('click', function () {
        editModal.classList.remove('active');
        setTimeout(() => {
            editModal.style.display = 'none';
        }, 300);
        document.getElementById('newFile').value = '';
    });

    // بستن مودال با دکمه انصراف
    cancelEdit.addEventListener('click', function () {
        editModal.classList.remove('active');
        setTimeout(() => {
            editModal.style.display = 'none';
        }, 300);
        document.getElementById('newFile').value = '';
    });

    // بستن مودال با کلیک خارج از آن
    editModal.addEventListener('click', function (e) {
        if (e.target === editModal) {
            editModal.classList.remove('active');
            setTimeout(() => {
                editModal.style.display = 'none';
            }, 300);
            document.getElementById('newFile').value = '';
        }
    });

    // ارسال فرم ویرایش
    document.getElementById('articleForm').addEventListener('submit', function (e) {
        e.preventDefault();
        // نمایش اسپینر لودینگ
        submitText.textContent = 'در حال ذخیره...';
        loadingSpinner.classList.remove('hidden');
        submitBtn.disabled = true;

        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => response.json())
            .then(data => {
                // مخفی کردن اسپینر لودینگ
                submitText.textContent = 'ذخیره تغییرات';
                loadingSpinner.classList.add('hidden');
                submitBtn.disabled = false;

                editModal.classList.remove('active');
                setTimeout(() => {
                    editModal.style.display = 'none';
                }, 300);

                if (data.status === 'success') {
                    Swal.fire({
                        title: 'موفقیت آمیز!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'باشه',
                        timer: 3000,
                        timerProgressBar: true,
                        willClose: () => {
                            document.getElementById('newFile').value = '';
                            window.location.reload();
                        }
                    });
                } else {
                    Swal.fire({
                        title: 'خطا!',
                        text: data.message,
                        icon: 'error',
                        confirmButtonText: 'متوجه شدم',
                        timer: 3000,
                        timerProgressBar: true
                    });
                    document.getElementById('newFile').value = '';
                }
            })
            .catch(error => {
                // مخفی کردن اسپینر لودینگ
                submitText.textContent = 'ذخیره تغییرات';
                loadingSpinner.classList.add('hidden');
                submitBtn.disabled = false;

                editModal.classList.remove('active');
                setTimeout(() => {
                    editModal.style.display = 'none';
                }, 300);

                Swal.fire({
                    title: 'خطا!',
                    text: 'خطایی در ارتباط با سرور رخ داده است.',
                    icon: 'error',
                    confirmButtonText: 'متوجه شدم',
                    timer: 3000,
                    timerProgressBar: true
                });
                document.getElementById('newFile').value = '';
            });
    });
});

// انیمیشن برای کارت‌ها هنگام نمایش
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {threshold: 0.1});

document.querySelectorAll('.article-card').forEach((card, index) => {
    card.style.opacity = 0;
    card.style.transform = 'translateY(20px)';
    card.style.transition = `all 0.6s ease ${index * 0.1}s`;
    observer.observe(card);
});


// نمایش پیام های  toast
document.addEventListener('DOMContentLoaded', function() {
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


// حذف مقاله
document.querySelectorAll('.delete-article-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const articleId = this.getAttribute('data-article-id');
        const articleTitle = this.getAttribute('data-article-title');

        Swal.fire({
            title: 'حذف مقاله',
            text: `آیا از حذف مقاله "${articleTitle}" مطمئن هستید؟`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'بله، حذف شود',
            cancelButtonText: 'انصراف',
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                // ارسال درخواست حذف به سرور با متد GET
                fetch(`/delete-article/${articleId}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('خطا در پاسخ سرور');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        Swal.fire({
                            title:'حذف شد!',
                            text:'مقاله با موفقیت حذف شد.',
                            icon:'success',
                            confirmButtonText:'باشه'
                        }).then(() => {
                            window.location.reload();
                        });
                    } else {
                        Swal.fire(
                            'خطا!',
                            data.message || 'خطایی در حذف مقاله رخ داد.',
                            'error'
                        );
                    }
                })
                .catch(error => {
                    Swal.fire(
                        'خطا!',
                        'خطایی در ارتباط با سرور رخ داد: ' + error.message,
                        'error'
                    );
                });
            }
        });
    });
});