<template>

  <div class="row p-1">
      <div class="col d-flex justify-content-between">
         <div class="px-2">
            <a
               class="text-uppercase text-dark"
               @click="toFilter"
               style="cursor: pointer"
               ><i class="fa-solid fa-angle-left"></i> Volver</a
            >
        </div>
        <div class="px-2" v-if="isAuthenticated == true">
            <a class="text-dark mr-3">Bienvenido: <span class="text-uppercase">{{ getUsername() }}</span></a>
            <br>
            <button class="btn btn-secondary mt-2 text-uppercase" @click="onLogout"><i class="fa-solid fa-arrow-left"></i> Logout</button>
        </div>   
   </div>
  </div>


  <div class="row d-flex justify-content-center mt-3">
    <div class="col-lg-6 col-sm-12 mt-2">
      <table class="table" >
        <thead>
          <tr>
            <th scope="col">Audio Name</th>
            <th scope="col">{{ endpoint }}</th>
            <th scope="col">Percentage of Audio</th>
          </tr>
        </thead>

        <tbody v-for="val in values" :key="val.id" >
          <tr id="val">
            <td>{{ val.audio_name }}</td>
            <td>{{ val.value }}</td>
            <td>{{ val.percentage }}</td>
          </tr>
        </tbody>
       
      </table>     
    </div>
   
  </div>

  <div class="row d-flex justify-content-center mt-3">
      <button id="boton" @click="getValues()" class="btn btn-secondary">
         <i class="fa-solid fa-magnifying-glass"></i> Obtener Valores
      </button>
  </div>
</template>



<script lang="ts">

import FilterAPI from "../api/FilterApi";
export default {
  name: "DetailsView",

  data() {
      return {
         values: null,
      };
  },

  props: {
      endpoint: {
         type: String,
         required: true,
      },
  },

  computed:{
    isAuthenticated(){
      return this.$store.state.user.isAuthenticated;
    }
  },

  methods: {

      async getValues() {
        const resp = await FilterAPI.get(`/${this.$props.endpoint}`);
          
          console.log( 'hola' )
          this.values = resp.data;

          console.log( this.values )

        },

      toFilter() {
         this.$router.push({ name: "filter" });
      },
      onLogout(){
        let payloadRefreshedTokens = {
          idToken: '',
          accessToken: ''
      }
        this.$store.commit("login", payloadRefreshedTokens)
        this.$store.commit("logout")
    },
      getUsername(){
        return this.$store.state.user.name
      }
  },
};
</script>


<style>

</style>