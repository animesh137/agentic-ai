const form = document.getElementById('todo-form');
const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');

const state = {
  todos: []
};

function renderTodos() {
  list.innerHTML = '';

  if (state.todos.length === 0) {
    const emptyState = document.createElement('li');
    emptyState.textContent = 'No tasks yet. Add one above.';
    emptyState.className = 'todo-item';
    list.appendChild(emptyState);
    return;
  }

  state.todos.forEach((todo, index) => {
    const item = document.createElement('li');
    item.className = `todo-item${todo.done ? ' completed' : ''}`;

    const text = document.createElement('span');
    text.textContent = todo.text;

    const actions = document.createElement('div');
    actions.className = 'todo-actions';

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.textContent = todo.done ? 'Undo' : 'Done';
    toggle.addEventListener('click', () => {
      state.todos[index].done = !state.todos[index].done;
      renderTodos();
    });

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = 'Remove';
    remove.addEventListener('click', () => {
      state.todos.splice(index, 1);
      renderTodos();
    });

    actions.append(toggle, remove);
    item.append(text, actions);
    list.appendChild(item);
  });
}

form.addEventListener('submit', event => {
  event.preventDefault();
  const value = input.value.trim();

  if (!value) {
    return;
  }

  state.todos.push({ text: value, done: false });
  input.value = '';
  input.focus();
  renderTodos();
});

renderTodos();
