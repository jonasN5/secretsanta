import axios from 'axios'


const instance = axios.create({
    baseURL: 'http://localhost:8000/',
});

// Set the Auth token on any request
instance.interceptors.request.use(function (config) {
    const token = localStorage.getItem('token');
    config.headers.Authorization = token ? `Token ${token}` : '';
    return config;
});

export default instance