let dragged;

function drag(ev) {
  dragged = ev.target;
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drop(ev) {
  ev.preventDefault();
  ev.currentTarget.appendChild(dragged);

  fetch('/move_card', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      card_id: dragged.dataset.cardId,
      list_id: ev.currentTarget.parentElement.dataset.listId
    })
  });
}
