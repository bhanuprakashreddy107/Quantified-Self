<template>
<div>
<nav>
<RouterLink to="/login">Login</RouterLink>
<RouterLink to="/seeTrackers">See Trackers</RouterLink>
<RouterLink to="/logout">Logout</RouterLink>
</nav>
</div>
</template>

<script>
export default {
    name:'Header'
}
</script>

<style>
.nav{
    background-color: #333;
    overflow: hidden;
}
.nav a{
    float: left;
    color:aliceblue;
    padding:14px 16px;
    text-align: center;
    font-size: 17px;
    text-decoration:none;
    margin-right: 5px;
}
</style>