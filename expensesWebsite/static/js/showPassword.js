const togglePassword = document.querySelector('.togglePassword'); 


const handleToggle = (event) => {

    if (togglePassword.textContent === 'Show'){
        togglePassword.textContent = 'Hide';

        password.setAttribute('type', 'text');
    } else {
        togglePassword.textContent = 'Show';
        password.setAttribute('type', 'password');
    };
};

togglePassword.addEventListener('click', handleToggle );