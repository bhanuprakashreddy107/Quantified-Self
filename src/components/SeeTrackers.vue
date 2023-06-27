<template>
<div v-if="name != 'None'">
    <div class="sidebar">
            <b><RouterLink to="/addTracker">Add Tracker</RouterLink></b>
            <b><RouterLink to="/logout">Logout</RouterLink></b>
        </div>
    <div class="container" v-if="trackers.length > 0">
        <b><h1 id="my">My Trackers</h1></b><br><br>
        <div v-for=" tracker in trackers" class="col">
            
                <h2 id="h">{{tracker.tracker_name}}</h2>
                <h4 id="h">your description: {{tracker.des}}</h4>
                <h4 id="h">recently added : {{recent[tracker['tracker_id']].recentl}}</h4>
                <h4 id="h">recent value : {{recent[tracker['tracker_id']].recentv}}</h4>
                <button @click="addlog(tracker.tracker_id)" id="addlog">Add Log</button>
                <button @click="deleteTracker(tracker.tracker_id)" id="del">Delete</button>
                <button @click="viewData(tracker.tracker_id)" id="vd">View Data</button>
                <button @click="editTracker(tracker.tracker_id)" id="ed">Edit</button>
        </div>
        <!-- <div v-if="toggle">
            <h1>Fill the From to Edit</h1><br>
            <label>Enter your tracker name</label>
            <input v-model="t_name" placeholder="tracker name .." /><br>
            <label>Tracker description</label>
            <textarea v-model="desc" placeholder="add your description.."></textarea>
            <label>select type of tracker</label>
            <div>
                <select v-model="t_type">
                <option disabled value="">Please select one</option>
                <option>Numerical</option>
                <option>Time Duration</option>
                <option>Boolean</option>
                </select>
            </div>
            <button @click="saveTracker(edit)">Save Changes</button>
        </div> -->
        <div class="form-popup" id="myForm">
            <div class="form-container">
                <h1>Edit</h1>

                <label>Enter your tracker name</label>
                <input v-model="t_name" placeholder="tracker name .." type="text" /><br>
                <label>Tracker description</label>
                <textarea v-model="desc" placeholder="add your description.." type="text"></textarea>
                <label>select type of tracker</label>
                <div>
                    <label class="cn">Numerical
                    <input v-model="t_type" type="radio" value="Numerical">
                    <span class="checkmark"></span>
                  </label>
                  <label class="cn">Time Duration
                    <input v-model="t_type" type="radio" value="Time Duration" >
                    <span class="checkmark"></span>
                </label>
                <label class="cn">Boolean
                    <input v-model="t_type" type="radio" value="Boolean" >
                    <span class="checkmark"></span>
                </label>
                </div>

                <button class="btn" @click="saveTracker(edit)">Submit</button>
                <button type="button" class="btn cancel" @click="closeForm()">Close</button>
                <div v-if="warn" style="color:red">
                    please fill all fields
                </div>
            </div>
            
        </div>
    </div>
    <div id="else" v-else >
      <h1>Sorry, you have added no Trackers !</h1>
      <h1>Go back and Kindly add Trackers.</h1>
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
import Header from './Header.vue'

