import {get, post} from './network';


export function UserDataH(data) {
    const result = get('/api/user/data', data);
    return result;
}

export function LoginH(data) {
    const result = post('api/user/login', data);
    return result;
}


