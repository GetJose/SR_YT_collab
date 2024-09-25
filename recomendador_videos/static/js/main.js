// Função para pegar o CSRF token dos cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Se este cookie começa com o nome que desejamos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Configura o jQuery para adicionar o token CSRF automaticamente às requisições AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Apenas adiciona o token para requisições que vão para o mesmo domínio
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).on('click', '.rate-button', function(e) {
    e.preventDefault();

    var videoId = $(this).data('video-id');
    var rating = $(this).data('rating');
    var url = $(this).data('url');  // Pega a URL diretamente do data-attribute

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'rating': rating
        },
        success: function(response) {
            if (rating === 1) {
                $('#video-' + videoId + ' .rate-button').removeClass('liked disliked');
                $('#video-' + videoId + ' .rate-button[data-rating="1"]').addClass('liked');
            } else {
                $('#video-' + videoId + ' .rate-button').removeClass('liked disliked');
                $('#video-' + videoId + ' .rate-button[data-rating="-1"]').addClass('disliked');
            }
            $('#video-' + videoId + ' .rating-message').text(response.message);
        },
        error: function(xhr) {
            $('#video-' + videoId + ' .rating-message').text('Erro ao avaliar o vídeo.');
        }
    });
});
