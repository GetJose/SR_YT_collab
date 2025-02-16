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
                'rating': 0,
                'method': method
            },
            success: function(response) {
                console.log('Avaliação inicial salva com sucesso.');
            },
            error: function(xhr) {
                console.error('Erro ao salvar a avaliação inicial.');
            }
        });

        // Verificar se fullscreen é permitido
        const iframe = $(this).find('iframe')[0];
        if (iframe && document.fullscreenEnabled) {
            try {
                if (iframe.requestFullscreen) {
                    iframe.requestFullscreen();
                } else if (iframe.mozRequestFullScreen) { 
                    iframe.mozRequestFullScreen();
                } else if (iframe.webkitRequestFullscreen) { 
                    iframe.webkitRequestFullscreen();
                } else if (iframe.msRequestFullscreen) { 
                    iframe.msRequestFullscreen();
                }
            } catch (error) {
                console.warn("Não foi possível entrar em fullscreen:", error);
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

        const videoElement = $(this).closest('.video-item');
        const videoTitle = videoElement.find('h3').text();
        const method = videoElement.data('method');

        console.log(`Título do vídeo: ${videoTitle}`);
        console.log(`ID do vídeo: ${videoId}`);
        console.log(`Avaliação: ${rating === 1 ? "Gostei" : "Não gostei"}`);
        console.log(`Método de recomendação: ${method}`);

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                'video_id': videoId,
                'rating': rating,
                'method': method
            },
            success: function(response) {
                $('#video-' + videoId + ' .rate-button').removeClass('liked disliked');
                $('#video-' + videoId + ` .rate-button[data-rating="${rating}"]`).addClass(rating === 1 ? 'liked' : 'disliked');
                messageDiv.text(response.message);
            },
            error: function(xhr) {
                messageDiv.text('Erro ao avaliar o vídeo.');
            }
        });
    });
});
