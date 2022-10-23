<template>
  
  <div class="row p-1">
    <div class="col d-flex justify-content-between">
        <div class="px-2">
            <a class="text-uppercase text-dark" @click="toHome" style="cursor: pointer;"><i class="fa-solid fa-angle-left"></i> Volver</a>
        </div>
        <div class="px-2" v-if="isAuthenticated == true">
            <a class="text-dark mr-3">Bienvenido: <span class="text-uppercase">{{ getUsername() }}</span></a>
            <br>
            <button class="btn btn-secondary mt-2 text-uppercase" @click="onLogout"><i class="fa-solid fa-arrow-left"></i> Logout</button>
        </div>           
    </div>
  </div>


  <div class="container mt-2 p-2 d-flex justify-content-center animate__animated animate__fadeInDown">
    <img class="p-2" src="@/assets/logoA.png"/>
    <div class="mt-5">
      <h1>Servicios de Etiquetado</h1>
    </div>
  </div>


  <div  class="container d-flex justify-content-center  animate__animated animate__fadeIn">
    <div id="fileUpload" class="card p-3 shadow-sm border">
        <input type="file" id="file" ref="file" @change="handleFileUpload()" />
    </div>
  </div> 


  <div class="mt-3 animate__animated animate__fadeIn">
    <audio id="audio" controls autoplay></audio>
  </div>




  <form @submit.prevent="tagAudio()">
  <div v-if="audioCargado" class="row d-flex justify-content-center mt-2 animate__animated animate__fadeInDown">

    <div class="col-lg-2 col-sm-6 mt-3">
      <h5>Determine el Genero</h5>
      <div class="form-check text-center">
        <input class="form-check-input" type="radio" name="genero" value="femenino">
        <label class="form-check-label">
          Femenino
        </label>
      </div>
      <div class="form-check text-center">
        <input class="form-check-input" type="radio" name="genero" value="masculino">
        <label class="form-check-label">
          Masculino
        </label>
      </div>
      <div class="form-check text-center">
        <input class="form-check-input" type="radio" name="genero" value="indeterminado">
        <label class="form-check-label">
          Indeterminado
        </label>
      </div>
    </div>


    <div class="col-lg-2 col-sm-6 mt-3">
      <h5>Rango Etario</h5>
      <div class="form-check">
        <input class="form-check-input" type="radio" name="edad" value="menor">
        <label class="form-check-label">
          Menor de 30 años
        </label>
      </div>
      <div class="form-check">
          <input class="form-check-input" type="radio" name="edad" value="mayor">
          <label class="form-check-label">
            Mayor de 30 años
          </label>
      </div>
    </div>
  </div>

  <button  v-if="audioCargado" type="submit" id="tag"
           class="btn btn-success mt-4 animate__animated animate__fadeInDown"> Registrar Etiqueta   
  </button>

  </form>

</template>





<script lang="ts">

import { defineComponent } from 'vue';
import  FilterAPI from '../api/FilterApi'
import Swal from 'sweetalert2';

export default defineComponent({

  name: 'FilterView',
  data(){

      return {
        file: '',
        files: [],
        audioCargado: false,
        genero: '',
        edad: ''
      }
  },
  computed:{
    isAuthenticated(){
      return this.$store.state.user.isAuthenticated;
    }
  },

  methods: {

    
    async tagAudio() { 

      const gen = ( document.querySelector( 'input[name="genero"]:checked' ) as HTMLInputElement );
      const age = ( document.querySelector( 'input[name="edad"]:checked' ) as HTMLInputElement );

      if ( gen == null || age == null ) {
        this.message('Debe seleccionar ambas opciones')
      }
      else{
        this.genero = gen.value 
        this.edad = age.value

        let formData = new FormData();
        formData.append('files', this.file);
        formData.append('gender', this.genero)
        formData.append('age_range', this.edad)

        const tags = await FilterAPI.post('/training_tag', formData )

        tags.data.msg ? this.message( tags.data.msg ) : this.message2( 'Registro realizado correctamente')


        console.log( tags.data )
        this.reset()
      } 
 
    },

    message( msg: string ) {
      Swal.fire({
            icon: 'error',
            title: 'Error al Etiquetar',
            text: msg,
          })
    },

    message2( msg: string ) {
      Swal.fire({
            icon: 'success',
            title: 'Registro Existoso',
            text: msg,
          })
    },

    reset() {
        const file = (document.getElementById('file') as HTMLInputElement)
        file.value =  ''
        file.disabled = false
        this.audioCargado = this.genero = this.edad = ''      
    },

    handleFileUpload(){
      this.file = (this.$refs.file as any).files[0]
      this.audioCargado = true
  
      const urlObj = URL.createObjectURL( (this.$refs.file).files[0] );
      const audio = (document.getElementById('audio') as any);

      audio.addEventListener("load", () => {
        URL.revokeObjectURL(urlObj);
      });
   
      audio.src = urlObj;     
    },

    toHome() {
    this.$router.push({ name: 'home'})
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

})
</script>






<style scoped>
.animate__fadeInDown {
  animation-duration: 2.2s;
}

.animate__fadeInLeft {
  animation-duration: 2.2s;
}

.animate__fadeIn {
  animation-duration: 5s;
}

#calidad{
  background-color: #f1faee;
}

#fileUpload{
  background-color: #f1faee;
}
</style>

