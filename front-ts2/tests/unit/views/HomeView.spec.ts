import Swal  from 'sweetalert2'
import HomeView from '@/views/HomeView.vue'

import { routes } from "@/router";
import { storeRole1, storeRole2 } from "../mockStore/store";
import { flushPromises, shallowMount } from "@vue/test-utils";
import { createRouter, createWebHistory } from 'vue-router'


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

    const mockRouter = {
        push: jest.fn(),
    }


    

    test('Debe de renderizar correctamente HomeView y mostrar el nombre de usuario ', () => {

        const wrapper = shallowMount( HomeView, {
            global: {
                plugins: [ storeRole1 ],
                mocks: {
                    $router: router,           
                }
            },
            computed: {
                isAuthenticated() {
                return storeRole1.state.user.isAuthenticated
                }
            },
        })

        const UserName = wrapper.find('span').text() 
        expect( UserName ).toBe('jorge' )
        expect( wrapper.html() ).toMatchSnapshot()
    });



    test('Al clickear botón de filtro se dirigira a filterView', () => {

        const wrapper = shallowMount( HomeView, {
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

        wrapper.find('.filter').trigger('click')
        expect( mockRouter.push ).toHaveBeenCalledWith({ name: 'filter' })
    });


    
    test('Al clickear boton de tag con Role2 el guard  NO se dispara', async() => {
        
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
        
        wrapper.find('.tag').trigger('click')     
        await flushPromises()

        expect( Swal.fire ).not.toHaveBeenCalled()      
    });


    test('Al clickear boton de filtro con Role1 el guard NO se dispara', async() => {
        
        localStorage.setItem('rol', storeRole1.state.user.rol )
        
        router.push({ name: 'home' })

        await router.isReady()

        const wrapper = shallowMount( HomeView, {
            global: {
            plugins: [ storeRole1, router ],

            },
            computed: {
                isAuthenticated() {
                return storeRole1.state.user.isAuthenticated
                }
            },
        })
        
        wrapper.find('.filter').trigger('click')     
        await flushPromises()

        expect( Swal.fire ).not.toHaveBeenCalled()      
    });

})



        