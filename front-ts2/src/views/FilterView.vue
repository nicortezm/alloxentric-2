
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
      <h1>Servicios de Audio</h1>
    </div>
  </div>

  <div  class="container d-flex justify-content-center  animate__animated animate__fadeIn">
    <div id="fileUpload" class="card p-3 shadow-sm border">
        <input type="file" id="file" class="file" ref="file" @change="handleFileUpload($event)"/>
    </div>
  </div>

  <div class="container d-flex justify-content-center  animate__animated animate__fadeInLeft">
    
    <div id="calidad" class="col-4-sm p-1 border mt-4">

      <h5 class="p-2"><b>Reglas de Calidad</b></h5>

      <table class="table table-md table-borderless">

          <tr>
            <th class="text-left" scope="col">FILTRO</th>
            <th scope="col ">RESULTADO</th>
            <th scope="col ">DETALLES</th>
          </tr>

          <tr>
            <th class="text-left h6" scope="col">
              <input ref="silencio_total" type="checkbox" id="silencio_total">
              Silencio Total    
            </th>
            <th scope="col"><label v-if="silencioTotal != undefined">{{ silencioTotal }} segundos</label></th>
            <th scope="col">
              <button class="btn btn-secondary btn-sm" v-if="silencioTotal != undefined" id="detalles" @click="toDetails('total_silence')">
                <i class="fa-solid fa-magnifying-glass"></i>
                  Detalle
              </button>
            </th>
          </tr>

          <tr>
            <th class="text-left h6" scope="col">
              <input ref="silencio_final" type="checkbox" id="silencio_final">
              Silencio Final
            </th>
            <th scope="col"><label v-if="silencioFinal != undefined">{{ silencioFinal }} segundos</label></th>
            <th scope="col">
              <button  class="btn btn-secondary btn-sm" v-if="silencioFinal != undefined" @click="toDetails('final_silence')">
                <i class="fa-solid fa-magnifying-glass"></i>
                  Detalle
                </button>
            </th>
          </tr>
          
          <tr>
            <th class="text-left h6" scope="col">
              <input ref="silencio_inicial" type="checkbox" id="silencio_inicial">
              Silencio Inicial
            </th>
            <th scope="col"><label v-if="tiempoEspera != undefined">{{ tiempoEspera }} segundos</label></th>
            <th scope="col">
              <button class="btn btn-secondary btn-sm" v-if="tiempoEspera != undefined" @click="toDetails('wait_time')">
                <i class="fa-solid fa-magnifying-glass"></i> 
                  Detalle
                </button>
              </th>
          </tr>

          <tr>
            <th class="text-left h6" scope="col">
              <input ref="ruido" type="checkbox" id="noise">
              Ruido
            </th>
            <th scope="col"><label v-if="tiempoRuido != undefined">{{ tiempoRuido }} segundos</label></th>
            <th scope="col">
              <button class="btn btn-secondary btn-sm" v-if="tiempoRuido != undefined" @click="toDetails('noise')">
                <i class="fa-solid fa-magnifying-glass"></i>
                Detalle</button>
            </th>
          </tr>

      </table>

      <template v-if="audioCargado">
          <button  @click="submitFile" id="calc" ref="calc" class="btn btn-success mr-4" >Calcular</button>
          <button @click="reset" id="reset" ref="reset" class="btn btn-info" disabled>Reset</button>
      </template>
    </div>
     
  </div> 



</template>



<script lang="ts">
import { defineComponent  } from 'vue';
import  FilterAPI from '../api/FilterApi'
import Swal from 'sweetalert2';

export default defineComponent({

  name: 'FilterView',
  data(){

      return {
        file: '',
        audioCargado: false,
        silencioFinal: null,
        silencioTotal: null,
        tiempoEspera: null,
        tiempoRuido: null,
        final: null,
        total: null, 
        inicial: null,
        ruido: null
      }
  },

  computed:{
    isAuthenticated(){
      return this.$store.state.user.isAuthenticated;
    }
  },

  methods: {

      async submitFile() {

        this.$refs.calc.disabled = true
        this.$refs.file.disabled = true

        this.$refs.silencio_total.disabled   = this.$refs.ruido.disabled = 
        this.$refs.silencio_inicial.disabled = this.$refs.silencio_final.disabled = true

        let formData = new FormData();
        formData.append('files', this.file);

        try {

          if ( !this.$refs.silencio_final.checked   &&
               !this.$refs.silencio_total.checked   && 
               !this.$refs.silencio_inicial.checked &&
               !this.$refs.ruido.checked ) {
              return this.message( 'Debe Seleccionar una opción')
            }
 

          Swal.fire({
          title: 'Cargando...',
          html: 'Por favor espere hasta que la petición se complete',
          didOpen: () => {
            Swal.showLoading()
          },
           allowOutsideClick: false   
          })

          if ( this.$refs.silencio_final.checked ){
            const respFinal = await FilterAPI.post( '/final_silence',formData )
            if(!respFinal.data.msg) {
              this.final = respFinal.data.value
            } else {
              return this.message( respFinal.data.msg )
            }
          }       

          if ( this.$refs.silencio_total.checked ) {
            const respTotal = await FilterAPI.post( '/total_silence',formData )
            if(!respTotal.data.msg) {
              this.total = respTotal.data.value
            } else {
              return this.message( respTotal.data.msg )  
            }
          } 

          if ( this.$refs.silencio_inicial.checked ) {
            const respInitial = await FilterAPI.post( '/wait_time',formData )
            if(!respInitial.data.msg) {
              this.inicial = respInitial.data.value
            } else {
              return this.message( respInitial.data.msg )
               
            }
          }
          
          if ( this.$refs.ruido.checked ) {
            const respNoise = await FilterAPI.post( '/noise',formData )
            if(!respNoise.data.msg) {
              this.ruido = respNoise.data.value
            } else {
              return this.message( respNoise.data.msg ) 
            }
          } 

          
        } catch (error) {
          return this.message( 'Peticion Sobrecargada, Pruebe con menos filtros' )
        }
        

        this.silencioFinal = this.final
        console.log(   this.silencioFinal,  this.final )
        this.silencioTotal = this.total 
        this.tiempoEspera  = this.inicial
        this.tiempoRuido   = this.ruido
        this.$refs.reset.disabled = false
        Swal.close()
      },




      message( msg: string ) {
        Swal.fire({
              icon: 'error',
              title: 'Error al calcular',
              text: msg,
            })
        this.reset()
      },



      async toDetails( service: string ) {
        this.$router.push( { name: 'details' , params: { endpoint : service } } )
      },



      handleFileUpload(){
        this.file = (this.$refs.file as any).files[0]
        this.audioCargado = true
      },

      toHome() {
      this.$router.push({ name: 'home'})
      },


      reset() {
        const checkbox    = ( document.querySelectorAll('input[type=checkbox]') as any )
        checkbox.forEach( e => {
          e.disabled = false 
          e.checked = false
        });
        
        this.$refs.file.disabled = false 
        this.$refs.file.value    =  ''

        Object.assign(this.$data, this.$options.data.call(this))
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
