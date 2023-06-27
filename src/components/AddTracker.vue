<template>

<div v-if="user_name != 'None'">
    <div class="sidebar">
        <b><RouterLink to="/seeTrackers">See trackers</RouterLink></b>
        <b><RouterLink to="/logout">Logout</RouterLink></b>
    </div>
    
    <div class="container">
      
        <h1 id="h1">Welcome {{user_name}}, Add Your Tracker</h1><br>
        <b><label>Enter your Tracker Name</label></b><br>
        <input type="text" v-model="tracker_name" placeholder="Enter Tracker Name.." required /><br>
        <b><label>select the Type</label></b>
        <!--<div>
            <select v-model="tracker_format" required>
                <option disabled value="">Please select one</option>
                <option>Numerical</option>
                <option>Time Duration</option>
                <option>Boolean</option>
            </select>
        </div><br><br> -->
        
        <div>
          <form class="form-container">
          <label class="cn">Numerical
                <input v-model="tracker_format" type="radio" value="Numerical">
                <span class="checkmark"></span>
              </label>
              <label class="cn">Time Duration
                <input v-model="tracker_format" type="radio" value="Time Duration" >
                <span class="checkmark"></span>
            </label>
            <label class="cn">Boolean
                <input v-model="tracker_format" type="radio" value="Boolean" >
                <span class="checkmark"></span>
            </label>
            </form>
        </div>
        <br>
        <b><label>Add your description</label></b><br>
        <textarea v-model="desc" placeholder="add your description.." required></textarea><br><br>
        
        <button @click="addTracker">Add Tracker</button>
        <div v-if="warn">
          <p style="color:yellow">please complete all the fields</p>
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


export default{
    name:'AddTracker',
    data()
    {
        return {
            tracker_name : '',
            tracker_format : '',
            tracker_id:'',
            user_name:'',
            desc:'',
            warn:false
        }
    },

    methods:{
        async addTracker(){
            if(this.tracker_name.trim()=='' || this.tracker_format.trim()=='' || this.desc.trim() ==''){
              this.warn = true;
            }
            else{
              let result = await axios.post("http://localhost:5000/addTracker",{
                  name : this.tracker_name,
                  des : this.desc,
                  format : this.tracker_format
              })
              this.tracker_id = result.data.id
              console.log(result.data.id)
              if(result.status == 200){
                  alert("Tracker added succesfully !");
                  this.tracker_name='' ;
                  this.tracker_format='' ;
                  this.note='';
                  this.warn=false;
              }
            }
        },
        async getUser(){
            let result = await axios.post("http://localhost:5000/getUser",{
                pray:'please'
            })
            this.user_name = result.data.name;
        }
    },
     mounted(){
        this.getUser();    
    }
}
</script>

<style scoped>

textarea {
  width: 100%;
  height: 150px;
  padding: 12px 20px;
  box-sizing: border-box;
  border: 2px solid black;
  border-radius: 12px;
  background-color: #f8f8f8;
  font-size: 16px;
  resize: none;

}

button {
  background-color: white;
  color: black;
  padding: 14px 20px;
  cursor: pointer;
  width: 100%;
  border:solid 2px black;

}

button:hover {
  background-color: black;
  color:white;
  border:none;
}

.sidebar {
  margin: 0;
  padding: 0;
  width: 200px;
  position: fixed;
  height: 100%;
  overflow: auto;
  background: #c9cb5a;
  background: -webkit-linear-gradient(top left, #c9cb5a, #FF9393);
  background: -moz-linear-gradient(top left, #c9cb5a, #FF9393);
  background: linear-gradient(to bottom right, #c9cb5a, #FF9393);
  border:solid 1px black;
}

label{
    color:black;
    font-size: large;
}
.please{
  padding:20px 700px 1000px;
}
.container {
  padding: 16px 400px 500px;
}

#h1{
    color:black;
}

/* Sidebar links */
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

input[type=text], input[type=password],input[type=email] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: solid 2px black;
  background: #f1f1f1;
  border-radius: 12px;
}

input[type=text]:focus, input[type=password]:focus,input[type=email]:focus {
  background-color: #ddd;
  outline: none;
}

/* ----------------------------- */
/* select ------------ */

.form-container .cn {
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
.form-container .cn input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

/* Create a custom radio button */
.form-container .checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: #eee;
  border-radius: 50%;
}

/* On mouse-over, add a grey background color */
.form-container .cn:hover input ~ .checkmark {
  background-color: #ccc;
}

/* When the radio button is checked, add a blue background */
.form-container .cn input:checked ~ .checkmark {
  background-color: #2196F3;
}

/* Create the indicator (the dot/circle - hidden when not checked) */
.form-container .checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the indicator (dot/circle) when checked */
.form-container .cn input:checked ~ .checkmark:after {
  display: block;
}

/* Style the indicator (dot/circle) */
.form-container .cn .checkmark:after {
 	top: 9px;
	left: 9px;
	width: 8px;
	height: 8px;
	border-radius: 50%;
	background: white;
}

.form-container{
  border: solid 2px black;
  border-radius: 12px;
}
</style>