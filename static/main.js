document.getElementById('contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const contact = document.getElementById('contact').value;
  const type = document.getElementById('type').value;

  const response = await fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, contact, type }),
  });

  const result = await response.json();
  
  if (result.redirect) {
    window.location.href = result.redirect;
  } else {
    document.getElementById('response').innerText = result.message;
  }
});
