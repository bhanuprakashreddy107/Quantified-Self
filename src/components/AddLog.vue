<template>
<div class="Log" v-if="name != 'None'">
    <div class="sidebar">
        <b><RouterLink to="/seeTrackers">See trackers</RouterLink></b>
        <b><RouterLink to="/addTracker">Add Tracker</RouterLink></b>
        <b><RouterLink to="/logout">Logout</RouterLink></b>
    </div>
    <div class="container">
        <h1>Add Log here..</h1>
        <div v-if="type === 'Numerical'">
            <b><label>Enter the value:</label></b>
            <input type="number" v-model="value" placeholder="Enter a numeric value (in mts)" required/>
        </div>
        <div v-else-if="type === 'Time Duration'">
            <b><label>Enter the hours value:</label></b>
            <input type="number" v-model="h" required/>

            <b><label>Enter the minutes value:</label></b>
            <input type="number" v-model="m" required/>

            <b><label>Enter the seconds value:</label></b>
            <input type="number" v-model="s" required/>
        </div>
        <div v-else>
            <b><label>Select the value</label></b>
            <!-- <input type="radio" v-model="value" value="Yes" />
            <label for="one">True</label>

            <input type="radio" v-model="value" value="No" />
            <label for="two">False</label> -->
            <label class="cn">Yes
                <input v-model="value" type="radio" value="Yes" >
                <span class="checkmark"></span>
              </label>
              <label class="cn">No
                <input v-model="value" type="radio" value="No">
                <span class="checkmark"></span>
            </label>

        </div>
        <b><label>Enter a note</label></b>
        <input type="text" v-model="note" placeholder="Enter a note here.." />
        <button @click="addLog">Add Log</button>
        <div v-if="warn" style="color:yellow">
          please fill in all fields !!
        </div>
    </div>
</div>
<div v-else>
    <div class="please">
    <h1>Please Login</h1>
    <RouterLink to="/login">Login</RouterLink>
    </div>
</div>
</template>

<script>

import axios from 'axios';
import Header from './Header.vue';

export default{
    name : 'AddLog',
    data(){
        return{
            value : '',
            note : '',
            type : '',
            name:'',
            m:'',
            h:'',
            s:'',
            warn:false
        }
    },

    components:{
        Header,
    },
    methods:{
        async addLog(){
          
          if(this.type==="Time Duration"){
            if(this.h=='' || this.m=='' || this.s==''){
              this.warn = true
            }
            else{
            let result = await axios.post("http://localhost:5000/addLog/"+this.$route.params.id,{
                
                log_value : String(this.h)+" hrs "+String(this.m)+" mins "+String(this.s)+" secs",
                log_note : this.note
                
            })
            console.log(result)
            alert("log added succesfully!");
            this.note = '';
            this.h='';
            this.m='';
            this.s='';
            }
          }
          else{
            if(this.value == ''){
              this.warn = true;
            }
            else{
            let result = await axios.post("http://localhost:5000/addLog/"+this.$route.params.id,{

              log_value : this.value,
              log_note : this.note
            })
            console.log(result)
            alert("log added succesfully!");
            this.note = '';
            this.value = ''; 
          }
          }
             
        },

        async getType(){
            let result = await axios.post("http://localhost:5000/getType/"+this.$route.params.id,{
                pray : 'please'
            })
            this.type = result.data.type;
        },
        async getUser(){
            let result = await axios.post("http://localhost:5000/getUser",{
                pray:'please'
            })
            this.name = result.data.name;
        }
    },
    mounted(){
        this.getType();
        this.getUser()
    }

}
</script>

<style scoped>
.container {
  padding: 16px 400px 550px;
}
.please{
  padding:20px 700px 1000px;
}

button {
  background-color: white;
  color: black;
  padding: 14px 20px;
  margin: 8px 0;
  border: solid 2px black;
  cursor: pointer;
  width: 100%;

}
label{
    color:black;
}

/* Add a hover effect for buttons */
button:hover {
  background-color: black;
  color:white;
  border:none;
}

input[type=number], input[type=text] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
  border-radius: 12px;
}

.sidebar {
  margin: 0;
  padding: 0;
  width: 200px;
  background-color: #f1f1f1;
  position: fixed;
  height: 100%;
  overflow: auto;
  border:solid 1px black;
  background: #c9cb5a;
  background: -webkit-linear-gradient(top left, #c9cb5a, #FF9393);
  background: -moz-linear-gradient(top left, #c9cb5a, #FF9393);
  background: linear-gradient(to bottom right, #c9cb5a, #FF9393);
}

.sidebar a {
  display: block;
  color: black;
  padding: 16px;
  text-decoration: none;
  border-bottom: solid 1px black;
}


/* Links on mouse-over */
.sidebar a:hover:not(.active) {
  background-color: black;
  color: white;
}

/* Page content. The value of the margin-left property should match the value of the sidebar's width property */
div.content {
  margin-left: 200px;
  padding: 1px 16px;
  height: 1000px;
}

/* On screens that are less than 700px wide, make the sidebar into a topbar */
@media screen and (max-width: 700px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  .sidebar a {float: left;}
  div.content {margin-left: 0;}
}

/* On screens that are less than 400px, display the bar vertically, instead of horizontally */
@media screen and (max-width: 400px) {
  .sidebar a {
    text-align: center;
    float: none;
  }
}

.cn {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 22px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default radio button */
.cn input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

/* Create a custom radio button */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: #eee;
  border-radius: 50%;
}

/* On mouse-over, add a grey background color */
.cn:hover input ~ .checkmark {
  background-color: #ccc;
}

/* When the radio button is checked, add a blue background */
.cn input:checked ~ .checkmark {
  background-color: #2196F3;
}

/* Create the indicator (the dot/circle - hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the indicator (dot/circle) when checked */
.cn input:checked ~ .checkmark:after {
  display: block;
}

/* Style the indicator (dot/circle) */
.cn .checkmark:after {
 	top: 9px;
	left: 9px;
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background: white;
}
</style>