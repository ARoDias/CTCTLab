/* exported setCookie, getCookie */

// Function to set cookie with expiration time
export function setCookie(name, value, hours) {
    const expires = new Date(Date.now() + hours * 3600000).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


