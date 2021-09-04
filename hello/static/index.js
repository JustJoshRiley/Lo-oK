async function get_urls(){
    return await fetch('/results').then(response => response.json());
};

await get_urls().then(urls => alert(urls['urls'][0]));s