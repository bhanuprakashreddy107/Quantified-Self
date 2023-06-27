<template>
<div class="logout">
<h1>you logged out successfully !</h1>

<RouterLink to="login">Login</RouterLink>
</div>
</template>

<script>
import axios from 'axios'

export default{
    name : 'Logout',
    
    methods:{
        async removeUser(){
            let result = await axios.post("http://localhost:5000/removeUser",{
                pray:'please'
            })

        }
    },
    mounted(){
        this.removeUser();
    }
}
</script>

<style>
.logout{
    padding : 100px 650px 1000px;
}
</style>