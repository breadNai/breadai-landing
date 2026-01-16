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

    // Form Submission Logic
    quoteForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Collect Form Data
        const formData = {
            company: document.getElementById('company').value,
            department: document.getElementById('department').value,
            position: document.getElementById('position').value,
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            timestamp: new Date().toISOString()
        };

        // Button Loading State
        const submitBtn = quoteForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerText;
        submitBtn.innerText = '전송 중...';
        submitBtn.disabled = true;

        // Simulate API Call / Email Send
        setTimeout(() => {
            console.log('--- New Quote Inquiry ---');
            console.log('To: ceo@breadai.co.kr');
            console.table(formData);

            // Success Feedback
            alert(`견적 문의가 성공적으로 접수되었습니다.\n\n[전송된 데이터]\n회사: ${formData.company}\n이름: ${formData.name}\n이메일: ${formData.email}\n\nceo@breadai.co.kr로 자동 전송되었습니다.`);

            // Reset and Close
            quoteForm.reset();
            closeModal();

            submitBtn.innerText = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
});

// Card Toggle Function (Global)
function toggleCard(card) {
    // Optional: Close others when one opens
    // document.querySelectorAll('.feature-card').forEach(c => {
    //     if (c !== card) c.classList.remove('expanded');
    // });

    card.classList.toggle('expanded');
}
