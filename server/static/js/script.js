var globalDocumentText = "";  // Global variable to store the document text

function submitQuery() {
    console.log("Submitting query...");
    var userQuery = document.getElementById('userQuery').value;
    $.ajax({
        url: '/create-embedding',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ query: userQuery }),
        success: function(response) {
            // Assuming 'answer' is the key that holds the GPT-4 response
            var answer = response.answer;
            document.getElementById('response').innerText = answer;
        },
        error: function(error) {
            console.error("Error:", error);
        }
    });
}

function askQuestion() {
    var userQuestion = document.getElementById('userQuery').value;
    $.ajax({
        url: '/ask-question',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ question: userQuestion, documentText: globalDocumentText }),
        success: function(response) {
            // Assuming 'answer' is the key that holds the GPT-4 response
            var answer = response.answer;
            document.getElementById('response').innerText = answer;
        },
        error: function(error) {
            console.error("Error:", error);
        }
    });
}

function askForSourcePages(documentText) {
    $.ajax({
        url: '/ask-question',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ question: "Which pages are these quotes from?", documentText: documentText }),
        success: function(response) {
            // Uncomment and update if you plan to display source info
            // document.getElementById('source').innerText = "Source: " + response.answer;
        },
        error: function(error) {
            console.error("Error:", error);
        }
    });
}