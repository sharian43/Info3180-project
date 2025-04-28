<template>
    <!--Part 2 #2-->
    <form @submit.prevent="Signup" id="registerForm">
      <div>
          <input type="text" name="username" class="form-control" placeholder="Username:" />
      </div>
      <div>
          <input type="text" name="password" class="form-control" placeholder="Password:" />
      </div>
      <div>
          <input type="text" name="fullname" class="form-control" placeholder="Full Name:" />
      </div>
      <div>
          <input type="email" name="email" class="form-control" placeholder="Email Address:" />
      </div>


      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>
      <!-- Error Messages -->
      <div v-if="errorMessages.length" class="alert alert-danger">
      <ul>
          <li v-for="(error, index) in errorMessages" :key="index">{{ error }}</li>
      </ul>
      </div>

      <button type="submit">Sign Up</button>
    </form>
</template>

<script setup>
import {ref} from 'vue';
const successMessage = ref('');
const errorMessages = ref([]);

function Signup(){
  const registerForm = document.getElementById('registerForm');
  let form_data = new FormData(registerForm);

  fetch ('/api/register', {method: 'POST', body: form_data})
  .then ((response)=> response.json())
  .then ((data)=> {
      //display success
      console.log ('User is registered', data)
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