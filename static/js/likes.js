document.addEventListener('DOMContentLoaded', function() {
    console.log('DEBUG: likes.js - Document click detected. Target:', event.target);


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

    document.addEventListener('click', function(event) {
        
        const likeQuestionButton = event.target.closest('.js-like-button');
        if (likeQuestionButton) {

            event.preventDefault();
            const questionId = likeQuestionButton.dataset.questionId;
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
                    const countSpan = likeQuestionButton.querySelector('.js-like-count');
                    if (countSpan) {
                        countSpan.textContent = data.likes_count;
                    }

                    if (data.action === 'liked') {
                        likeQuestionButton.classList.remove('btn-outline-primary');
                        likeQuestionButton.classList.add('btn-primary');
                    } else {
                        likeQuestionButton.classList.remove('btn-primary');
                        likeQuestionButton.classList.add('btn-outline-primary');
                    }
                }
            })
            .catch(error => console.error('Error liking question:', error));
            return;
        }

        const likeAnswerButton = event.target.closest('.js-like-answer-button');
        if (likeAnswerButton) {
            event.preventDefault();
            const answerId = likeAnswerButton.dataset.answerId;
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
                    const countSpan = likeAnswerButton.querySelector('.js-answer-like-count');
                    if (countSpan) {
                        countSpan.textContent = data.likes_count;
                    }

                    if (data.action === 'liked') {
                        likeAnswerButton.classList.remove('btn-outline-success');
                        likeAnswerButton.classList.add('btn-success');
                    } else {
                        likeAnswerButton.classList.remove('btn-success');
                        likeAnswerButton.classList.add('btn-outline-success');
                    }
                }
            })
            .catch(error => console.error('Error liking answer:', error));
            return;
        }

    });

    document.addEventListener('change', function(event) {

        const correctAnswerCheckbox = event.target.closest('.js-correct-answer');
        if (correctAnswerCheckbox) {
            const answerId = correctAnswerCheckbox.dataset.answerId;
            const questionId = correctAnswerCheckbox.dataset.questionId;
            const isChecked = correctAnswerCheckbox.checked;
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
            .then(data => {
                if (data.status === 'ok') {
                    console.log('Correct answer status updated:', data);
                } else {
                    console.error('Error updating correct answer status:', data);
                }
            })
            .catch(error => console.error('Error marking correct answer:', error));
            return;
        }

    });

});