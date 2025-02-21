document.addEventListener("DOMContentLoaded", function () {
    $(document).on('click', '.video-item', function (e) {
        e.preventDefault();
        
        // Verifica se o elemento tem ID antes de tentar acessar
        const videoId = $(this).attr('id') || ''; 

        if (videoId.includes('-')) {
            const videoIdNumber = videoId.split('-')[1];

            if (videoIdNumber) {
                const videoElement = $(this).closest('.video-item');
                const method = videoElement.data('method') || '';  
                const url = '/initialRateVideo/';

                if (method) {  
                    $.ajax({
                        url: url,
                        method: 'POST',
                        data: {
                            'video_id': videoIdNumber,
                            'rating': 0,
                            'method': method
                        },
                        success: function (response) {
                            console.log('Avaliação inicial salva com sucesso.');
                        },
                        error: function (xhr) {
                            console.error('Erro ao salvar a avaliação inicial.');
                        }
                    });
                }
            }
        }

        // Lógica do fullscreen (separada da avaliação)
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

    $(document).on('click', '.rate-button', function (e) {
        e.preventDefault();
        e.stopPropagation();

        const videoId = $(this).data('video-id') || null;
        const rating = $(this).data('rating') || null;
        const url = $(this).data('url') || null;
        const messageDiv = $(this).siblings('.rating-message');

        if (!videoId || !rating || !url) {
            console.warn("Dados de avaliação incompletos.");
            return;
        }

        const videoElement = $(this).closest('.video-item');
        const videoTitle = videoElement.find('h3').text() || "Título não disponível";
        const method = videoElement.data('method') || '';

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
            success: function (response) {
                $('#video-' + videoId + ' .rate-button').removeClass('liked disliked');
                $('#video-' + videoId + ` .rate-button[data-rating="${rating}"]`).addClass(rating === 1 ? 'liked' : 'disliked');
                messageDiv.text(response.message);
            },
            error: function (xhr) {
                messageDiv.text('Erro ao avaliar o vídeo.');
            }
        });
    });
});
