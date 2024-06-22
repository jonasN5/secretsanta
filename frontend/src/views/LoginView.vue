<template>
  <form @submit.prevent="submit">
    <div class="margin-bottom">
      <label class="input-label" for="email">Email: </label>
      <input v-model="email" type="email"/>
    </div>
    <div class="margin-bottom">
      <label class="input-label" for="password">Password: </label>
      <input v-model="password" type="password"/>
    </div>
    <button class="margin-bottom" type="submit" @click="login">
      Login
    </button>
    <div class="pointer" @click="navigateToSignup">No account? Signup instead.</div>


  </form>
</template>

<script>
import {login} from "/src/services/auth.js";

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      // Send login request and handle authentication token
      login(this.email, this.password).then((response) => {
        // Store the token in local storage
        localStorage.setItem('token', response.key);
        this.$router.push({path: '/'});
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });

    },
    navigateToSignup() {
      this.$router.push(
          {
            path: `/signup`
          })
    }
  }
}
</script>