// for share button of scrits

document.querySelectorAll('.share-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const title = this.dataset.title;
            const url = this.dataset.url;

            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).catch(err => console.log('Sharing failed', err));
            } else {
                // Fallback: Copy to clipboard
                navigator.clipboard.writeText(url)
                    .then(() => alert('Link copied to clipboard!'))
                    .catch(() => alert('Copy failed. Please try manually.'));
            }
        });
    });