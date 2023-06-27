<template>
<div class="container">
    <b><h1>Change password ??</h1></b><br><br>
    <b><label>Email:</label></b>
    <input v-model="email" type="email" placeholder="email.." />
    <b><label>New password:</label></b>
    <input v-model="new_pass" type="text" placeholder="new.." />
    <b><label>Confirm new password:</label></b>
    <input v-model="c_pass" type="text" placeholder="confirm.." />
    <button @click="submit" class="submitbtn">Submit</button>

<div v-if="toggle">
    <div v-if="answer == 'invalidEmail'">
        <p style="color:azure"> Invalid Email !</p>
    </div>
    <div v-else-if="answer == 'dontMatch'">
        <p style="color:azure">Passwords don't Match!</p><br>
        <p style="color:azure">Please verify the passwords.</p>
    </div>
    <div v-else-if="answer == 'sameOldAndNew'">
        <p style="color:azure">The New Password cannot be same as Old one !</p><br>
        <p style="color:azure">Kindly choose different password.</p>
    </div>
    <div v-else-if="answer == 'Null'">
        <p style="color:azure">All Fields must be Filled!</p><br>
    </div>
    <div v-else>
        <p style="color:green">Successfully Changed the Password</p>
        <RouterLink to="/login">Return to Login page</RouterLink>
    </div>

</div>
</div>
</template>

<script>
import axios from 'axios'

export default{
    name:'Forgot',
    data(){
        return{
            new_pass:'',
            c_pass:'',
            email:'',
            toggle:false,
            answer:''
        }
    },
    
    methods:{
        async submit(){
            let result = await axios.post("http://localhost:5000/forgot",{
                email : this.email,
                new_pass : this.new_pass,
                c_pass : this.c_pass
            })
            this.answer = result.data.response;
            if(this.answer != 'success'){
                this.toggle = true;
            }

        }
    }
}
</script>

<style>
* {box-sizing: border-box}

/* Full-width input fields */
  input[type=text], input[type=password],input[type=email] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
  border-radius: 12px;
}

input[type=text]:focus, input[type=password]:focus,input[type=email]:focus {
  background-color: #ddd;
  outline: none;
}

button:hover {
    background-color: black;
    border:solid 1px white;
    color:white;
}

label{
    color:black
}

.submitpbtn {
  float: left;
  width: 50%;
}

/* Add padding to container elements */
.container {
  padding: 16px 50px 500px;
}

/* Clear floats */
.clearfix::after {
  content: "";
  clear: both;
  display: table;
}

/* Change styles for cancel button and signup button on extra small screens */
@media screen and (max-width: 300px) {
.submitbtn {
    width: 100%;
  }
}
</style>