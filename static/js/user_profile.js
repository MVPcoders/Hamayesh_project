// مدیریت مودال ویرایش مقاله
document.addEventListener('DOMContentLoaded', function () {
    // دکمه‌های ویرایش
    const editButtons = document.querySelectorAll('button:has(i.fa-edit)');

    // عناصر مودال
    const editModal = document.getElementById('editModal');
    const closeEditModal = document.getElementById('closeEditModal');
    const cancelEdit = document.getElementById('cancelEdit');

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
            // نمایش مودال
            editModal.style.display = 'flex';

        });
    });

    // بستن مودال با دکمه بستن
    closeEditModal.addEventListener('click', function () {
        editModal.style.display = 'none';
        document.getElementById('newFile').value = '';
    });

    // بستن مودال با دکمه انصراف
    cancelEdit.addEventListener('click', function () {
        editModal.style.display = 'none';
        document.getElementById('newFile').value = '';
    });

    // بستن مودال با کلیک خارج از آن
    editModal.addEventListener('click', function (e) {
        if (e.target === editModal) {
            editModal.style.display = 'none';
            document.getElementById('newFile').value = '';
        }
    });

    // ارسال فرم ویرایش
    document.getElementById('articleForm').addEventListener('submit', function (e) {
        e.preventDefault();
        //
        const formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
        })
            .then(response => response.json())
            .then(data => {
                editModal.style.display = 'none';
                if (data.status === 'success') {
                    Swal.fire({
                        title: 'موفقیت آمیز!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'باشه!',
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
                        timer: 3000, // 3 ثانیه
                        timerProgressBar: true
                    });
                    document.getElementById('newFile').value = '';
                }
            })
            .catch(error => {
                editModal.style.display = 'none';
                Swal.fire({
                    title: 'خطا!',
                    text: 'خطایی در ارتباط با سرور رخ داده است.',
                    icon: 'error',
                    confirmButtonText: 'متوجه شدم',
                    timer: 3000, // 3 ثانیه
                    timerProgressBar: true
                });
                document.getElementById('newFile').value = '';
            });
    });
});


// Add animation to article cards when they come into view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {threshold: 0.1});

document.querySelectorAll('.article-card').forEach(card => {
    card.style.opacity = 0;
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
});


