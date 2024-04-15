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
      // Add the user message to the chat
      addUserMessage(message);

      // Send the message to Django backend using AJAX
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/chat/', true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Correct way to get CSRF token from cookies
      xhr.onreadystatechange = function() {
          if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
              var response = JSON.parse(this.responseText);
              // Add the bot response to the chat
              addBotMessage(response.response);
              var chatbox = document.getElementById('chat-messages');
              chatbox.scrollTop = chatbox.scrollHeight; // Scroll to the bottom
          }
      };
      xhr.send('message=' + encodeURIComponent(message));
      
      input.value = ''; // Clear input box after sending
  }
}

// Function to add user message to chat
function addUserMessage(content) {
  var chatMessages = document.getElementById('chat-messages');
  var messageDiv = document.createElement('div');
  messageDiv.classList.add('message', 'user-message');
  messageDiv.textContent = content; // Use textContent for security
  chatMessages.appendChild(messageDiv);
}

// Function to add bot message to chat
function addBotMessage(content) {
  var chatMessages = document.getElementById('chat-messages');
  var messageDiv = document.createElement('div');
  messageDiv.classList.add('message', 'bot-message');
  messageDiv.textContent = content; // Use textContent for security
  chatMessages.appendChild(messageDiv);
}

// Function to get CSRF token from cookies
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
