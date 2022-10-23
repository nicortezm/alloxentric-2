<template> 

  <div class="row p-1">
    <div class="col d-flex justify-content-end">
        <div class="px-2" v-if="isAuthenticated == true">
            <a class="text-dark mr-3">Bienvenido: <span class="text-uppercase">{{ $store.state.user.name }}</span></a>
            <br>
            <button class="btn btn-secondary mt-2 text-uppercase" @click="onLogout"><i class="fa-solid fa-arrow-left"></i> Logout</button>
        </div>        
    </div>
  </div>
  <div class="container mt-2 p-2 d-flex justify-content-center animate__animated animate__fadeInDown">
    <img class="p-2" src="@/assets/logoA.png"/>
    <div class="mt-5">
      <h1>Servicios de Audio</h1>
    </div>
  </div>

  <div class="container d-flex justify-content-center">
      <div class="col-lg-6 col-sm-12 border border-dark p-5" style="border-radius: 20px; background-color:#f1faee;">
      <h3 class="text-center">¿Qué Desea Hacer?</h3>
      <button class="filter btn btn-secondary mt-3" @click="toFilter"  style="border-radius: 10px;"> Filtros de Calidad</button>
      <button class="tag btn btn-secondary mt-3 ml-2" @click="toTags" style="border-radius: 10px;"> Etiquetar Audios</button>
    </div>
  </div>
</template>




<script lang="ts">

import { defineComponent } from 'vue';

export default defineComponent({

  name: 'HomeView',

  computed:{
    isAuthenticated(){
      return this.$store.state.user.isAuthenticated;
    }
  },

  methods: {
    toTags() {
      this.$router.push({ name: 'tags'})
    },

     toFilter() {
      this.$router.push({ name: 'filter'})
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
  }


})
</script>

