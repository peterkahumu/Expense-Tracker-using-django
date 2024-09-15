const username = document.querySelector('#username');
const feedbackField = document.querySelector('.invalid-feedback');

// event listener when the user start to type.
username.addEventListener('keyup', (event) => {
    const usernameVal = event.target.value;

    // CREATE AN API CALL TO THE SERVER.
    if (usernameVal.length > 0) {
       fetch('/authentication/validate-username', {
        body: JSON.stringify({username: usernameVal}),
        method: 'POST',
       })
       .then((res)=> res.json())
       .then((data)=> {
        console.log("data", data);
        if(data.username_error){
            username.classList.add("is-invalid");
            feedbackField.style.display = "block";
            feedbackField.textContent = data.username_error;
        } else {
            username.classList.remove("is-invalid");
            feedbackField.style.display = "none";
        }
       });
    }
});