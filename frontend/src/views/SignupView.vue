<template>
  <form @submit.prevent="submit">
    <div class="margin-bottom">
      <label class="input-label" for="username">Username: </label>
      <input v-model="username" type="text"/>
    </div>
    <div class="margin-bottom">
      <label class="input-label" for="email">Email: </label>
      <input v-model="email" type="email"/>
    </div>
    <div class="margin-bottom">
      <label class="input-label" for="password">Password: </label>
      <input v-model="password1" type="password"/>
    </div>
    <div class="margin-bottom">
      <label class="input-label" for="password">Repeat Password: </label>
      <input v-model="password2" type="password"/>
    </div>
    <button class="margin-bottom" type="submit" @click="signUp">
      Signup
    </button>
    <div class="pointer" @click="navigateToLogin">Already have an account? Login instead.</div>


  </form>
</template>

<script>

import {signUp, login} from "@/services/auth.js";

export default {
  name: 'Signup',
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: ''
    };
  },
  methods: {
    signUp() {
      signUp(this.username, this.email, this.password1, this.password2).then((response) => {
        // Login after sign up to get the token
        login(this.email, this.password1).then((response) => {
          localStorage.setItem('token', response.key);
          this.$router.push({path: '/'});
        }).catch((error) => {
          alert(JSON.stringify(error.response.data))
        });
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });

    },
    navigateToLogin() {
      this.$router.push(
          {
            path: `/login`
          })
    }
  }
}
</script>