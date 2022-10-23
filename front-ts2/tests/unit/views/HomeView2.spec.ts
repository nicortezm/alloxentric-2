import { flushPromises, shallowMount } from "@vue/test-utils";
import HomeView from '@/views/HomeView.vue'
import { storeRole1, storeRole2 } from "../mockStore/store";
import Swal  from 'sweetalert2'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from "@/router";



const router = createRouter({
    history: createWebHistory(),
    routes: routes,
})


jest.mock('sweetalert2', () => ({
    fire: jest.fn(),
    showLoading: jest.fn(),
    close: jest.fn()
}))


describe('Pruebas en la Vista de Home View', () => {

    test('Al clickear boton de tag con Role1 el guard se dispara', async( ) => {
        
        localStorage.setItem('rol', storeRole1.state.user.rol )
        
        router.push({ name: 'home' })

        await router.isReady()

        let wrapper = shallowMount( HomeView, {
            global: {
            plugins: [ storeRole1, router ],

            },
            computed: {
                isAuthenticated() {
                return storeRole1.state.user.isAuthenticated
                }
            },
        })
        
        wrapper.find('.tag').trigger('click')     
        await flushPromises()


        expect( Swal.fire ).toHaveBeenCalledWith({
            icon: 'warning',
            title: 'Rol invalido',
            text: `${ storeRole1.state.user.rol } no tiene acceso a esa vista`,
        })  
    });


    test('Al clickear boton de filtro con Role2 el guard se dispara', async() => {
        
        localStorage.setItem('rol', storeRole2.state.user.rol )
        
        router.push({ name: 'home' })

        await router.isReady()

        const wrapper = shallowMount( HomeView, {
            global: {
            plugins: [ storeRole2, router ],

            },
            computed: {
                isAuthenticated() {
                return storeRole2.state.user.isAuthenticated
                }
            },
        })
        
        wrapper.find('.filter').trigger('click')     
        await flushPromises() 
        
        expect( Swal.fire ).toHaveBeenCalledWith({
            icon: 'warning',
            title: 'Rol invalido',
            text: `${ storeRole1.state.user.rol } no tiene acceso a esa vista`,
        })  
    });


  
})



        