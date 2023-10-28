// Wait for the HTML document to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Find the button element by its ID
    var myButton = document.getElementById('myButton');

    // Find the element where you want to display the text
    var resultText = document.getElementById('resultText');

    // Add a click event listener to the button
    myButton.addEventListener('click', function () {
        // Change the text when the button is clicked
        resultText.innerHTML = 'Button clicked!';
    });
});
