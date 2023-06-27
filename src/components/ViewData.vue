<template>
<div v-if="name != 'None'">
<div class="sidebar">
        <b><RouterLink to="/seeTrackers">See trackers</RouterLink></b>
        <b><RouterLink to="/addTracker">Add Tracker</RouterLink></b>
        <b><RouterLink to="/logout">Logout</RouterLink></b>
        
    </div>
<div class="parent">
<div class="container" v-if="logs.length > 0">
    <h1>your Log Data</h1><br><br>
    <div>
    <canvas id="myChart"></canvas>
    </div>
    <button @click="download" id="down"><b>Download stats</b></button><br><br>
    <div v-for="log in logs" id="log">
        <h3>your log value is {{log.log_value}}</h3>
        <h3>you added this at {{log.log_stamp}}</h3>
        <h3>Note : {{log.log_note}}</h3><br>
        <button @click="deleteLog(log.log_id)" id="del"><b>delete</b></button>
        <button @click="doSome(log.log_id)" id="ed"><b>edit</b></button>
    </div>
    <!--<div v-if="toggle">

</div>  -->
</div>
<div v-else>
  <h1>Sorry, you have added no data !</h1>
</div>
<div class="form-popup" id="myForm">
    <div class="form-container">
        <h1>Edit</h1>
    <div v-if="type === 'Numerical'">
            <input type="number" v-model="value" placeholder="Enter a numeric value"/>
        </div>
        <div v-else-if="type === 'Time Duration'">
            <b><label>Enter the hours value:</label></b>
            <input type="number" v-model="h"/>

            <b><label>Enter the minutes value:</label></b>
            <input type="number" v-model="m"/>

            <b><label>Enter the seconds value:</label></b>
            <input type="number" v-model="s"/>
        </div>
        <div v-else>

            <label class="cn">Yes
                <input v-model="value" type="radio" value="Yes">
                <span class="checkmark"></span>
              </label>
              <label class="cn">No
                <input v-model="value" type="radio" value="No" >
                <span class="checkmark"></span>
            </label>
        </div>
    <label>Enter a Note</label>
    <input type="text" v-model="note" placeholder="enter a note"/>
    <button @click="saveLog(edit)" class="save">Save Changes</button>
    <button @click="closeForm()" class="close">Cancel</button>
    <div v-if="warn" style="color:red">
      <p>please fill in all fields.</p>
    </div>
    </div>
    
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
import Chart from 'chart.js/auto';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';


import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
} from 'chart.js'


