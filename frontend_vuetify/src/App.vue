<template>
  <v-app>
    <v-container>
      <v-form lazy-validation ref="form" v-on:submit.prevent="submitForm"> 
        <v-row justify="space-between">
          <v-col>
            <v-text-field
                v-model="student.name"
                label="Name"
                clearable
                :rules="[rules.required]"
             ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
                v-model="student.course"
                label="Course"
                clearable
                :rules="[rules.required]"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
                v-model.number="student.rating"
                type="number"
                min=0
                label="Rating"
                clearable
                :rules="[rules.isdigit]"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-btn class="my-3" color="success" type="submit">Submit</v-btn>
          </v-col>
        </v-row>
      </v-form>
    </v-container>  
 <v-container justify="space-between"> 
    <v-data-table
        :headers="headers"
        :items="students"
    >
       <template v-slot:item="row">
          <tr @dblclick="$data.student = row.item">
            <td>{{row.item.name}}</td>
            <td>{{row.item.course}}</td>
            <td>{{row.item.rating}}</td>
            <td>
                <v-btn class="mx-2" fab dark small @click="deleteStudent(row.item)">
                    <v-icon dark>mdi-delete</v-icon>
                </v-btn>
            </td>
          </tr>
      </template>
    </v-data-table>
 </v-container>   
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data(){
    return {
        headers: [
        {
            text: "Students",
            align: "start",
            sortable: true,
            value: "name",
        },
        {
            text: "Course",
            sortable: true,
            value: "course",
        },
        {
            text: "Rating",
            sortable: true,
            value: "rating",
        },
        {
            text: "Delete",
            sortable: false,
        },
        ],
        student: {
            'name': '',
            'course': '',
            'rating': '',
        },
        students: [],
        rules: {
            required: v => !!v || "Required",
            isdigit: v => {
                if (!isNaN(parseFloat(v)) && v >= 0) return true;
                return "Rating must be a number";
            }
        
        }
    }
  },
  async created(){
    await this.getStudents()
     },
  methods: {
    async getStudents(){
        var response = await fetch('http://localhost:8000/api/students/');
        this.students = await response.json();
        this.$refs.form.resetValidation()
    },
    submitForm(){
        if (this.$refs.form.validate()){
            if (this.student.id === undefined){
                this.createStudent();
            }
            else{
                this.editStudent();
            }
        }
    },
    async createStudent(){
        await this.getStudents();
        await fetch('http://localhost:8000/api/students/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.student)
        });
        await this.getStudents();    
        this.student = {}
    },
    async editStudent(){
        await this.getStudents();
        await fetch(`http://localhost:8000/api/students/${this.student.id}/`, {
            method: 'put',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.student)
        });
        await this.getStudents();    
        this.student = {};
    },
    async deleteStudent(student){
        await this.getStudents();
        await fetch(`http://localhost:8000/api/students/${student.id}/`, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.student)
        });
        await this.getStudents();    
    },


  }
}
</script>
