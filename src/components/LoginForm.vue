<template>
      <!--Part 2 #2-->
      <form @submit.prevent="login" id="loginForm">
        <div>
            <input type="text" name="username" class="form-control" placeholder="Username:" />
        </div>
        <div>
            <input type="text" name="password" class="form-control" placeholder="Password:" />
        </div>
      
        <!-- Error Messages -->
        <div v-if="errorMessages.length" class="alert alert-danger">
        <ul>
            <li v-for="(error, index) in errorMessages" :key="index">{{ error }}</li>
        </ul>
        </div>

        <button type="submit">Login</button>
      </form>
</template>

<script setup>
import {ref} from "vue";
const successMessage = ref('');
const errorMessages = ref([]);

function Login(){
    const loginForm = document.getElementById('loginForm');
    let form_data = new FormData(loginForm);

    fetch ('/api/auth/login', {method: 'POST', body: form_data})
    .then ((response)=> response.json())
    .then ((data)=> {
        //display success
        console.log ('Login successful', data)
        //check if the response has a success message
        if(data.message){
            successMessage.value = data.message;
        }
        if (data.errors){
            errorMessages.value = data.errors;
        }
    })
    .catch ((error)=>{
        errorMessages.value = ["An unexpected error occurred. Please try again."];
        console.log(error)
    });
};

</script>