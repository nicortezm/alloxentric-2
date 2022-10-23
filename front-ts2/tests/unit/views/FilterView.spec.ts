import { flushPromises, shallowMount } from "@vue/test-utils";
import FilterView from '@/views/FilterView.vue';
import { storeRole1 } from "../mockStore/store";





describe('Pruebas en la Vista de Filtros', () => {

   const mockRouter = {
      push: jest.fn(),
   }

   test('Debe de Mostrase Correctamente la vista FilterView', () => {
      
      const wrapper = shallowMount( FilterView, {
         global: {
            plugins: [ storeRole1 ],
            mocks: {
               $router: mockRouter,           
            }
         },
         computed: {
            isAuthenticated() {
            return storeRole1.state.user.isAuthenticated
            }
         },
      })

      expect( wrapper.html() ).toMatchSnapshot()
   });



    test('Cargar un audio Habilita el boton de Busqueda', async() => {

      const wrapper = shallowMount( FilterView, {
         data() {
            return {
               audioCargado: true,
               file: 'hola.mp3',
               silencioTotal: null
            }
         },
         global: {
            plugins: [ storeRole1 ],
            mocks: {
               $router: mockRouter,           
            }
         },
         computed: {
            isAuthenticated() {
            return storeRole1.state.user.isAuthenticated
            }
         },
         methods: {
            submitFile: jest.fn() 
         }
         
      })

      const handleSubmitFileSpy = jest.spyOn( wrapper.vm, 'submitFile')

      wrapper.find('#calc').trigger('click')  

      await flushPromises()
      expect( handleSubmitFileSpy ).toHaveBeenCalledTimes(1); 
   });



    
   test('Al tener resultado, se habilita Btn de Details y este redirecciona a Details con sus parametros ', async() => {

      const wrapper = shallowMount( FilterView, {
         data() {
            return {
               audioCargado: true,
               file: 'hola.mp3',
               silencioTotal: 1
            }
         },
         global: {
            plugins: [ storeRole1 ],
            mocks: {
               $router: mockRouter,           
            }
         },
         computed: {
            isAuthenticated() {
            return storeRole1.state.user.isAuthenticated
            }
         },
         methods: {
            submitFile: jest.fn(),
            toDetails: jest.fn()    
         }    
      });

      const detalleSpy = jest.spyOn( wrapper.vm, 'toDetails')

      wrapper.find('#detalles').trigger('click')
      await flushPromises()

      expect( detalleSpy ).toHaveBeenCalledTimes(1); 

      expect( mockRouter.push ).toHaveBeenCalledWith({ 
         name: "details",
         params:  
            { endpoint: "total_silence"}
      });

    })


});