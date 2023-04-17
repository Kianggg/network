// I really hope we're allowed to use JQuery for this

$(document).ready(function() {
    $("#edit-post-button").click(function() {
        // Get the post id
        var post_id = $(this).parent().attr("id")
        //  Determine status of button
        let buttonStatus = $(this).attr('value');
        // Get content/textarea
        let content_container = $(this).siblings('#post-content');

        // Time to edit!
        if (buttonStatus == "Edit") {
            // Change text on button
            $(this).attr('value', "Save");
            // Get textarea
            content_container.replaceWith(function () {
                let replacement = "<textarea id='post-content'>" + content_container.text() + "</textarea>";
                return replacement;
            });
        }
        // Otherwise, save this post!
        else {
            // Get the new text
            new_content = $(this).siblings('#post-content').text()
            
            // Set the new text
            fetch(`/posts/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: new_content
                })
            });

            // Change back the text box
            editing_box = $(this).siblings('#post-content');
            editing_box.replaceWith(function () {
                let replacement = "<span id='post-content'>" + new_content + "</span>";
                return replacement;
            });

            // Change text on button
            $(this).attr('value', "Edit");
            create_alert("success", "Post edited successfully!");
        }
    })
})

// Sends a notification to the top of the screen that fades after 7 seconds
// Type must be 'success' or 'error'
function create_alert(type, message) {
  let alert = document.createElement('div');
  alert.setAttribute("id", "announcement");
  alert.setAttribute("class", type);
  alert.innerHTML = `<h3>${message}</h3>`;
  document.querySelector(".body").prepend(alert);
}