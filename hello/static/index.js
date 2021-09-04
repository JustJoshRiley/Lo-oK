async function get_urls(){
    return await fetch('/results').then(response => response.json());
};

get_urls().then(urls => alert(urls['urls'][0]));