export default{
    name:'ViewData',
    data(){
        return{
            logs : [],
            loaded : false,
            chartData : null,
            dsets : [],
            bool:false,
            edit:null,
            value:'',
            note:'',
            toggle:false,
            type:'',
            down:[],
            name:'',
            h:'',
            m:'',
            s:'',
            warn:false,
        }
    },
    
    components:{
        Line,
    },
    methods:{
        async getType(){
            let result = await axios.post("http://localhost:5000/getType/"+this.$route.params.id,{
                pray:'please'
            })
            this.type = result.data.type;
            if(this.type === 'Numerical'){
                this.bool = true;
            }
        },
        doSome(id){
            this.edit = id;
            document.getElementById("myForm").style.display="block";
        },
        closeForm(){
            this.h='';
            this.m='';
            this.s='';
            this.note='';
            this.warn=false;
            document.getElementById("myForm").style.display="none";
        },
        async logData(){
            let result = await axios.post("http://localhost:5000/viewData/"+this.$route.params.id,{
                pray : 'please'
            })
            this.logs = result.data;
            console.log(result.data);
        },
        async deleteLog(id){
            let result = await axios.delete("http://localhost:5000/deleteLog/"+id);
            this.logData();
            this.getData();
            this.pdfData();
        },
        async saveLog(id){
            if(this.type==='Time Duration'){
                if(this.h=='' || this.m=='' || this.s==''){
                  this.warn = true;
                }
                else{
                let result = await axios.post("http://localhost:5000/saveLog/"+id,{
                    log_value : String(this.h)+" hrs "+String(this.m)+" mins "+String(this.s)+" secs",
                    log_note : this.note
                })
                console.log(result.data.confirm);
                this.toggle = false;
                this.logData();
                this.getData();
                this.pdfData();
                document.getElementById("myForm").style.display="none";
                this.h='';
                this.m='';
                this.s='';
                this.note='';
                this.warn=false;
                }
                
            }
            else{
            if(this.value=='' || this.note==''){
              this.warn = true;
            }
            else{
            let result = await axios.post("http://localhost:5000/saveLog/"+id,{
                log_value : this.value,
                log_note : this.note,
            })
            console.log(result.data.confirm);
            this.toggle = false;
            this.logData();
            this.pdfData();
            document.getElementById("myForm").style.display="none";
            }
            }
            this.value='';
            this.note='';
            
        },
        async getData(){
            let result = await axios.post("http://localhost:5000/getData/"+this.$route.params.id,{
                pray : 'please'
            })
            
            const ctx = document.getElementById('myChart');
            const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: result.data.labels,
                datasets: [{
                    label: 'Log Data',
                    data: result.data.values,
                    fill: false,
                    borderColor: 'rgb(0, 0, 0)',
                    color: '#666',
                    pointHoverBackgroundColor:'#123',
                    tension: 0.1,
                    xAxisID:'X-axis',
                    yAxisID:'Y-axis',
                }]
                },
            });
            myChart;
             
        },
        async pdfData(){
            let result = await axios.post("http://localhost:5000/download",{
                pray:'please'
            })
            for (const one of result.data) {
                let k = [one.n,one.tracker,one.count,one.avg,one.total];
                this.down.push(k);
            }
        },
        download(){
            var pdf = new jsPDF();
            pdf.text('your Statistics',50,10);
            autoTable(pdf,{
                head : [['Sl No','Tracker Name','count','Average','total value']],
                margin : {top:50},
                body : this.down
            });
            pdf.save('stats.pdf');
        },
        async getUser(){
            let result = await axios.post("http://localhost:5000/getUser",{
                pray:'please'
            })
            this.name = result.data.name;
        }
    },
    mounted(){
        this.getUser();
        this.getType();
        this.getData();
        this.logData();
        this.pdfData();
    }
}
</script>

<style>
.please{
  padding:20px 700px 1000px;
}
button {
  padding: 14px 20px;
  margin: 8px 0;
  border: solid 2px black;
  cursor: pointer;
  width: 20%;
  border-radius: 12px;
}

.container {
  padding: 16px 400px 500px;
}
.parent{
  padding:16px 400px 1000px;
}
#down{
    background-color:coral;
    color:black;
    border:solid 2px black;
}

#down:hover{
    background-color: black;
    color:white
}
#log{
  border:solid 2px black;
  border-radius: 12px;
  padding-left: 12px;
}
#ed {
  background-color: #9f7013;
  color:black;
  border:solid 2px black;
}
#ed:hover{
    background-color: black;
    color:white;
}

#del {
  background-color: #ce2208;
  color:black;
  border:solid 2px black;
}
#del:hover{
    background-color: black;
    color:white;
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
.form-container input[type=number], input[type=text] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  background: #f1f1f1;
  border-radius: 12px;

}

/* When the inputs get focus, do something */
.form-container input[type=number]:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/login button */
.form-container .save {
  background-color: hsl(52, 77%, 52%);
  color: black;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom:10px;
  opacity: 0.8;
}

.form-container .save:hover{
    background-color: black;
    color:white;
}

/* Add a red background color to the cancel button */
.form-container .close {
  background-color: red;
  color: black;
  padding: 16px 20px;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom:10px;
  opacity: 0.8;
}

.form-container .close:hover {
  background-color: black;
  color:white;
}

/* Add some hover effects to buttons */
.form-container .btn:hover, .open-button:hover {
  opacity: 1;
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

.form-container{
  border:solid 2px black;
  border-radius: 12px;
}
</style>