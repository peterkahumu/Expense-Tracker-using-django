const search = document.querySelector('#search');

search.addEventListener('keyup', (event) => {

    const data = event.target.value;

    if (data.trim().length > 0){
        fetch('/search', {
            body: JSON.stringify({data: data}),
            method: 'POST', 
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('data', data);
        });
    }
})