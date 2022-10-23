// ts-nocheck ignores all ts errors in the file
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck

import DetailsView from '@/views/DetailsView.vue'

import { routes } from "@/router";
import { storeRole1, storeRole2 } from "../mockStore/store";
import { flushPromises, MountingOptions, shallowMount } from "@vue/test-utils";
import { createRouter, createWebHistory } from 'vue-router'

// @ts-ignore`
describe('Pruebas en la Vista DetailsView', () => {

   const mockRouter = {
      push: jest.fn(),
   }

   test('Debe de renderizar correctamente la vista', () => {
      
      const wrapper = shallowMount( DetailsView, {
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
         props: {
            endpoint: 'silencio_total'
         }
      });

      expect( wrapper.html() ).toMatchSnapshot();
   });



   test('Al clickear boton obtener Valores la tabla se pobla', () => {

      const values = [
         { audio_duration:1, audio_name: 'test1.mp3', value: 1, percentage: 10 },
         { audio_duration:2, audio_name: 'test2.mp3', value: 2, percentage: 20 },
         { audio_duration:3, audio_name: 'test3.mp3', value: 3, percentage: 30 },
         { audio_duration:4, audio_name: 'test4.mp3', value: 4, percentage: 40 },
         { audio_duration:5, audio_name: 'test5.mp3', value: 5, percentage: 50 }
      ]

      const wrapper = shallowMount( DetailsView, {
         data() {
            return {
               values: [
                  { audio_duration:1, audio_name: 'test1.mp3', value: 1, percentage: 10 },
                  { audio_duration:2, audio_name: 'test2.mp3', value: 2, percentage: 20 },
                  { audio_duration:3, audio_name: 'test3.mp3', value: 3, percentage: 30 },
                  { audio_duration:4, audio_name: 'test4.mp3', value: 4, percentage: 40 },
                  { audio_duration:5, audio_name: 'test5.mp3', value: 5, percentage: 50 }
               ]
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
         props: {
            endpoint: 'silencio_total'
         }
      });

      wrapper.find('#boton').trigger('click');

       expect( wrapper.find('table').text() )
      .toBe(`Audio Namesilencio_totalPercentage of Audio${ values[0].audio_name }${ values[0].value }${ values[0].percentage }${ values[1].audio_name }${ values[1].value }${ values[1].percentage }${ values[2].audio_name }${ values[2].value }${ values[2].percentage }${ values[3].audio_name }${ values[3].value }${ values[3].percentage }${ values[4].audio_name }${ values[4].value }${ values[4].percentage }`)
   });








});