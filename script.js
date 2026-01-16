document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const modal = document.getElementById('contactModal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.querySelector('.close-btn');
    const quoteForm = document.getElementById('quoteForm');

    // Functions
    const openModal = () => {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    };

    const closeModal = () => {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    };

    // Event Listeners
    openBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
    });

    closeBtn.addEventListener('click', closeModal);

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Form Submission Logic (Updated for Formspree)
    quoteForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Button Loading State
        const submitBtn = quoteForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerText;
        submitBtn.innerText = '전송 중...';
        submitBtn.disabled = true;

        // Collect Form Data
        const formData = new FormData(quoteForm);

        // Send to Formspree
        fetch("https://formspree.io/f/mvzzgjrz", {
            method: "POST",
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                // Success Feedback
                alert("견적 문의가 성공적으로 접수되었습니다!\n빠른 시일 내에 연락드리겠습니다.");
                quoteForm.reset();
                closeModal();
            } else {
                // Error Feedback
                response.json().then(data => {
                    if (Object.hasOwn(data, 'errors')) {
                        alert(data["errors"].map(error => error["message"]).join(", "));
                    } else {
                        alert("죄송합니다. 전송 중 오류가 발생했습니다. 다시 시도해주세요.");
                    }
                });
            }
        }).catch(error => {
            alert("죄송합니다. 전송 중 네트워크 오류가 발생했습니다. 다시 시도해주세요.");
        }).finally(() => {
            submitBtn.innerText = originalText;
            submitBtn.disabled = false;
        });
    });
});

// Card Toggle Function (Global)
function toggleCard(card) {
    card.classList.toggle('expanded');
}
