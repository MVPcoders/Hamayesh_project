// مدیریت مودال ویرایش مقاله
document.addEventListener('DOMContentLoaded', function() {
    // دکمه‌های ویرایش
    const editButtons = document.querySelectorAll('button:has(i.fa-edit)');

    // عناصر مودال
    const editModal = document.getElementById('editModal');
    const closeEditModal = document.getElementById('closeEditModal');
    const cancelEdit = document.getElementById('cancelEdit');

    // برای هر دکمه ویرایش رویداد کلیک اضافه می‌کنیم
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
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
    closeEditModal.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    // بستن مودال با دکمه انصراف
    cancelEdit.addEventListener('click', function() {
        editModal.style.display = 'none';
    });

    // بستن مودال با کلیک خارج از آن
    editModal.addEventListener('click', function(e) {
        if (e.target === editModal) {
            editModal.style.display = 'none';
        }
    });

    // ارسال فرم ویرایش
    // document.getElementById('editArticleForm').addEventListener('submit', function(e) {
    //     e.preventDefault();
    //
    //     // اینجا کدهای ارسال فرم به سرور را اضافه کنید
    //     // ...
    //
    //     // بعد از ارسال موفق، مودال را ببندید
    //     editModal.style.display = 'none';
    //
    //     // پیام موفقیت آمیز نمایش دهید
    //     alert('تغییرات با موفقیت ذخیره شدند.');
    // });
});


// Add animation to article cards when they come into view
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.article-card').forEach(card => {
    card.style.opacity = 0;
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.6s ease';
    observer.observe(card);
});

