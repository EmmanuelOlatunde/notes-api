// static/notes/app.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('note-form');
  const title = document.getElementById('title');
  const content = document.getElementById('content');
  const tags = document.getElementById('tags');
  const search = document.getElementById('search');
  const noteList = document.getElementById('note-list');

  const token = document.querySelector('input[name=csrfmiddlewaretoken]')?.value;

  function fetchNotes(query = '') {
    fetch(`/api/notes/?search=${query}`, {
      headers: {
        'Accept': 'application/json'
      }
    })
    .then(res => res.json())
    .then(data => {
      noteList.innerHTML = '';
      data.forEach(note => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = `<strong>${note.title}</strong><br>${note.content}<br><small>${note.tags?.join(', ')}</small>`;
        noteList.appendChild(li);
      });
    });
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const payload = {
      title: title.value,
      content: content.value,
      tags: tags.value.split(',').map(tag => tag.trim()).filter(Boolean),
    };

    fetch('/api/notes/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': token || '',
      },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(() => {
      form.reset();
      fetchNotes();
    });
  });

  search.addEventListener('input', () => {
    fetchNotes(search.value);
  });

  fetchNotes();
});
