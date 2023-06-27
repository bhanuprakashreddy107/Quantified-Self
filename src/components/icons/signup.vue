<template>
    <img class="logo" src="../assets/pic.jpeg" />
    <center><h1>Sign up</h1></center><br>
    <div class="register">
        <input type="text" v-model="user_name" placeholder="Enter Name.." />
        <input type="text" v-model="user_email" placeholder="Enter Email.." />
        <input type="password" v-model="password" placeholder="Enter Password.." />
        <center><button @click="signup">Sign up</button></center>
        
    </div>
</template>

<script>

export default{
    name : 'signup',
    data : {
        user_name:'',
        user_email:'',
        password:''
    },
    methods:{
        signup(){
            alert("user added successfully");
        }
    }
}
</script>

<style>

.logo {
  display: block;
  margin: 0 auto 2rem;
  width: 400px;
}

.register input{
    width : 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left: auto;
    border : 1px solid skyblue;

}

.register button{
    width : 320px;
    height : 40px;
    border : 1px solid skyblue;
    background: skyblue;
    color: white;
    cursor: pointer;

}


</style>