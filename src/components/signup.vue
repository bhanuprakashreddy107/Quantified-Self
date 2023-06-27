<template>
    <!-- <div class="register">
        <input type="text" v-model='name' placeholder="Enter Name.." />
        <input type="text" v-model="email" placeholder="Enter Email.." />
        <input type="text" v-model="pass" placeholder="Enter Password.." />
        <button @click="signup">Sign up</button><br><br>
        <RouterLink to="/login">Login</RouterLink>
    </div> -->
    <div class="container">
        <h3 id="s">Sign Up</h3>
        <hr>

        <label for="email"><b>Email</b></label>
        <input type="email" v-model="email" placeholder="Enter Email" required>

        <label for="psw"><b>Create Username</b></label>
        <input type="text" v-model="name" placeholder="Enter Username" required>

        <label for="psw-repeat"><b>Password</b></label>
        <input type="password" v-model="pass" placeholder="Enter Password"  required>

        <button @click="signup">Sign up</button><br><br>
        <RouterLink to="/login">Login</RouterLink>

        
    </div>
    
</template>

<script>
import axios from 'axios';

export default{
    name : 'signup',
    data(){
        return{
            name:'',
            email:'',
            pass:''
        }
    },
    
    methods:{
        async signup()
        {
            let result = await axios.post("http://localhost:5000/addUser",{
                user_name : this.name,
                user_email : this.email,
                password : this.pass
            });
            console.warn(result);
            if (result.status==200){
               this.$router.push({name:'Login'})
            }
        }
    }
}
</script>

<style scoped>
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

hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}

/* Set a style for all buttons */
button {
  background-color: white;  
  padding: 14px 20px;
  margin: 8px 0;
  border: solid 2px black;
  cursor: pointer;
  width: 100%;
}

button:hover {
    background-color: black;
    border:solid 1px white;
    color:white;
}

label{
    color:black
}
#s{
    color: black;
    padding: 0px 725px;
}

/* Float cancel and signup buttons and add an equal width */
.signupbtn {
  float: left;
  width: 50%;
}

/* Add padding to container elements */
.container {
  padding: 16px 100px 600px;
}

/* Clear floats */
.clearfix::after {
  content: "";
  clear: both;
  display: table;
}

/* Change styles for cancel button and signup button on extra small screens */
@media screen and (max-width: 300px) {
.signupbtn {
    width: 100%;
  }
}
</style>