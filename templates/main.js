const buttons = document.querySelectorAll('button');

buttons.forEach(button => {
  button.addEventListener('click', () => {
    showPopup();
  });
});
function showPopup() {
    const popup = document.querySelector('.popup');
    popup.style.display = 'block';
}

document.getElementById('close-button').addEventListener('click', function() {
    // Hide the pop-up window
    this.parentElement.style.display = 'none';
    console.log("LOG")
});