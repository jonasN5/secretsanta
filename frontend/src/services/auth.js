import axios from "@/axios";

/**
 * Sign up a new user
 * @param {string} username
 * @param {string} email
 * @param {string} password1
 * @param {string} password2
 * @returns {Promise<any>}
 */
export async function signUp(username, email, password1, password2) {
    const response = await axios
        .post(`/auth/registration/`, {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2
        })

    return response.data;
}

/**
 * Log the user in and return the obtained token.
 * @param {string} email
 * @param {string} password
 * @returns {Promise<any>}
 */
export async function login(email, password) {
    const response = await axios
        .post(`/auth/login/`, {'email': email, 'password': password})
    return response.data;
}

