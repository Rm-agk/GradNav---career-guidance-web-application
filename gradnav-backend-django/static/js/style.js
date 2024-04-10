document.getElementById('chatbot-toggle').onclick = function() {
    var widget = document.getElementById('chatbot-widget');
    widget.style.display = 'flex'; // Show the chat widget
};

document.getElementById('chat-close').onclick = function() {
    var widget = document.getElementById('chatbot-widget');
    widget.style.display = 'none'; // Hide the chat widget
};

// Function to handle sending messages
function sendMessage() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();

    if (message !== '') {
        var chatbox = document.getElementById('chat-messages');
        // Display user message
        chatbox.innerHTML += '<div>User: ' + message + '</div>';

        // Send the message to Django backend using AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/chat/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        // Make sure to replace '{{ csrf_token }}' with the actual token value dynamically inserted by Django template
        xhr.setRequestHeader('X-CSRFToken', 'YourCSRFTokenHere'); // Handle CSRF token dynamically
        xhr.onreadystatechange = function() {
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                var response = JSON.parse(this.responseText);
                // Display bot response
                chatbox.innerHTML += '<div>Bot: ' + response.response + '</div>';
                chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
            }
        };
        xhr.send('message=' + encodeURIComponent(message));
        
        input.value = ''; // Clear input box after sending
    }
}

document.getElementById('chat-input').onkeypress = function(e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent the default action to stop from adding a new line
        sendMessage();
    }
};

document.getElementById('chat-send').onclick = function() {
    sendMessage();
};

document.addEventListener('DOMContentLoaded', () => {
  const testimonials = document.querySelectorAll('.testimonial');
  let currentIndex = 0;

  function showTestimonial(index) {
    testimonials.forEach((testimonial, i) => {
      testimonial.style.display = i === index ? 'block' : 'none';
    });
  }

  document.querySelector('.btn-prev').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
    showTestimonial(currentIndex);
  });

  document.querySelector('.btn-next').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % testimonials.length;
    showTestimonial(currentIndex);
  });

  // Initialize the first testimonial
  showTestimonial(currentIndex);
});
