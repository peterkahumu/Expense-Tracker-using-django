const username = document.querySelector('#username');
const feedbackField = document.querySelector('.username-feedback');
const usernameSuccess = document.querySelector('.username-success');

const email = document.querySelector('#email');
const emailFeedback = document.querySelector('.email-feedback');
const emailSuccess = document.querySelector('.email-success');

const password = document.querySelector('#password');  
const submitButton = document.querySelector('.submit-btn');

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
        if(data.username_error){
            username.classList.add("is-invalid");
            feedbackField.style.display = "block";
            feedbackField.textContent = data.username_error;
            usernameSuccess.style.display = "none";
            submitButton.setAttribute('disabled', 'disabled')
            submitButton.disabled = true;

        } else {
            username.classList.remove("is-invalid");
            feedbackField.style.display = "none";
            usernameSuccess.style.display = "block";
            usernameSuccess.textContent = "Username is available.";
            submitButton.removeAttribute('disabled');
        }
       });
    } else {
        username.classList.remove("is-invalid");
        feedbackField.style.display = "none";
        usernameSuccess.style.display = "none";
    }
});

email.addEventListener('keyup', (event) => {
    const emailVal = event.target.value;

    // CREATE AN API CALL TO THE SERVER.
    if (emailVal.length > 0) {
       fetch('/authentication/validate-email', {
        body: JSON.stringify({email: emailVal}),
        method: 'POST',
       })
       .then((res)=> res.json())
       .then((data)=> {
        if(data.email_error){
            email.classList.add("is-invalid");
            emailFeedback.style.display = "block";
            emailSuccess.style.display = "none";
            emailFeedback.textContent = data.email_error;
            submitButton.setAttribute('disabled', 'disabled')
            submitButton.disabled = true;
        } else {
            email.classList.remove("is-invalid");
            emailFeedback.style.display = "none";
            submitButton.removeAttribute('disabled');
            emailSuccess.textContent = 'Email available for user';
            emailFeedback.style.display = 'none';
            emailSuccess.style.display = 'block'
        }
       });
    } else {
        email.classList.remove("is-invalid");
        emailFeedback.style.display = "none";
        emailSuccess.style.display = 'none';
    }
});

