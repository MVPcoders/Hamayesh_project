  function updateAuthorForms() {
            const authorCount = parseInt(document.getElementById('authorCount').value);
            const authorsContainer = document.getElementById('authorsContainer');

            // Limit the maximum number of authors
            if (authorCount > 4) {
                alert('حداکثر تعداد نویسندگان 4 نفر می‌باشد');
                document.getElementById('authorCount').value = 4;
                return;
            }

            // Clear existing author forms
            authorsContainer.innerHTML = '';

            // Create new author forms with different colors
            const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

            for (let i = 0; i < authorCount; i++) {
                const authorForm = document.createElement('div');
                authorForm.className = 'author-form animate-fade-in';
                authorForm.style.borderLeftColor = colors[i];

                authorForm.innerHTML = `
                    <div class="author-form-header">
                        <h4 class="author-form-title" style="color: ${colors[i]}">نویسنده ${i + 1}</h4>
                        ${i > 0 ? `<button type="button" class="remove-author" style="background-color: ${colors[i]}" onclick="removeAuthorForm(this)">حذف نویسنده</button>` : ''}
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-group">
                            <label for="authorFirstName${i}" class="form-label">نام</label>
                            <input type="text" id="authorFirstName${i}" name="authorFirstName${i}" class="form-input" required>
                        </div>

                        <div class="form-group">
                            <label for="authorLastName${i}" class="form-label">نام خانوادگی</label>
                            <input type="text" id="authorLastName${i}" name="authorLastName${i}" class="form-input" required>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="form-group">
                            <label for="authorEmail${i}" class="form-label">ایمیل</label>
                            <input type="email" id="authorEmail${i}" name="authorEmail${i}" class="form-input" required>
                        </div>
                        <div class="form-group">
                            <label for="authorCodemeli${i}" class="form-label">کدملی</label>
                            <input type="text"
                               id="authorCodemeli${i}"
                               name="authorCodemeli${i}"
                               class="form-input"
                               required
                               oninput="validateNationalId(this)">
                            <div id="nationalIdError${i}" class="text-red-500 text-sm mt-1 hidden">کدملی وارد شده کمتر از 10 رقم است.</div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                        <div class="form-group">
                            <label class="form-label">نویسنده مسئول</label>
                            <div class="flex items-center mt-2">
                                <input type="radio" id="correspondingAuthor${i}" name="correspondingAuthor" value="${i}" ${i === 0 ? 'checked' : ''}>
                                <label for="correspondingAuthor${i}" class="mr-2">این نویسنده مسئول مکاتبات است</label>
                            </div>
                        </div>
                    </div>
                `;

                authorsContainer.appendChild(authorForm);
            }
        }

        function removeAuthorForm(button) {
            const authorForm = button.closest('.author-form');
            const authorsContainer = document.getElementById('authorsContainer');
            const authorForms = authorsContainer.querySelectorAll('.author-form');

            // Don't allow removing if only one author remains
            if (authorForms.length <= 1) {
                alert('مقاله باید حداقل یک نویسنده داشته باشد');
                return;
            }

            authorForm.classList.add('animate__animated', 'animate__fadeOut');

            setTimeout(() => {
                authorForm.remove();
                // Update count input
                document.getElementById('authorCount').value = authorForms.length - 1;
            }, 500);
        }

        // Initialize with one author form
        document.addEventListener('DOMContentLoaded', updateAuthorForms);

        // Upload file functionality
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('articleFile');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const uploadSuccess = document.getElementById('uploadSuccess');
        const progressBar = document.getElementById('progressBar');

        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFileUpload();
            }
        });

        // Click event
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // File input change event
        fileInput.addEventListener('change', handleFileUpload);

        function handleFileUpload() {
            const file = fileInput.files[0];
            if (!file) return;

            // Reset previous state
            fileInfo.style.display = 'none';
            uploadSuccess.style.display = 'none';

            // Validate file size (5MB max)
            if (file.size > 5 * 1024 * 1024) {
                alert('حجم فایل باید کمتر از 5MB باشد');
                fileInput.value = '';
                return;
            }

            // Validate file type (ONLY Word files)
            const validTypes = [
                'application/msword', // برای doc
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document' // برای docx
            ];

            if (!validTypes.includes(file.type)) {
                alert('فقط فایل‌های Word (doc و docx) قابل قبول هستند');
                fileInput.value = '';
                return;
            }

            // Additional check for file extension (for extra security)
            const fileExtension = file.name.split('.').pop().toLowerCase();
            if (!['doc', 'docx'].includes(fileExtension)) {
                alert('فقط فایل‌های با پسوند .doc یا .docx قابل قبول هستند');
                fileInput.value = '';
                return;
            }

            // Show file info
            fileName.textContent = file.name;
            fileInfo.style.display = 'flex';

            // Only show success after upload simulation
            simulateUploadProgress(() => {
                uploadSuccess.style.display = 'block';
            });
        }

        function simulateUploadProgress() {
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 10;
                if (progress >= 100) {
                    progress = 100;
                    clearInterval(interval);
                    uploadSuccess.style.display = 'block';
                }
                progressBar.style.width = `${progress}%`;
            }, 200);
        }
        // کنترل ارسال مقاله
        document.getElementById('articleForm').addEventListener('submit', function(e) {
            e.preventDefault();


            const submitButton = document.getElementById('submitButton');
            const loadingMessage = document.getElementById('loadingMessage');
            submitButton.classList.add('hidden');
            loadingMessage.classList.remove('hidden');
            loadingMessage.classList.add('flex');

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
                if (data.status === 'success') {
                    Swal.fire({
                        title: 'موفقیت آمیز!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'باشه',
                        timer: 3000,
                        timerProgressBar: true,
                        willClose: () => {
                            window.location.href = '/profile';
                        }
                    });
                } else {

                    submitButton.classList.remove('hidden');
                    loadingMessage.classList.add('hidden');
                    loadingMessage.classList.remove('flex');

                    Swal.fire({
                        title: 'خطا!',
                        text: data.message,
                        icon: 'error',
                        confirmButtonText: 'متوجه شدم',
                        timer: 3000,
                        timerProgressBar: true
                    });
                }
            })
            .catch(error => {

                submitButton.classList.remove('hidden');
                loadingMessage.classList.add('hidden');
                loadingMessage.classList.remove('flex');

                Swal.fire({
                    title: 'خطا!',
                    text: 'خطایی در ارتباط با سرور رخ داده است.',
                    icon: 'error',
                    confirmButtonText: 'متوجه شدم',
                    timer: 3000,
                    timerProgressBar: true
                });
            });
        });
        // code melli error
        function validateNationalId(input) {
          const errorElement = document.getElementById(`nationalIdError${input.id.replace('authorCodemeli', '')}`);
          input.value = input.value.replace(/[^0-9]/g, '');

          if (input.value.length > 10) {
            input.value = input.value.slice(0, 10);
          }

          errorElement.classList.toggle('hidden', input.value.length === 10);
        }