export default{
    name : 'SeeTrackers',
    data(){
        return{
            t_name:'',
            t_type:'',
            toggle : false,
            trackers : [],
            edit : null,
            desc:'',
            recent:null,
            name:'',
            warn:false
        }
    },
    components:{
        Header,
    },
    methods:{
        addlog(id){
            this.$router.push({path:`/addLog/${id}`});
        },
        editTracker(id){
            this.edit = id;
            document.getElementById("myForm").style.display = "block";
        },
        closeForm(){
            document.getElementById("myForm").style.display= "none";
            this.t_name='';
            this.desc='';
            this.t_type='';
            this.warn=false;
        },
        viewData(id){
            this.$router.push({path:`/viewData/${id}`})
        },
        async deleteTracker(id){
            let result = await axios.delete("http://localhost:5000/deleteTracker/"+id)
            .then(alert("deleted successfully"))
            this.loadData();
            this.getRecent()
            
        },
        async loadData(){
            let result = await axios.post("http://localhost:5000/seeTrackers",{
                name : 'Bhanu',
            }).then(response =>{
                this.trackers = response.data
                console.log(response.data);
            })
        },
        
        async saveTracker(id){
            if(this.t_name.trim()=='' || this.desc.trim()=='' || this.t_type.trim()==''){
              this.warn = true
            }
            else{
            let result = await axios.post("http://localhost:5000/saveTracker/"+id,{
                    name: this.t_name,
                    des : this.desc,
                    type : this.t_type
            })
            alert("saved Changed successfuly");
            console.log(result.data.confrim);
            this.toggle = false;
            this.loadData();
            this.getRecent();
            document.getElementById("myForm").style.display= "none";
            this.t_name='';
            this.desc='';
            this.t_type='';
            this.warn=false;
            }
            
        },
        async getRecent(){
            let result = await axios.post("http://localhost:5000/getRecent",{
                pray : 'please'
            })
            this.recent = result.data;
            console.log(result.data)

        },
        async getUser(){
            let result = await axios.post("http://localhost:5000/getUser",{
                pray:'please'
            })
            this.name = result.data.name;

        }

    },
        mounted() {
            this.getUser();
            this.loadData();
            this.getRecent();
    },
}
</script>


<style scoped>
#h{
    color:black;
}
#else{
  padding:12px 400px 1000px;
}
.col{
    border:solid 2px black;
    border-radius: 12px;
    padding-left: 12px;
}
.sidebar {
  margin: 0;
  padding: 0;
  width: 200px;
  background-color: #f1f1f1;
  position: fixed;
  height: 100%;
  overflow: auto;
  background: #c9cb5a;
  background: -webkit-linear-gradient(top left, #c9cb5a, #FF9393);
  background: -moz-linear-gradient(top left, #c9cb5a, #FF9393);
  background: linear-gradient(to bottom right, #c9cb5a, #FF9393);
  border:solid 1px black;
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

.container {
  padding: 16px 400px 1000px;
}

div.content {
  margin-left: 200px;
  padding: 1px 16px;
  height: 1000px;
}

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

button {
  padding: 14px 20px;
  margin: 8px 0;
  border: solid 1px black;
  cursor: pointer;
  width: 20%;

}

button:hover{
    background-color: white;
    color:black;
}
#addlog {
  background-color: #87b049;
  color:black;
  border:none;

}
#addlog:hover{
    background-color:black;
    color:white;
}

#del {
  background-color: #ce2208;
  color:black;
  border:none;
}
#del:hover{
    background-color: black;
    color:white;
}
.please{
  padding:20px 700px 1000px;
}

#vd {
  background-color: skyblue;
  color:black;
  border:none;
}
#vd:hover{
    background-color: black;
    color:white;
}

#ed {
  background-color: #daa9ff;
  color:black;
  border:none;
}
#ed:hover{
    background-color: black;
    color:white;
}

body {font-family: Arial, Helvetica, sans-serif;}
* {box-sizing: border-box;}


.form-popup {
  display: none;
  position: fixed;
  bottom: 0;
  right: 15px;
  border: 1px solid black;
  z-index: 9;
  border-radius: 12px;
}

/* Add styles to the form container */
.form-container {
  max-width: 300px;
  padding: 10px;
  background-color: white;
}

/* Full-width input fields */
.form-container input[type=text] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  background: #f1f1f1;
  border-radius: 12px;
}

/* When the inputs get focus, do something */
.form-container input[type=text]:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/login button */
.form-container .btn {
  background-color: hsl(52, 77%, 52%);
  color: black;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom:10px;
  opacity: 0.8;
}

.form-container .btn:hover{
    background-color: black;
    color:white;
}

/* Add a red background color to the cancel button */
.form-container .cancel {
  background-color: red;
}

.form-container .cancel:hover {
  background-color: black;
  color:white;
}

/* Add some hover effects to buttons */
.form-container .btn:hover, .open-button:hover {
  opacity: 1;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 12px 20px;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
  font-size: 16px;
  resize: none;
}

label{
    color:black;
}

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

</style>