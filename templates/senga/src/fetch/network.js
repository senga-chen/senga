// import 'whatwg-fetch';
// import 'es6-promise';

function obj2params (obj, currentUrl) {
    let str = [];
    for (let p in obj) {
        if (obj.hasOwnProperty(p)) {
            str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]));
        }
    }
    let param = str.join('&');
    if (currentUrl) {
        if (/\?/g.test(currentUrl)) {
            return currentUrl + param;
        } else {
            return currentUrl + '?' + param;
        }
    } else {
        return param;
    }
}

function paramToBody (obj) {
    let formData = new FormData();
    for (let p in obj) {
        formData.append(p, obj[p]);
    }
    return formData;
}

let baseURL = "";
export function get (url, data) {
    let myInit = {
        method: 'GET',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            "Auth": '123'
        }
    };
    let fetchUrl = baseURL + url;
    if (data) {
        fetchUrl = obj2params(data, fetchUrl)
    }
    let result = fetch(fetchUrl, myInit).then(response=>response.json());
    return result;
}

export function post(url, parms) {
    let myInit = {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*'
        },
        credentials: 'include'
    };
    myInit.body = paramToBody(parms);
    return fetch(url, myInit).then(response=>response.json());
}

