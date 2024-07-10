document.addEventListener('DOMContentLoaded', function () {
    fetch('/static/videosData.json')
        .then(response => response.json())
        .then(data => {
            const gallery = document.getElementById('video-gallery');
            data.forEach(video => {
                const videoCard = document.createElement('div');
                videoCard.classList.add('video-card');

                videoCard.innerHTML = `
                    <h3>${video.title}</h3>
                    <img src="${video.img}" alt="${video.alt}" style="width: auto; height: 150px; margin:0 auto;">
                    <a href="${video.url}" class="glightbox btn-watch-video d-flex align-items-center justify-content-center pt-2">
                        <i class="bi bi-play-circle"></i>
                        <span>Ver Video</span>
                    </a>
                `;

                gallery.appendChild(videoCard);
            });

            const lightbox = GLightbox({
                selector: '.glightbox'
            });
        })
        .catch(error => console.error('Error loading video data:', error));
});
