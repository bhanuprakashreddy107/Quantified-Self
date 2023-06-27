<template>
<div class="out">
<div class="container">
<h1> Hello, welcome to home page</h1><br><br>
<h3>About Quantified self:</h3><br>
<b> <p>
    The quantified self refers both to the cultural phenomenon of self-tracking with
    technology and to a community of users and makers of self-tracking tools who share an 
    interest in "self-knowledge through numbers".Quantified self practices overlap with the practice
    of lifelogging and other trends that incorporate technology and data acquisition into daily life, often with the 
    goal of improving physical, mental, and emotional performance. The widespread adoption in recent years of wearable 
    fitness and sleep trackers such as the Fitbit or the Apple Watch, combined with the increased presence of 
    Internet of things in 
    healthcare and in exercise equipment, have made self-tracking accessible to a large segment of the population.
    Other terms for using self-tracking data 
    to improve daily functioning[3] are auto-analytics,
    body hacking, self-quantifying, self-surveillance, sousveillance
    (recording of personal activity), and personal informatics.
</p></b>
<RouterLink to="/signup" id="link">signup</RouterLink><br><br>
<RouterLink to="/login" id="link">login</RouterLink>
</div>
</div>
</template>

<script>

export default{
    name : 'Home',
    
}
</script>

<style scoped>

#link{
    border: 1px solid black;
    background-color: white;
    color:black;
    padding:10px 15px;
}

#link:hover{
    background-color: black;
    color:white
}
.out{
    padding: 0px 50px 400px ;
}
.out .container{
    padding:0px 300px 1000px;
}


</style>