document.addEventListener("DOMContentLoaded", function () {
    function sendRating(videoId, rating, method, messageDiv = null) {
        if (videoId && rating !== null && method) {
            $.ajax({
                url: '/recomendacao/rate_video/',
                method: 'POST',
                data: { 'video_id': videoId, 'rating': rating, 'method': method },
                success: function (response) {
                    if (messageDiv) messageDiv.text(response.message || 'Avaliação registrada com sucesso.');
                },
                error: function () {
                    if (messageDiv) messageDiv.text('Erro ao avaliar o vídeo.');
                }
            });
        }
    }

    $(document).on('click', '.video-item', function (e) {
        e.preventDefault();
        const videoId = $(this).attr('id')?.split('-')[1] || '';
        const method = $(this).data('method') || '';
    
        sendRating(videoId, 0, method);
        
        const iframe = $(this).find('iframe')[0];
        if (iframe) {
            iframe.scrollIntoView({ behavior: 'smooth', block: 'center' }); 
            iframe.focus(); 

            iframe.contentWindow.postMessage(
                '{"event":"command","func":"playVideo","args":""}',
                '*'
            );

            $(this).find('.play-overlay').hide();
        }
    });

    $(document).on('click', '.play-overlay', function (e) {
        e.preventDefault();
        const videoContainer = $(this).closest('.video-item');
        const iframe = videoContainer.find('iframe')[0];
    
        if (iframe) {
            iframe.contentWindow.postMessage(
                '{"event":"command","func":"playVideo","args":""}',
                '*'
            );
    
            $(this).hide(); 
        }
    });
    

    $(document).on('click', '.rate-button', function (e) {
        e.preventDefault();
        e.stopPropagation();
        
        const videoId = $(this).data('video-id');
        const rating = $(this).data('rating');
        const messageDiv = $(this).siblings('.rating-message');
        const method = $(this).closest('.video-item').data('method') || '';

        if ($(this).hasClass('liked') || $(this).hasClass('disliked')) {
            $(this).removeClass('liked disliked');
        } else {
            $(this).siblings('.rate-button').removeClass('liked disliked');
            $(this).addClass(rating === 1 ? 'liked' : 'disliked');
        }

        sendRating(videoId, rating, method, messageDiv);
    });

    $(document).on('click', function (e) {
        if (!$(e.target).closest('.video-item').length) {
            $('.play-overlay').show();
        }
    });
});
