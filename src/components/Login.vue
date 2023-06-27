<template>
    <h1 id="l">Login</h1><br>
    <!-- <div class="login">
        <input type="text" v-model="email" placeholder="Enter Email.." />
        <input type="text" v-model="pass" placeholder="Enter Password.." />
        <button @click="login">Login</button><br>
        <h4><RouterLink to="/signup">Sign Up</RouterLink></h4><br><br>
    </div> -->
    <div class="container">
        <label for="uname" id="u"><b>Email</b></label>
        <input type="text" v-model="email" placeholder="Enter email" required>

        <label for="psw" id="p"><b>Password</b></label>
        <input type="password" v-model="pass" placeholder="Enter Password" required>

        <button @click="login">Login</button>
        <RouterLink to="/signup">Sign Up</RouterLink>


        <span class="psw">Forgot <RouterLink to="/forgot">password</RouterLink></span>
        <div v-if="toggle">
        <h2 id="invalid">Invalid credentials !</h2>
    </div>
        
    </div>
    
    
</template>

<script>
import axios from 'axios';


export default{
    name : 'Login',
    data() {
        return{
            email : '',
            pass : '',
            toggle : false
        }
    },
    
    methods:{
         async login(){
            this.toggle = false;
            let result = await axios.post("http://localhost:5000/checkUser",{
                user_email : this.email,
                password : this.pass
            })
            // to get data without promises , use the below line
            // console.log(result.data.confirm)

            if(result.data.confirm == 'valid'){
                this.$router.push({name:'AddTracker'})
            }
            else{
                    this.toggle = true
            }
        },
        async getUser(){
            let result = await axios.post("http://localhost:5000/getUser",{
                pray:'please'
            })
            this.name = result.data.name;
            if(this.name != "None"){
                this.$router.push({name:'AddTracker'})
            }
        }
    },
    mounted(){
      this.getUser();
    }
    
}
</script>



<style scoped>
.logo {
  display: block;
  margin: 0 auto 2rem;
  width: 400px;
}

.container #invalid{
  padding:50px 500px 200px;
}

#u,#p{
    color:black;
}

#l{
    color:black;
    align-self: center;
    padding: 10px 856px;
}

/* Full-width inputs */
input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
  border-radius: 12px;
}

/* Set a style for all buttons */
button {
  background-color: white;
  color: black;
  padding: 14px 20px;
  margin: 8px 0;
  border: solid 2px black;
  cursor: pointer;
  width: 100%;

}

/* Add a hover effect for buttons */
button:hover {
  background-color: black;
  color:white;
  border:none;
}

/* Extra style for the cancel button (red) */
.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}

#invalid{
  padding:12px 170px;
}

/* Center the avatar image inside this container */

/* Avatar image */

/* Add padding to containers */
.container {
  padding: 16px 250px 700px;
}

/* The "Forgot password" text */
span.psw {
  float: right;
  padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
    display: block;
    float: none;
  }
  .cancelbtn {
    width: 100%;
  }
}

</style>