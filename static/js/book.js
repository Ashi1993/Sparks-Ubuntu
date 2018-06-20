$(document).ready(function(){
    console.log("ready!");
    // loadBooks();
});

// function loadBooks(){
//     $.ajax({
//         url: '/loadBooks',
//         data: $('form').serialize(),
//         type: 'POST',
//         success: function (response) {
//             console.log("Response " + response);
//             window.location.href = "book.html";
//         },
//         error: function (error) {
//             console.log("Error " + error);
//             // alert(error);
//         }
//     })
// }