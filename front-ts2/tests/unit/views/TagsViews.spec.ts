
import Swal  from 'sweetalert2'
import TagsView from '@/views/TagsView.vue'

import { storeRole1, storeRole2 } from "../mockStore/store";
import { flushPromises, shallowMount } from "@vue/test-utils";



jest.mock('sweetalert2', () => ({
    fire: jest.fn(),
    showLoading: jest.fn(),
    close: jest.fn()
}))


describe('Pruebas en la Vista de Tags View', () => {

   const mockRouter = {
      push: jest.fn(),
   }


   test('Debe de renderizar Correctamente TagsView', () => {

      const wrapper = shallowMount( TagsView, {
         global: {
            plugins: [ storeRole2 ],
            mocks: {
               $router: mockRouter,           
            }
         },
         computed: {
            isAuthenticated() {
            return storeRole2.state.user.isAuthenticated
            }
         },
      })

      expect( wrapper.html() ).toMatchSnapshot();
   });

    

   test('Al cargar un audio y clickear registrar se dispara la funcion', async() => {
      
      const wrapper = shallowMount( TagsView, {
         data() {
            return {
               audioCargado: true,
               genero: 'masculino',
               edad: '30'
            }
         },
         global: {
            plugins: [ storeRole2 ],
            mocks: {
               $router: mockRouter,           
            }
         },
         computed: {
            isAuthenticated() {
            return storeRole2.state.user.isAuthenticated
            }
         },
         methods: {
            tagAudio: jest.fn() 
         }
         
      })

      const handleTagAudioSpy = jest.spyOn( wrapper.vm, 'tagAudio')

      wrapper.find('#tag').trigger('submit')  

      await flushPromises()
      expect( handleTagAudioSpy ).toHaveBeenCalledTimes(1); 
         
   });

  


});


    
    



        

