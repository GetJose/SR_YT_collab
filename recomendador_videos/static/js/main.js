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

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    $(document).on('click', '.video-item', function(e) {
        e.preventDefault();
        
        const videoId = $(this).attr('id').split('-')[1];  
        const videoElement = $(this).closest('.video-item');
        const method = videoElement.data('method'); 
        const url = '/initialRateVideo/';  

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                'video_id': videoId,
                'rating': 0  ,
                'method' : method
            },
            success: function(response) {
                console.log('Avaliação inicial salva com sucesso.');
            },
            error: function(xhr) {
                console.error('Erro ao salvar a avaliação inicial.');
            }
        });

        const iframe = $(this).find('iframe')[0];
        if (iframe) {
            let requestFullScreen = iframe.requestFullscreen || iframe.mozRequestFullScreen || iframe.webkitRequestFullscreen || iframe.msRequestFullscreen;
            if (requestFullScreen) {
                requestFullScreen.call(iframe);
            }
        }
    });

    $(document).on('click', '.rate-button', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const videoId = $(this).data('video-id');
        const rating = $(this).data('rating');
        const url = $(this).data('url');
        const messageDiv = $(this).siblings('.rating-message');
    
        // Capturar os dados do botão
        const videoElement = $(this).closest('.video-item');
        const videoTitle = videoElement.find('h3').text();
        const method = videoElement.data('method');  // Pegar o método de recomendação
    
        // Imprimir os dados no console
        console.log(`Título do vídeo: ${videoTitle}`);
        console.log(`ID do vídeo: ${videoId}`);
        console.log(`Avaliação: ${rating === 1 ? "Gostei" : "Não gostei"}`);
        console.log(`Método de recomendação: ${method}`);
    
        $.ajax({
            url: url,
            method: 'POST',
            data: {
                'video_id': videoId,  // Adicionado para garantir que o ID seja enviado
                'rating': rating,
                'method': method  // Enviar o método de recomendação
            },
            success: function(response) {
                if (rating === 1) {
                    $('#video-' + videoId + ' .rate-button').removeClass('liked disliked');
                    $('#video-' + videoId + ' .rate-button[data-rating="1"]').addClass('liked');
                } else {
                    $('#video-' + videoId + ' .rate-button').removeClass('liked disliked');
                    $('#video-' + videoId + ' .rate-button[data-rating="-1"]').addClass('disliked');
                }
                messageDiv.text(response.message);
            },
            error: function(xhr) {
                messageDiv.text('Erro ao avaliar o vídeo.');
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const recommendationMenu = document.getElementById("recommendationMenu");
    const recommendationSubmenu = document.getElementById("recommendationSubmenu");

    // Mostrar/ocultar submenu ao clicar
    recommendationMenu.addEventListener("click", function(event) {
        event.preventDefault(); // Previne a navegação do link
        recommendationSubmenu.style.display =
            recommendationSubmenu.style.display === "block" ? "none" : "block";
    });

    // Ocultar submenu ao clicar fora dele
    document.addEventListener("click", function(event) {
        if (!recommendationMenu.contains(event.target) && !recommendationSubmenu.contains(event.target)) {
            recommendationSubmenu.style.display = "none";
        }
    });
});
