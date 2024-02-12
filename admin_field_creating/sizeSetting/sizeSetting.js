// Get the slider and display element
const slider = document.getElementById('sliderinput');
const sliderText = document.getElementById('slidertext')

// Set the initial size of the table
let tableSize = 3;
sliderText.textContent = `Table size: ${tableSize} x ${tableSize}`;

// Create the table and append it to the fieldDiv element
const field = document.getElementById('field');
for (let i = 0; i < tableSize; i++) {
  const row = document.createElement('tr');
  for (let j = 0; j < tableSize; j++) {
    const cell = document.createElement('td');
    const button = document.createElement('button');
    button.textContent = 'Button';
    cell.appendChild(button);
    row.appendChild(cell);
  }
  field.appendChild(row);
}

// Update the table size when the slider value changes
slider.addEventListener('input', () => {
  tableSize = slider.value;
  sliderText.textContent = `Field size: ${tableSize} x ${tableSize}`;
  field.innerHTML = ''; // Clear the existing table
  for (let i = 0; i < tableSize; i++) {
    const row = document.createElement('tr');
    for (let j = 0; j < tableSize; j++) {
      const cell = document.createElement('td');
      const button = document.createElement('button');
      button.textContent = '';
      button.className = "cell"
      cell.appendChild(button);
      row.appendChild(cell);
    }
    field.appendChild(row);
  }
});