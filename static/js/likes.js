
document.addEventListener('DOMContentLoaded', function() {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    document.querySelectorAll('.js-like-button').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const questionId = this.dataset.questionId;
            const url = `/question/${questionId}/like/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            })
            .then(response => response.json())
            .then(data => {

                if (data.status === 'ok') {
                    const countSpan = button.querySelector('.js-like-count');
                    if (countSpan) {
                        countSpan.textContent = data.likes_count;
                    }

                    if (data.action === 'liked') {
                        button.classList.remove('btn-outline-primary');
                        button.classList.add('btn-primary');
                    } else {
                        button.classList.remove('btn-primary');
                        button.classList.add('btn-outline-primary');
                    }
                }
            })
        });
    });

    document.querySelectorAll('.js-like-answer-button').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const answerId = this.dataset.answerId;
            const url = `/answer/${answerId}/like/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    const countSpan = button.querySelector('.js-answer-like-count');
                    if (countSpan) {
                        countSpan.textContent = data.likes_count;
                    }

                    if (data.action === 'liked') {
                        button.classList.remove('btn-outline-success');
                        button.classList.add('btn-success');
                    } else {
                        button.classList.remove('btn-success');
                        button.classList.add('btn-outline-success');
                    }
                }
            });
        });
    });


    document.querySelectorAll('.js-correct-answer').forEach(function(checkbox) {
        checkbox.addEventListener('change', function(event) {

            const answerId = this.dataset.answerId;
            const questionId = this.dataset.questionId;
            const isChecked = this.checked;

            const url = '/mark_correct_answer/';

            const formData = new FormData();
            formData.append('question_id', questionId);
            formData.append('answer_id', answerId);
            formData.append('is_checked', isChecked);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            })
            .then(response => response.json())
        });
    });
});