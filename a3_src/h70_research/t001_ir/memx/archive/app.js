// Load YouTube video and chatbot when form is submitted
form.addEventListener('submit', (e) => {
	e.preventDefault();
	const videoId = getVideoId(input.value);
	if (videoId) {
		loadVideo(videoId);
		loadChatbot(videoId);
	}
});

// Extract video ID from YouTube URL
function getVideoId(url) {
	const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
	const match = url.match(regExp);
	if (match && match[2].length === 11) {
		return match[2];
	} else {
		alert('Invalid YouTube URL');
		return null;
	}
}

// Load YouTube video player
function loadVideo(videoId) {
	player.innerHTML = `
		<iframe
			src="https://www.youtube.com/embed/${videoId}?autoplay=1&enablejsapi=1&origin=${window.location.origin}"
			allowfullscreen
		></iframe>
	`;
}

// Load chatbot in iframe
function loadChatbot(videoId) {
	const chatbot = document.querySelector('#chatbot');
	chatbot.src = `https://mychatbotwebsite.com?videoId=${videoId}`;
}
