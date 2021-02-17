import axios from 'axios';

const URL = "http://a9d2c1bfef3f.ngrok.io";

export const api = axios.create({
    baseURL: URL
});

export const list = (url = URL) => {
    let request = 'get';
    return axios[request](url);
};

export const fetchData = (resource) => {

    let url = `${URL}/${resource}`;    
    return list(url);
};

export const postData = async (url, params) => {
    return await api.post(url, params);
};

export const postDataUser = async (url, params) => {
    return await api.post(url, params);
};


export const setCache = (key, resource) => {
    localStorage.setItem(key, JSON.stringify((resource)));
};

export const listCache = (key) => {
    try {
        return JSON.parse(localStorage.getItem(key))
    } catch (error) {
        return [];
    }
};

export const deleteCache = (key) => {
    localStorage.removeItem(key);
};
